"""
    1. Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
        Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или
        ip-адресом. В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего
        сообщения («Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью
        функции ip_address().
        (Внимание! Аргументом сабпроцеса должен быть список, а не строка!!! Крайне желательно использование потоков.)
"""
import threading
from ipaddress import ip_address
import platform
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


if __name__ == '__main__':
    result = {'Узел доступен': [], 'Узел недоступен': []}
    input_list = ['yandex.ru', 'a', 'google.com', '8.8.8.0', '8.8.8.1', '8.8.8.2', '8.8.8.3', '8.8.8.4', '8.8.8.5',
                  '8.8.8.6', '8.8.8.7', '8.8.8.8']
    print(host_ping(input_list))
