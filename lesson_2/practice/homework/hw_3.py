"""
    3. Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2.
        Но в данном случае результат должен быть итоговым по всем ip-адресам, представленным в табличном формате
            (использовать модуль tabulate).
        Таблица должна состоять из двух колонок и выглядеть примерно так:
            Reachable
            10.0.0.1
            10.0.0.2

            Unreachable
            10.0.0.3
            10.0.0.4
        ------------------ (факультативно) --------------------------
"""


import threading
import platform
from ipaddress import ip_address
from subprocess import Popen, PIPE
from tabulate import tabulate


def check_ip(value):
    try:
        host = ip_address(value)
    except Exception:
        host = value
    return host


def ping(value):
    host = check_ip(value)

    param = "-n" if platform.system().lower() == 'windows' else "-c"
    command = ['ping', param, '1', '-w', '1', str(host)]
    process = Popen(command, stdout=PIPE, stderr=PIPE)

    if process.wait() == 0:
        result.get('Узел доступен').append(str(host))
    else:
        result.get('Узел недоступен').append(str(host))
    return result


def host_ping(list_nodes):
    threads = []
    for value in list_nodes:
        thread = threading.Thread(target=ping, args=(value,), daemon=False)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return result


def host_range_ping(host, result_num):
    print('Начинаю проверку узлов...')
    check_ip(host)
    result_list = []
    num = 0
    while True:
        if num == result_num:
            break
        result_list.append(host)
        host = str(ip_address(host) + 1)
        num += 1
    return host_ping(result_list)


def host_range_ping_tab(host, result_num):
    return tabulate(host_range_ping(host, result_num), headers='keys')


if __name__ == '__main__':
    result = {'Узел доступен': [], 'Узел недоступен': []}

    # input_host = '8.8.8.0'
    input_host = input('Введите первоначальный адрес: ')

    # range_ping = 250
    range_ping = int(input('Сколько адресов проверить?: '))

    print(host_range_ping_tab(input_host, range_ping))
