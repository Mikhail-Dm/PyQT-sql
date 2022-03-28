"""
    1. Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
        Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или
        ip-адресом. В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего
        сообщения («Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью
        функции ip_address().
        (Внимание! Аргументом сабпроцеса должен быть список, а не строка!!! Крайне желательно использование потоков.)
"""


from ipaddress import ip_address, ip_interface
import platform
from subprocess import Popen, PIPE


list_nodes = []
for url in ['yandex.ru', 'a', 'google.com', '8.8.8.0']:
    try:
        list_nodes.append(ip_address(url))
        # my_list.append(ip_interface(url))
    except ValueError:
        list_nodes.append(url)

    param = "-n" if platform.system().lower() == 'windows' else "-c"
    command = ["ping", param, "1", url]

    process = Popen(command, stdout=PIPE, stderr=PIPE)
    stdout_data, stderr_data = process.communicate()
    if stdout_data:
        print(f'Узел "{url}" доступен.')
    else:
        print(f'Узел "{url}" недоступен.')


print(f'\nСписок узлов: {list_nodes}')
