"""
    1. Начать реализацию класса «Хранилище» для серверной стороны. Хранение необходимо осуществлять в базе данных.
        В качестве СУБД использовать sqlite. Для взаимодействия с БД можно применять ORM.
        Опорная схема базы данных:
            На стороне сервера БД содержит следующие таблицы:
                a) клиент:
                    * логин;
                    * информация.
                b) историяклиента:
                    * время входа;
                    * ip-адрес.
                c) списокконтактов (составляется на основании выборки всех записей с id_владельца):
                    * id_владельца;
                    * id_клиента.
"""

import datetime
from pprint import pprint
from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class ServerBase:
    Base = declarative_base()

    class AllUsers(Base):
        __tablename__ = 'all_users'
        id = Column(Integer, primary_key=True)
        login = Column(String, unique=True)
        last_connection = Column(DateTime)

        def __init__(self, login):
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

    def __init__(self):
        self.engine = create_engine('sqlite:///server_database.db3', echo=False, pool_recycle=7200)

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


if __name__ == '__main__':
    db = ServerBase()
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
