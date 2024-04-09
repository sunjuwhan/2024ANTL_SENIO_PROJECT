import drone_controller_switch
import drone_controller_joystick
import drone_controller_information
import drone_controller_videostreamer
import drone_controller_datasender
from threading import Thread, Lock
import os

class class_Drone_Controller_System:
    def __init__(self):
        self.info = drone_controller_information.class_Drone_Controller_Information()
        self.controllerJoystick_L = drone_controller_joystick.class_Drone_Controller_Joystick(0, 0, 1, 2, 0, 1, self.info)
        self.controllerJoystick_R = drone_controller_joystick.class_Drone_Controller_Joystick(1, 0, 1, 2, 0, 2, self.info)
        self.videoStreamer = drone_controller_videostreamer.class_Drone_Controller_VideoStreamer()
        self.dataSender = drone_controller_datasender.class_drone_controller_datasender(self.info)

    def start_Drone_Controller(self):
        print("SYSTEM ALARM::Drone Controller Started")
        thread_Joystick_Left = Thread(target=self.controllerJoystick_L.run_joystick)
        thread_Joystick_Right = Thread(target=self.controllerJoystick_R.run_joystick)
        thread_VideoStream = Thread(target=self.videoStreamer.run_VideoStreamer())
        thread_dataSender = Thread(target=self.dataSender.run_data_sender())
        thread_Joystick_Left.start()
        thread_Joystick_Right.start()
        thread_VideoStream.start()
        thread_dataSender.start()

    def print_system_log(self):
        print("=" * 50)
        print("Drone Controller State")
        print("Joystick Left(x:{}, y:{}, val:{}".format(self.info.joystick_Left_x, self.info.joystick_Left_y,
                                                        self.info.joystick_Left_val))
        print("Joystick Right(x:{}, y:{}, val:{}".format(self.info.joystick_Right_x, self.info.joystick_Right_y,
                                                         self.info.joystick_Right_val))
        print("=" * 50)
        os.system('clear')

            
    def run_drone_controller_system(self):
        # controllerSwitch = drone_controller_switch.class_Drone_Controller_Switch(self)
        self.start_Drone_Controller()
        while True:
            self.print_system_log()