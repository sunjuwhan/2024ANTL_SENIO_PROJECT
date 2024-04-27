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
            if self.info.drone_state=="disarm":  #현재 드론 상태가 disarm 즉 미시동상태일때
                if self.info.switch1==1:  #시동 걸면 시동 거는 신호만 보내고
                    self.info.drone_state="arm"    
                    mode="arm"  #시동걸러 들어가고
                   

            #이미 시동 상태일경우 다른 모드를 전송할수있어
            elif self.info.drone_state=="arm":
                if self.info.switch1==0:
                    #시동 끄는 곳으로 날라가고
                    self.info.drone_state="disarm"
                    mode="disarm"
                if self.info.switch2==1  and self.info.switch4==0:  #2번 스위치가 켜지면 착륙 4번이 꺼져있고
                    mode="land"
                elif self.info.switch2==0 and self.info.switch4==1:
                    mode="takeoff"
                if self.info.switch2==0 and self.info.switch4==0 and self.info.switch3==1:
                    mode="manual" 
                elif self.info.switch2==0 and self.info.switch4==0 and self.info.switch3==0:
                    mode="gps"
                    
            joystick_data = f"{self.info.joystick_Left_x} {self.info.joystick_Left_y} {self.info.joystick_Right_x} {self.info.joystick_Right_y} {mode}" 
            self.info.__joystick_data=joystick_data
            # 조이스틱 값 TCP 전송
            self.send_joystick_data(joystick_data)
