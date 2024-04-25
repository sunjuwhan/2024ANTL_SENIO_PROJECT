import cv2
import numpy as np
import socket
import struct

# UDP 소켓 설정
UDP_IP = '192.168.50.63'
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# 비디오 출력창 생성
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

# 이미지 조각을 합치는 함수
def merge_image_chunks(chunks, shape):
    height, width = shape
    image = np.zeros((height, width, 3), np.uint8)
    idx = 0
    for i in range(0, height, 100):
        for j in range(0, width, 100):
            chunk = chunks[idx]
            h, w, _ = chunk.shape
            image[i:i+h, j:j+w] = chunk
            idx += 1
    return image

while True:
    chunks = []
    total_size = 0
    # 이미지 조각 수신
    while True:
        data, addr = sock.recvfrom(65535)  # 최대 UDP 패킷 크기
        size = struct.unpack("L", data[:8])[0]
        total_size += size
        chunks.append(np.frombuffer(data[8:], np.uint8))
        if total_size >= 640 * 480 * 3:  # 예상 이미지 크기보다 크면 루프 종료
            break
    
    # 이미지 조각을 합쳐서 비디오로 출력
    img = merge_image_chunks(chunks, (480, 640))
    cv2.imshow('frame', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
