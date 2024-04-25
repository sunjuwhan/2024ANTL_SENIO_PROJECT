import cv2
import numpy as np
import socket
from picamera2 import Picamera2

# Picamera2 초기화
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
#picam2.preview_configuration.main.format = "RGB888"
#picam2.preview_configuration.align()
#picam2.configure("preview")
picam2.start()

# UDP 설정
IP_CONTROLLER = "192.168.50.52"
PORT_CONTROLLER = 8080  # 적절한 포트번호로 변경하세요
BUFFER_SIZE = 46081
video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 이미지를 조각으로 나누는 함수
def split_image(image, num_slices):
    slice_height = image.shape[0] // num_slices
    slices = []
    for i in range(num_slices):
        start = i * slice_height
        end = start + slice_height
        slices.append(image[start:end, :])
    return slices

try:
    while True:
        im = picam2.capture_array()
        # 이미지를 20개의 조각으로 나누기
        #image_slices = split_image(im, 20)
        #s=im.tobytes()
        s=im.flatten()
        s=s.tostring()
        #각 조각을 전송
        #for i, slice_img in enumerate(image_slices):
        #    data = cv2.imencode('.jpg', slice_img)[1].tobytes()  # JPEG 형식으로 인코딩하여 바이트로 변환
        #    video_socket.sendto(bytes([i]) + data, (IP_CONTROLLER, PORT_CONTROLLER))
        for i in range(20):
            #video_socket.sendto(bytes([i]), (IP_CONTROLLER, PORT_CONTROLLER))
            video_socket.sendto(bytes([i]) +s[i*46080:(i+1) *46080], (IP_CONTROLLER, PORT_CONTROLLER))
        # 'q' 키를 누를 때까지 대기
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # OpenCV 창 닫기 및 Picamera2 종료
    cv2.destroyAllWindows()
    picam2.stop()
    video_socket.close()
