import ipaddress
import platform
from subprocess import Popen, PIPE
import chardet
import pprint


for url in ["yandex.ru", "a", 'google.com', '8.8.8.0']:
    param = "-n" if platform.system().lower() == 'windows' else "-c"
    command = ["ping", param, "1", url]
    process = Popen(command, stdout=PIPE, stderr=PIPE)

    stdout_data, stderr_data = process.communicate()
    if stdout_data:
        print(f'Узел "{url}" доступен.')
    else:
        print(f'Узел "{url}" недоступен.')


# def my_while(num, ip):
#     first_num = 0
#     new_ip = my_ip(ip)
#     my_list = []
#     while True:
#         if first_num == num:
#             return my_list
#         else:
#             my_list.append(str(new_ip))
#             new_ip += 1
#             first_num += 1
#             continue
#
#
# def my_ip(inp_ip):
#     try:
#         my_ip = ipaddress.ip_address(inp_ip)
#         return my_ip
#     except ValueError:
#         print('Неверный формат Ip-адреса.')


# pprint.pprint(my_while(5, '192.168.1.0'), width=40)
# print(my_while(5, '192.168.1.255'))
