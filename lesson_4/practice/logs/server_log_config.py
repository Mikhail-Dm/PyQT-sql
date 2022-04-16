import os
import sys

# logging - стандартный модуль для организации логирования
import logging.handlers
sys.path.append('../')



# Создаем объект форматирования:
FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s ")

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'server.log')

# Создаем файловый обработчик логирования (можно задать кодировку):
HANDLER = logging.handlers.TimedRotatingFileHandler(
    filename=PATH,
    when='D',
    interval=1,
    encoding='utf-8'
)

HANDLER.suffix = '%Y-%m-%d'
HANDLER.setFormatter(FORMATTER)

# Создаем объект-логгер с именем app.server:
LOGER = logging.getLogger('server')
# Добавляем в логгер новый обработчик событий и устанавливаем уровень логирования
LOGER.addHandler(HANDLER)
LOGER.setLevel(logging.DEBUG)


if __name__ == '__main__':
    STREAM_HANDLER = logging.StreamHandler()
    STREAM_HANDLER.setFormatter(FORMATTER)
    STREAM_HANDLER.setLevel(logging.DEBUG)
    LOGER.addHandler(STREAM_HANDLER)
    LOGER.debug('message')

    # LOGGER_S.critical('Критическая ошибка')
    # LOGGER_S.error('Ошибка')
    # LOGGER_S.debug('Отладочная информация')
    # LOGGER_S.info('Информационное сообщение')
