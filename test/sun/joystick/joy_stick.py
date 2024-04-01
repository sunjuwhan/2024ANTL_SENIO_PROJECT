import spidev
import time
import os

import socket
HOST='165.229.185.195'
PORT = 5000

def set_spi(num):
  spi=spidev.SpiDev()
  spi.open(num,0)
  spi.max_speed_hz=1000000   
  return spi


def ReadChannel(channel,spi):           
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

def stabil_vrx(vrx_pos):
  if(vrx_pos>=500 and vrx_pos<=510):
    vrx_pos=500
  elif(vrx_pos>=0 and vrx_pos < 3):
    vrx_pos=0
  elif(vrx_pos>=1000 and vrx_pos <=1030):
    vrx_pos=1000
  return vrx_pos

def stabil_vry(vry_pos):
  if(vry_pos>=495 and vry_pos<=510):
    vry_pos=500
  elif(vry_pos>=0 and vry_pos < 3):
    vry_pos=0
  elif(vry_pos>=1000 and vry_pos <=1035):
    vry_pos=1000
  return vry_pos
    
def stabil_vrx_2(vrx_pos_2):
  if(vrx_pos_2>=518 and vrx_pos_2 <=528):
    vrx_pos_2=500
  elif (vrx_pos_2>=0 and vrx_pos_2 < 3):
    vrx_pos_2=0
  elif (vrx_pos_2>=1000 and vrx_pos_2<=1030):
    vrx_pos_2=1000
  return vrx_pos_2

def stabil_vry_2(vry_pos_2):
  if(vry_pos_2>=501 and vry_pos_2<=511):
    vry_pos_2=500
  elif (vry_pos_2>=0 and vry_pos_2<=5):
    vry_pos_2=0
  elif (vry_pos_2>=1000 and vry_pos_2<=1030):
    vry_pos_2=1000
  return vry_pos_2 

def run():
  spi_left=set_spi(0)
  spi_right=set_spi(1)
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.connect((HOST, PORT))
  swt_channel = 0  
  vrx_channel = 1  
  vry_channel = 2  
  swt_channel_2 = 0  
  vrx_channel_2 = 1  
  vry_channel_2 = 2  

  delay = 0.1
  degree=20


  while True:
    vrx_pos = ReadChannel(vrx_channel,spi_left)  
    vry_pos =abs (ReadChannel(vry_channel,spi_left)-1022)
    swt_val = ReadChannel(swt_channel,spi_left)  
    vrx_pos_2 = ReadChannel(vrx_channel_2,spi_right)  
    vry_pos_2 = abs(ReadChannel(vry_channel_2,spi_right) -1023)
    swt_val_2 = ReadChannel(swt_channel_2,spi_right)  
 
    vrx_pos=float((stabil_vrx(vrx_pos)-500)/500)
    vry_pos=float(stabil_vry(vry_pos)/1000)
    vrx_pos_2=float((stabil_vrx_2(vrx_pos_2)-500)/500)
    vry_pos_2=float((stabil_vry_2(vry_pos_2)-500)/500)
    
    mode=0
    msg=f"{vrx_pos} {vry_pos} {vrx_pos_2} {vry_pos_2} "+mode  #yaw throtle  roll pirch
    print(msg)
    sock.sendto(msg.encode(),(HOST,PORT))
    time.sleep(delay)
  
run()