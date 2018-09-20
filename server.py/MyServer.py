import random
import socket
import struct
import threading
from datetime import datetime


def pack_data(sno=1):
    factory_no = sno  # random.randint(0, 4)
    furnace_no = sno * 2  # sno % 172
    a_i = random.random()
    b_i = random.random()
    c_i = random.random()
    i_default = 0.4
    a_v = 0.5
    b_v = 0.6
    c_v = 0.7
    e_speed = 0.8
    r_speed = 0.9
    a_action = 1.1
    b_action = 1.2
    c_action = 1.3
    indicators = 0x7000
    now = datetime.now()
    c_sum = 0x34
    print(factory_no, furnace_no, now)
    return struct.pack('!hhhffffffffffffihhhhhhh', sno, factory_no, furnace_no,
                       a_i, b_i, c_i, i_default, a_v, b_v, c_v, e_speed, r_speed,
                       a_action, b_action, c_action, indicators,
                       now.year, now.month, now.day, now.hour, now.minute, now.second,
                       c_sum)


def send_data(ip, port, n):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        while n:
            data = pack_data(n)
            sock.send(data)
            n -= 1
        # response = str(sock.recv(1024), 'ascii')
        # print("Received: {}".format(response))


if __name__ == '__main__':
    ip, port = "localhost", 54321

    for i in range(5):
        client = threading.Thread(target=send_data, args=(ip, port, 10))
        client.deamon = True
        client.start()
