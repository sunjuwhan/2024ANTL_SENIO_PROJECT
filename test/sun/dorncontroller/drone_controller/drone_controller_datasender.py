from drone_controller.drone_controller_information import *
from threading import Thread, Lock
import socket
import pickle
import time
#AP_IP="192.168.32.3"
PORT=8080
#PORT=65433
DRONE_IP="192.168.50.63"
HOST_IP="192.168.50.71"
class class_drone_controller_datasender:
    def __init__(self, info:class_Drone_Controller_Information):
        self.info = info
        self.target_ip = DRONE_IP# 드론 IP 주소   ap 192.168.32.3    drone 192.168.50.63
        self.target_port = PORT# port
        #self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.connect((self.target_ip, self.target_port))
    def send_joystick_data(self, data):
        try:
            # 데이터를 직렬화하고 전송
            self.socket.sendto(data.encode(),(self.target_ip,self.target_port))
        except Exception as e:
            print(f"Error sending joystick data: {e}")

    def run_data_sender(self):
        while True:
            mode=""
            #if(self.info.switch1==1):
            #    mode="arm"
            #else:
            #    mode="disarm"
            if (self.info.switch2==1) :
                mode="gps"
            else:
                mode="manual"
            mode="manual"
            joystick_data = f"{self.info.joystick_Left_x} {self.info.joystick_Left_y} {self.info.joystick_Right_x} {self.info.joystick_Right_y} {mode}" 
            # 조이스틱 값 TCP 전송
            self.send_joystick_data(joystick_data)
