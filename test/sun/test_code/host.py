import socket
import time
import sys

# A로부터 데이터를 받습니다.


# 소켓 생성



#HOST='165.229.185.195'
server_port=65433
HOST='192.168.50.71'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST,server_port))

HOST_2='192.168.232.137'
PORT_2=8080
sock_2=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while True:
    data,addr=sock.recvfrom(100)
    print(data)
    sock_2.sendto(data,(HOST_2,PORT_2))