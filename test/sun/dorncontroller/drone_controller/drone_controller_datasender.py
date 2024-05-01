from drone_controller.drone_controller_information import *
from threading import Thread, Lock
import socket
import pickle
import time
AP_IP="192.168.32.3"
PORT=8080
#PORT=65433
DRONE_IP="192.168.50.63"
HOST_IP="192.168.50.237"
class class_drone_controller_datasender:
    def __init__(self, info:class_Drone_Controller_Information):
        self.info = info
        self.target_ip = DRONE_IP# 드론 IP 주소   ap 192.168.32.3    drone 192.168.50.63
        self.target_port = PORT# port
        while True:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.target_ip, self.target_port))
                break
            except:
                continue
        #self.socket=None
    def send_joystick_data(self, data):
        try:
            # 데이터를 직렬화하고 전송
            self.socket.sendto(data.encode(),(self.target_ip,self.target_port))
            self.info.arm_data=self.socket.recv(30).decode()  #다시 전달받아
            pass
        except Exception as e:
            print(f"Error sending joystick data: {e}")

    def run_data_sender(self):
        while True:
            mode=""
            if self.info.switch1==1:  #내가 시동을 걸었어
                if self.info.arm_data=="off":
                    mode="arm"
                elif self.info.arm_data=="disarm":
                    mode="arm"
                elif self.info.arm_data=="arm":
                    #여기서 부터 다음 단계로넘어가 
                    if self.info.switch3==True:
                        if self.info.arm_data=="land":  #이미 착륙이 완료 되었을수도 있잖아.
                            mode="disarm"  #바로 자동으로 시동을 끄게끔 해주는거지
                            continue
                        else: 
                            mode="land" 
                    else:  #switch 3 번이 꺼져있어그러면 다음 단게로 넘어갈수있어
                        if self.info.switch4==True:
                            mode="manual"
                        elif self.info.switch4==False:
                            mode="gps"
                            
            elif self.info.switch1==0:
                if self.info.arm_data=="land":
                    mode="disarm"
            joystick_data = f"{self.info.joystick_Left_x} {self.info.joystick_Left_y} {self.info.joystick_Right_x} {self.info.joystick_Right_y} {mode}" 
            self.info.now_mode=mode
            self.info.joystick_data=joystick_data
            # 조이스틱 값 TCP 전송
            self.send_joystick_data(joystick_data)
