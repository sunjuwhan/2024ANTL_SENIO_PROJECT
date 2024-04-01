import numpy as np
from view.constant import *
from socket import *
from threading import *
from model.pilot_model import *
from model.video_mode import *
import socket
class SocketView():
    def __init__(self,model:PilotModel,video:VideoModel) -> None:
        self.video_socket=None
        self.pilot_socket=None
        self.__pilot_mode=model
        self.__video_model=video
    
    def make_socket(self):
        print('a')
        self.video_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        print('b')
        self.pilot_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        print('c')
        try:
            self.pilot_socket.bind(("127.0.0.1",5000)) 
        except Exception as e:
            print(e)
            
        print('d')
    def __data_send(self): #이미지 전송할 함수
       while True :  
           ###여기에 추후 type을 check해서 real_sense를 보낼지 pi camera를 보낼지 아니면 임시 데이터를 보낼지 판단해야하는 부분
           
            #frame=self.__video_model.get_frame() #이거는 파이 frame인지 real_sense frame인지에 따라서 변할수있는것
            
            #color_frame=frame.get_color_frame()
            #color_image=np.asanyarray(color_frame.get_data())
            #d=color_image.flatten()
            #s=d.tostring()
            #for i in range(20) :
                #self.video_socket.sendto(bytes([i]) + s[i*46080:(i+1)*46080],(UDP_IP,UDP_PORT))
            #print(self.__video_model.get_frame())
            self.video_socket.sendto((self.__video_model.get_frame().encode() ),("165.229.185.195",5002))
            
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
                print("recved dead")
                print(e)
            
    def run(self):
        try:
            print("making thread")
            self.make_socket()
            print("2")
            send_thread=Thread(target=self.__data_send)
            recv_thread=Thread(target=self.__data_recv)
            print("22222")
            send_thread.start()
            recv_thread.start()
            print("socket thread satar")
        except:
            print("socket_view thread is dead")
    
 
        
            
        