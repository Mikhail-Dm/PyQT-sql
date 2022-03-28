import os
import sys

# logging - стандартный модуль для организации логирования
import logging.handlers
sys.path.append('../')


# Создаем объект форматирования:
FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s ")

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client.log')

# Создаем файловый обработчик логирования (можно задать кодировку):
FILE_HANDLER = logging.FileHandler(filename=PATH, encoding='utf-8')
# FILE_HANDLER = logging.FileHandler('client.log')
FILE_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setLevel(logging.DEBUG)

# Создаем объект-логгер с именем app.server:
LOGER = logging.getLogger('client')
# Добавляем в логгер новый обработчик событий и устанавливаем уровень логирования
LOGER.addHandler(FILE_HANDLER)
LOGER.setLevel(logging.DEBUG)


if __name__ == '__main__':
    STREAM_HANDLER = logging.StreamHandler()
    STREAM_HANDLER.setFormatter(FORMATTER)
    STREAM_HANDLER.setLevel(logging.DEBUG)
    LOGER.addHandler(STREAM_HANDLER)
    LOGER.debug('message')

    # LOGGER_C.critical('Критическая ошибка')
    # LOGGER_C.error('Ошибка')
    # LOGGER_C.debug('Отладочная информация')
    # LOGGER_C.info('Информационное сообщение')
