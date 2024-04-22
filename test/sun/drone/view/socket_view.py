import numpy as np
from view.constant import *
from socket import *
from threading import *
from model.pilot_model import *
from model.video_mode import *
from view.constant import *
import socket
import time
class SocketView():
    def __init__(self,model:PilotModel,video:VideoModel) -> None:
        self.video_socket=None
        self.pilot_socket=None
        self.__pilot_mode=model
        self.__video_model=video
        self.__client_socket=None 
    def make_socket(self):
        self.video_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        #self.pilot_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.pilot_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        try:
            self.pilot_socket.bind((IP_DRONE,PORT_DRONE))   #여기는 내가 받아야하니까 내 주소 drone주소
            #self.pilot_socket.listen(1)
            #self.__client_socket,clien_address=self.pilot_socket.accept()
            print("make_socket end")
        except Exception as e:
            print("make_socket Error here")
            print(e)
    def __data_send(self): #이미지 전송할 함수
        while True : 
            s=self.__video_model.get_frame()  #46080
            for i in range(20):
                self.video_socket.sendto(bytes([i]) + s[i*46080:(i+1) * 46080],(IP_CONTROLLER,PORT_CONTROLLER))  #쏴야하니까 controller ip port
            
            
    def __data_recv(self):
        while True:
            try:
                recv_data=self.pilot_socket.recv(1024)
                decoded_data=recv_data.decode()
                data=decoded_data.split(' ')
                key_data=data[0:4] 
                mode_data=data[4]
                #data 를 interface인 pilot_mode에다가 저장해주고
                self.__pilot_mode.set_data(key_data,mode_data) 
                
            except Exception as e:
                print("receve dead")
                print(e)
            
    def run(self):
        try:
            print("making thread")
            self.make_socket()
            send_thread=Thread(target=self.__data_send)
            recv_thread=Thread(target=self.__data_recv)
            send_thread.start()
            recv_thread.start()
            print("socket thread started")
        except:
            print("socket_view thread is dead")
    
 
        
            
        