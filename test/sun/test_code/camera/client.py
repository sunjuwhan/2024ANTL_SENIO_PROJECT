import cv2
import numpy as np
import socket
import struct

# 비디오 캡처 설정
cap = cv2.VideoCapture(0)

# UDP 소켓 설정
UDP_IP = '192.168.50.47'
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 이미지 분할 함수
def split_image(image, chunk_size):
    chunks = []
    height, width = image.shape[:2]
    for i in range(0, height, chunk_size):
        for j in range(0, width, chunk_size):
            chunk = image[i:i+chunk_size, j:j+chunk_size]
            chunks.append(chunk)
    return chunks

# 이미지 크기 정보를 포함하여 UDP로 전송
def send_image_chunks(chunks):
    for chunk in chunks:
        # 이미지를 바이트 스트림으로 변환
        encoded, buffer = cv2.imencode('.jpg', chunk)
        jpg_as_text = buffer.tobytes()

        # 이미지 크기 정보를 포함하여 UDP로 전송
        message_size = struct.pack("L", len(jpg_as_text))
        sock.sendto(message_size + jpg_as_text, (UDP_IP, UDP_PORT))

# 이미지를 작은 조각으로 나누어 전송
while True:
    ret, frame = cap.read()
    chunks = split_image(frame, 100)  # 이미지를 100x100 크기의 조각으로 나눔
    send_image_chunks(chunks)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
