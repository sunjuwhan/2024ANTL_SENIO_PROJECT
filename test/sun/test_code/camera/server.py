import cv2
import numpy as np
import socket
import struct

# 비디오 소켓 설정
UDP_IP = '192.168.50.63'
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# 비디오 출력창 생성
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

while True:
    # 이미지 크기 수신
    data, addr = sock.recvfrom(4)
    size = struct.unpack("L", data)[0]
    
    # 이미지 데이터 수신
    data, addr = sock.recvfrom(size)
    nparr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 비디오 출력
    cv2.imshow('frame', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()