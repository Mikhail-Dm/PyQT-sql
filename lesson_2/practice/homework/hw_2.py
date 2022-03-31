"""
    2. Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
        Меняться должен только последний октет каждого адреса. По результатам проверки должно
        выводиться соответствующее сообщение.
"""
import threading
import platform
from ipaddress import ip_address
from subprocess import Popen, PIPE


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


if __name__ == '__main__':
    result = {'Узел доступен': [], 'Узел недоступен': []}
    input_host = '8.8.8.0'
    range_ping = 250
    print(host_range_ping(input_host, range_ping))
