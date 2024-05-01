import PIL.ImageTk
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading
import random
import string
from drone_controller.drone_controller_information import *
import time

class class_drone_controller_display_master:
    def __init__(self, info):
        self.dc_display = None
        self.info = info

    def run_display(self):
        self.dc_display = class_drone_controller_display(self.info)

class class_drone_controller_display:
    def __init__(self, info):
        self.info = info
        self.window = tk.Tk()
        self.window.title("Flight Controller Display")
        self.window.geometry("800x480")  # Set window size to 800x480

        # Load an example image initially
        self.info.frame = cv2.imread('/home/pi/2024ANTL_SENIO_PROJECT/img/2024_ANTL_Drone.png')

        # Convert the ndarray to PIL image
        pil_image = Image.fromarray(self.info.frame)
        resized_image = pil_image.resize((640, 480))
        # Convert the PIL image to PhotoImage
        self.vid = ImageTk.PhotoImage(resized_image)

        self.frame_canvas = tk.Canvas(self.window, width=640, height=480)
        self.frame_canvas.grid(row=0, column=0, sticky="nsew")
        self.frame_canvas.create_image(0, 0, image=self.vid, anchor=tk.NW)

        self.info_frame = tk.Frame(self.window, bg="#808080", width=160, height=480, bd=2, relief=tk.SOLID)  # Adjusted height for info frame
        self.info_frame.grid(row=0, column=1, sticky="nsew")

        self.gps_frame = tk.Frame(self.info_frame, bg="#404040", bd=2, relief=tk.SOLID)  # Box around GPS info
        self.gps_frame.pack(anchor="w", padx=8, pady=(4, 0), fill=tk.X)

        self.gps_label = tk.Label(self.gps_frame, text="GPS", anchor="w", bg="#404040", fg="white", font=("Arial bold", 10))  # GPS label
        self.gps_label.pack(anchor="w")

        self.latitude_label = tk.Label(self.gps_frame, text="Latitude: Waiting for data...", anchor="w",
                                       bg="#404040", fg="white",font=("Arial", 8))  # White text color
        self.latitude_label.pack(anchor="w")

        self.longitude_label = tk.Label(self.gps_frame, text="Longitude: Waiting for data...", anchor="w",
                                        bg="#404040", fg="white", font=("Arial", 8))  # White text color
        self.longitude_label.pack(anchor="w")

        self.switch_frame = tk.Frame(self.info_frame, bg="#404040", bd=2, relief=tk.SOLID)  # Box around switch info
        self.switch_frame.pack(anchor="w", padx=8, pady=(4, 0), fill=tk.X)
        switch_title = tk.Label(self.switch_frame, text="Switch", anchor="w", bg="#404040", fg="white",
                                font=("Arial bold", 10))
        switch_title.pack(anchor="w")
        self.switch_labels = []

        self.joystick_frame_L = tk.Frame(self.info_frame, bg="#404040", bd=2,
                                         relief=tk.SOLID)  # Box around joystick L info
        self.joystick_frame_L.pack(anchor="w", padx=8, pady=(4, 0), fill=tk.X)

        self.joystick_frame_R = tk.Frame(self.info_frame, bg="#404040", bd=2,
                                         relief=tk.SOLID)  # Box around joystick R info
        self.joystick_frame_R.pack(anchor="w", padx=8, pady=(4, 0), fill=tk.X)

        self.log_text_R = tk.Text(self.info_frame, width=22, height=7, bg="#1c1c1c", fg="white", font=("Arial", 8))
        self.log_text_R.pack(anchor="w", padx=8, pady=(4, 0))

        self.start_threads()
        self.window.mainloop()

    def start_threads(self):
        self.start_video_update_thread()
        self.start_gps_update_thread()
        self.start_switches_update_thread()
        self.start_joystick_update_thread()

    def start_video_update_thread(self):
        video_thread = threading.Thread(target=self.update_video_thread)
        video_thread.daemon = True  # Daemonize thread so it will automatically close when the main thread closes
        video_thread.start()

    def update_video_thread(self):
        while True:
            frame = self.info.frame
            pil_image = Image.fromarray(frame)
            resized_image = pil_image.resize((640, 480))  # 원하는 크기로 이미지 리사이즈

            # PIL 이미지를 PhotoImage로 변환
            self.photo = ImageTk.PhotoImage(image=resized_image)

            # 비디오 프레임 업데이트는 GUI 쓰레드에서 직접 호출할 수 없으므로
            # .after 메서드를 사용하여 GUI 쓰레드에 업데이트 요청을 보냅니다.
            self.frame_canvas.after(0, self.update_video_gui)

            # 쓰레드를 잠시 대기시켜 CPU 자원 소비를 줄입니다.
            time.sleep(0.1)

    def update_video_gui(self):
        # 비디오 캔버스 업데이트
        self.frame_canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def start_gps_update_thread(self):
        gps_thread = threading.Thread(target=self.update_gps_thread)
        gps_thread.daemon = True
        gps_thread.start()

    def update_gps_thread(self):
        while True:
            self.update_gps()
            time.sleep(1)  # 1초마다 업데이트

    def update_gps(self):
        latitude_text = f"Latitude: {self.info.drone_latitude:.5f}"
        longitude_text = f"Longitude: {self.info.drone_longitude:.5f}"

        self.latitude_label.config(text=latitude_text)
        self.longitude_label.config(text=longitude_text)

    def start_switches_update_thread(self):
        switches_thread = threading.Thread(target=self.update_switches_thread)
        switches_thread.daemon = True
        switches_thread.start()

    def update_switches_thread(self):
        while True:
            self.update_switches()
            time.sleep(1)  # 1초마다 업데이트

    def update_switches(self):
        for label in self.switch_labels:
            label.destroy()

        self.switch_labels = []
        for i in range(1, 5):  # 1부터 4까지 반복
            switch_value = getattr(self.info, f'switch{i}')  # self.info.switch1, self.info.switch2 등을 가져옴
            switch_label = tk.Label(self.switch_frame, text=f"Switch {i}: {switch_value}",
                                    anchor="w", bg="#404040", fg="white", font=("Arial", 8))  # White text color
            switch_label.pack(anchor="w", padx=8)
            self.switch_labels.append(switch_label)

    def start_joystick_update_thread(self):
        joystick_thread = threading.Thread(target=self.update_joystick_thread)
        joystick_thread.daemon = True
        joystick_thread.start()

    def update_joystick_thread(self):
        while True:
            self.update_joystick()
            time.sleep(1)  # 1초마다 업데이트

    def update_joystick(self):
        # Simulate joystick data
        joystick_values_L = {
            'x': self.info.joystick_Left_x,
            'y': self.info.joystick_Left_y,
            'switch': self.info.joystick_Left_val
        }
        joystick_values_R = {
            'x': self.info.joystick_Right_x,
            'y': self.info.joystick_Right_y,
            'switch': self.info.joystick_Right_val
        }

        self.update_joystick_labels(self.joystick_frame_L, "Joystick L", joystick_values_L)
        self.update_joystick_labels(self.joystick_frame_R, "Joystick R", joystick_values_R)

    def update_joystick_labels(self, frame, name, values):
        for label in frame.winfo_children():
            label.destroy()

        joystick_label = tk.Label(frame, text=name, anchor="w", bg="#404040", fg="white", font=("Arial bold", 10))
        joystick_label.pack(anchor="w")

        x_label = tk.Label(frame, text=f"x: {values['x']}", anchor="w", bg="#404040", fg="white", font=("Arial", 8))
        x_label.pack(anchor="w", padx=(8, 0))

        y_label = tk.Label(frame, text=f"y: {values['y']}", anchor="w", bg="#404040", fg="white", font=("Arial", 8))
        y_label.pack(anchor="w", padx=(8, 0))

        switch_label = tk.Label(frame, text=f"switch: {'ON' if values['switch'] else 'OFF'}", anchor="w",
                                bg="#404040", fg="white", font=("Arial", 8))
        switch_label.pack(anchor="w", padx=(8, 0))


if __name__ == "__main__":
    dc_display = class_drone_controller_display(class_Drone_Controller_Information())
