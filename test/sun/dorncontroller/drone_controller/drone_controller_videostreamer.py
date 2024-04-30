import cv2
import numpy as np
import socket
import numpy
AP_IP="192.168.32.1"
PORT=8005
MY_IP="192.168.50.47"
BUFFER_SIZE=46081
class class_Drone_Controller_VideoStreamer:
    def __init__(self, info):
        self.ip_address = MY_IP#내 ip   ap로 
        self.port = PORT  #고정
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.ip_address, self.port))
    def assemble_image(self,slices):
        return np.vstack(slices)
    def receive_video(self):
        frames = [b'' for _ in range(5)]

        while True:
            picture = b''
            data, addr = self.socket.recvfrom(46081)  # 각 패킷은 46081바이트
            frames[data[0]] = data[1:46081]  # 수신된 프레임 데이터 저장
            if data[0] == 4:  # 모든 패킷을 다 받았을 때
                for i in range(5):
                    picture += frames[i]  # 모든 프레임 데이터를 하나로 합침

                # 바이트 스트링을 numpy 배열로 변환하고 이미지로 디코딩
                frame = cv2.imdecode(np.frombuffer(picture, dtype=np.uint8), cv2.IMREAD_COLOR)
                cv2.imshow("frame", frame)

                # 프레임 표시 시간 계산

                # 'q' 키를 누르면 종료
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break
    def run_VideoStreamer(self):
        self.receive_video()