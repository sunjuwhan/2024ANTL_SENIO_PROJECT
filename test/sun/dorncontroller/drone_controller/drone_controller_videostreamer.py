import cv2
import numpy as np
import socket
import numpy
AP_IP="192.168.32.1"
PORT=8005
MY_IP="192.168.50.47"
BUFFER_SIZE=46081
class class_Drone_Controller_VideoStreamer:
    def __init__(self):
        self.ip_address = MY_IP#내 ip   ap로 
        self.port = PORT  #고정
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.ip_address, self.port))
    def assemble_image(self,slices):
        return np.vstack(slices)
    def receive_video(self):
        picture=b''
        data,addr=self.socket.recvfrom(46081)
        while True:
            picture = b''
            data, addr = self.socket.recvfrom(46081)
            s[data[0]] = data[1:46081]

            if data[0] == 4:
                for i in range(5):
                    picture += s[i]
                frame = cv2.imdecode(np.frombuffer(picture, dtype=np.uint8), cv2.IMREAD_COLOR)
                cv2.imshow("frame", frame)
    def run_VideoStreamer(self):
        self.receive_video()