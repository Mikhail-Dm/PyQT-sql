import datetime
from pprint import pprint
from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class ServerStorage:
    Base = declarative_base()

    class AllUsers(Base):
        __tablename__ = 'all_users'
        id = Column(Integer, primary_key=True)
        login = Column(String, unique=True)
        last_connection = Column(DateTime)

        def __init__(self, login):
            self.id = None
            self.login = login
            self.last_connection = datetime.datetime.now()

    class ActiveUsers(Base):
        __tablename__ = 'active_users'
        id = Column(Integer, primary_key=True)
        user = Column(String, ForeignKey('all_users.login'), unique=True)
        ip_address = Column(String)
        port = Column(Integer)
        time_login = Column(DateTime)

        def __init__(self, user, ip_address, port, time_login):
            self.user = user
            self.ip_address = ip_address
            self.port = port
            self.time_login = time_login

    class LoginHistory(Base):
        __tablename__ = 'login_history'
        id = Column(Integer, primary_key=True)
        user = Column(String, ForeignKey('all_users.login'))
        status = Column(String)
        ip_address = Column(String)
        port = Column(Integer)
        last_connection = Column(DateTime)

        def __init__(self, user, status, ip_address, port, last_connection):
            self.user = user
            self.status = status
            self.ip_address = ip_address
            self.port = port
            self.last_connection = last_connection

    class UsersContacts(Base):
        __tablename__ = 'user_contacts'
        id = Column(Integer, primary_key=True)
        user = Column(String, ForeignKey('all_users.login'))
        contact = Column(String, ForeignKey('all_users.login'))

        def __init__(self, user, contact):
            self.user = user
            self.contact = contact

    class UsersHistory(Base):
        __tablename__ = 'users_history'
        id = Column(Integer, primary_key=True)
        user = Column(String, ForeignKey('all_users.login'))
        sent = Column('sent', Integer)
        accepted = Column('accepted', Integer)

        def __init__(self, user, sent, accepted):
            self.user = user
            self.sent = sent
            self.accepted = accepted

    def __init__(self, path):
        self.engine = create_engine(f'sqlite:///{path}', echo=False, pool_recycle=7200)

        self.Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    def user_login(self, username, ip_address, port):
        request_user = self.session.query(self.AllUsers).filter_by(login=username)

        if request_user.count():
            user = request_user.first()
            user.last_connection = datetime.datetime.now()
        else:
            user = self.AllUsers(username)
            self.session.add(user)
            self.session.commit()

        new_active_user = self.ActiveUsers(user.login, ip_address, port, datetime.datetime.now())
        self.session.add(new_active_user)

        history_user = self.LoginHistory(user.login, 'login', ip_address, port, datetime.datetime.now())
        self.session.add(history_user)

        self.session.commit()

    def user_logout(self, username):
        user_active = self.session.query(self.AllUsers).filter_by(login=username).first()
        self.session.query(self.ActiveUsers).filter_by(user=user_active.login).delete()

        user_history = self.session.query(self.LoginHistory).filter_by(user=username).first()
        history_user = self.LoginHistory(
            user_history.user,
            'logout',
            user_history.ip_address,
            user_history.port,
            datetime.datetime.now(),
        )
        self.session.add(history_user)

        self.session.commit()

    def active_users_list(self):
        query = self.session.query(
            self.ActiveUsers.user,
            self.ActiveUsers.ip_address,
            self.ActiveUsers.port,
            self.ActiveUsers.time_login,
        ).join(self.AllUsers)
        return query.all()

    def users_list(self):
        query = self.session.query(
            self.AllUsers.login,
            self.AllUsers.last_connection,
        )
        return query.all()

    def login_history(self, username=None):
        query = self.session.query(
            self.LoginHistory.user,
            self.LoginHistory.status,
            self.LoginHistory.ip_address,
            self.LoginHistory.port,
            self.LoginHistory.last_connection,
        ).join(self.AllUsers)
        if username:
            query = query.filter(self.AllUsers.login == username)
        return query.all()

    # Функция фиксирует передачу сообщения и делает соответствующие отметки в БД
    def process_message(self, sender, recipient):
        # Получаем ID отправителя и получателя
        sender = self.session.query(self.AllUsers).filter_by(name=sender).first().id
        recipient = self.session.query(self.AllUsers).filter_by(name=recipient).first().id
        # Запрашиваем строки из истории и увеличиваем счётчики
        sender_row = self.session.query(self.UsersHistory).filter_by(user=sender).first()
        sender_row.sent += 1
        recipient_row = self.session.query(self.UsersHistory).filter_by(user=recipient).first()
        recipient_row.accepted += 1

        self.session.commit()

    # Функция добавляет контакт для пользователя.
    def add_contact(self, user, contact):
        # Получаем ID пользователей
        user = self.session.query(self.AllUsers).filter_by(name=user).first()
        contact = self.session.query(self.AllUsers).filter_by(name=contact).first()

        # Проверяем что не дубль и что контакт может существовать (полю пользователь мы доверяем)
        if not contact or self.session.query(self.UsersContacts).filter_by(user=user.id, contact=contact.id).count():
            return

        # Создаём объект и заносим его в базу
        contact_row = self.UsersContacts(user.id, contact.id)
        self.session.add(contact_row)
        self.session.commit()

    # Функция удаляет контакт из базы данных
    def remove_contact(self, user, contact):
        # Получаем ID пользователей
        user = self.session.query(self.AllUsers).filter_by(name=user).first()
        contact = self.session.query(self.AllUsers).filter_by(name=contact).first()

        # Проверяем что контакт может существовать (полю пользователь мы доверяем)
        if not contact:
            return

        # Удаляем требуемое
        print(self.session.query(self.UsersContacts).filter(
            self.UsersContacts.user == user.id,
            self.UsersContacts.contact == contact.id
        ).delete())
        self.session.commit()

    # Функция возвращает список контактов пользователя.
    def get_contacts(self, username):
        # Запрашиваем указанного пользователя
        user = self.session.query(self.AllUsers).filter_by(name=username).one()

        # Запрашиваем его список контактов
        query = self.session.query(self.UsersContacts, self.AllUsers.name). \
            filter_by(user=user.id). \
            join(self.AllUsers, self.UsersContacts.contact == self.AllUsers.id)

        # выбираем только имена пользователей и возвращаем их.
        return [contact[1] for contact in query.all()]

    # Функция возвращает количество переданных и полученных сообщений
    def message_history(self):
        query = self.session.query(
            self.AllUsers.login,
            self.AllUsers.last_connection,
            self.UsersHistory.sent,
            self.UsersHistory.accepted
        ).join(self.AllUsers)
        # Возвращаем список кортежей
        return query.all()


