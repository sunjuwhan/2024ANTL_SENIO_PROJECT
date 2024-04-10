from drone_controller.drone_controller_information import *
from threading import Thread, Lock
import socket
import pickle
import time
AP_IP="192.168.32.3"
PORT=8080
DRONE_IP="192.168.50.63"
class class_drone_controller_datasender:
    def __init__(self, info:class_Drone_Controller_Information):
        self.info = info
        self.socket_lock = Lock()  # 소켓 동기화를 위한 Lock 객체
        self.target_ip = AP_IP  # 드론 IP 주소   ap 192.168.32.3    drone 192.168.50.63
        self.target_port = PORT# port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.target_ip, self.target_port))
        print("send connect complete")
    def send_joystick_data(self, data):
        try:
            # 데이터를 직렬화하고 전송
            print(data)
            self.socket.sendall(data.encode())
            time.sleep(0.2)  
        except Exception as e:
            print(f"Error sending joystick data: {e}")

    def run_data_sender(self):
        while True:
            mode=""
            if(self.info.button1==1):
                mode="arm"
            elif (self.info.button2==1) :
                mode="takeoff"
            elif (self.info.button3==1):
                mode="manual"
            elif (self.info.button4==1):
                mode="gps"
            elif (self.info.button5==1):
                mode="disarm"
            elif (self.info.button6==1):
                self.info.button1=0
                self.info.button2=0
                self.info.button3=0
                self.info.button4=0
                self.info.button5=0
                self.info.button6=0
                mode="manual"    
            joystick_data = f"{self.info.joystick_Left_x} {self.info.joystick_Left_y} {self.info.joystick_Right_x} {self.info.joystick_Right_y} {mode}" 
            # 조이스틱 값 TCP 전송
            self.send_joystick_data(joystick_data)
