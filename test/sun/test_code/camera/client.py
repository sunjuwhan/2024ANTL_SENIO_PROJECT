import cv2
import numpy as np
import socket
import struct

# 비디오 캡처 설정
cap = cv2.VideoCapture(0)

# UDP 소켓 설정
UDP_IP = '192.168.50.63'
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    ret, frame = cap.read()
    # 이미지를 바이트 스트림으로 변환
    encoded, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = buffer.tobytes()

    # 이미지 크기 정보를 포함하여 UDP로 전송
    message_size = struct.pack("L", len(jpg_as_text))
    sock.sendto(message_size + jpg_as_text, (UDP_IP, UDP_PORT))

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()