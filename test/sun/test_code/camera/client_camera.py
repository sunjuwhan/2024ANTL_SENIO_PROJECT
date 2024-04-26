import socket
import cv2
import time
import numpy as np

UDP_IP = "192.168.50.47"
UDP_PORT = 9505

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)

# 카메라 해상도 설정
cap.set(3, 320)  # 가로 해상도
cap.set(4, 240)  # 세로 해상도

while True:
    ret, frame = cap.read()
    if ret:
        # 프레임을 JPEG 형식으로 압축
        _, encoded_frame = cv2.imencode('.jpg', frame)
        
        # 압축된 이미지 데이터를 바이트 스트링으로 변환
        s = encoded_frame.tobytes()

        # 바이트 스트링을 여러 패킷으로 나누어 전송
        for i in range(5):
            sock.sendto(bytes([i]) + s[i * 46080:(i + 1) * 46080], (UDP_IP, UDP_PORT))  # JPEG 압축된 프레임 전송


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
