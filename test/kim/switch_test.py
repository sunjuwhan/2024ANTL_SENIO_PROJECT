import gpiod
import time
class class_Drone_Controller_Switch:
    def __init__(self):

        self.switch1_pin = 27  # BCM 핀 번호
        self.switch2_pin = 17
        self.switch3_pin = 16
        self.switch4_pin = 26
        # GPIO 디바이스 초기화
        self.chip = gpiod.Chip('gpiochip4')  # 사용하는 GPIO 칩의 이름에 따라 변경할 수 있음
        self.lines = [self.chip.get_line(offset) for offset in [self.switch1_pin, self.switch2_pin, self.switch3_pin, self.switch4_pin]]
        for line in self.lines:
            line.request(consumer='drone_controller', type=gpiod.LINE_REQ_DIR_IN)
    def runSwitch(self):
        while True:
            # 현재 스위치 상태 읽기
            switch1 = True if self.lines[0].get_value() == 1 else False    #왼쪽위
            switch2 = True if self.lines[1].get_value() == 1 else False    #왼쪽 아래
            switch3 = True if self.lines[2].get_value() == 1 else False   #오른쪽 위
            switch4 = True if self.lines[3].get_value() == 1 else False  #오른쪽 아래
            print("switch1: {}".format(switch1))
            print("switch2: {}".format(switch2))
            print("switch3: {}".format(switch3))
            print("switch4: {}".format(switch4))
            time.sleep(0.3)

if __name__ == "__main__":
    dc_switch = class_Drone_Controller_Switch()
    dc_switch.runSwitch()