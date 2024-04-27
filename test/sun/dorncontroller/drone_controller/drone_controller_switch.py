import RPi.GPIO as GPIO
import time
from drone_controller.drone_controller_information import *

class class_Drone_Controller_Switch:
    def __init__(self, info):
        self.info = info
        self.switch1_pin = 13  # 보드 기준 핀 번호
        self.switch2_pin = 11
        self.switch3_pin = 36
        self.switch4_pin = 37
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.switch1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 풀 업 설정
        GPIO.setup(self.switch2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.switch3_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.switch4_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def runSwitch(self):
        while True:
            # 현재 스위치 상태 읽기
            self.info.switch1 = True if GPIO.input(self.switch1_pin) == GPIO.HIGH else False    #왼쪽위 
            self.info.switch2 = True if GPIO.input(self.switch2_pin) == GPIO.HIGH else False    #왼쪽 아래
            self.info.switch3 = True if GPIO.input(self.switch3_pin) == GPIO.HIGH else False   #오른쪽 위
            self.info.switch4 = True if GPIO.input(self.switch4_pin) == GPIO.HIGH else False  #오른쪽 아래 
            time.sleep(0.05)