if __name__ == '__main__':
    db = ServerStorage('server_base.db3')
    db.user_login('client_1', '192.168.1.4', 8888)
    db.user_login('client_2', '192.168.1.5', 7777)

    print('*' * 50 + '\nВыводим список активных пользователей:')
    pprint(db.active_users_list())
    print('*' * 50 + '\n')

    print('*' * 50 + '\nВыводим список пользователей, но перед этим разлогиниваем "client_1":')
    db.user_logout('client_1')
    pprint(db.users_list())
    print('*' * 50 + '\n')

    print('*' * 50 + '\nВыводим список активных пользователей:')
    pprint(db.active_users_list())
    print('*' * 50 + '\n')

    print('*' * 50 + '\nВыводим список пользователей, но перед этим разлогиниваем "client_2":')
    db.user_logout('client_2')
    pprint(db.users_list())
    print('*' * 50 + '\n')

    print('*' * 50 + '\nНиже список активных пользователей:')
    pprint(db.active_users_list())
    print('*' * 50 + '\n')

    print('*' * 50 + '\nНиже история пользователя "client_1":')
    pprint(db.login_history('client_1'))
    print('*' * 50 + '\n')

    print('*' * 50 + '\nНиже все пользователи:')
    pprint(db.users_list())
    print('*' * 50 + '\n')

    db.add_contact('test2', 'test1')
    db.add_contact('test1', 'test3')
    db.add_contact('test1', 'test6')
    db.remove_contact('test1', 'test3')
    db.process_message('McG2', '1111')
    pprint(db.message_history())
