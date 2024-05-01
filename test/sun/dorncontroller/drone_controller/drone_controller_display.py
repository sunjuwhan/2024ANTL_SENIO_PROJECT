import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading
from drone_controller.drone_controller_information import *


class VideoStreamThread(threading.Thread):
    def __init__(self, info, display):
        threading.Thread.__init__(self)
        self.info = info
        self.display = display
        self.stopped = False

    def run(self):
        while not self.stopped:
            frame = self.info.frame
            if frame is not None:
                pil_image = Image.fromarray(frame)
                resized_image = pil_image.resize((640, 480))  # Resize the image
                photo = ImageTk.PhotoImage(image=resized_image)
                self.display.update_video_frame(photo)

    def stop(self):
        self.stopped = True


class class_drone_controller_display_master:
    def __init__(self, info):
        self.dc_display = None
        self.info = info

    def run_display(self):
        self.dc_display = class_drone_controller_display(self.info)
        self.video_thread = VideoStreamThread(self.info, self.dc_display)
        self.video_thread.start()


class class_drone_controller_display:
    def __init__(self, info):
        self.info = info
        self.window = tk.Tk()
        self.window.title("Flight Controller Display")
        self.window.geometry("800x480")  # Set window size to 800x480

        # Create a canvas for displaying video
        self.frame_canvas = tk.Canvas(self.window, width=640, height=480)
        self.frame_canvas.grid(row=0, column=0, sticky="nsew")

        # Create frames for other information
        self.info_frame = tk.Frame(self.window, bg="#808080", width=160, height=480, bd=2, relief=tk.SOLID)
        self.info_frame.grid(row=0, column=1, sticky="nsew")

        # Initialize labels for GPS and switch information
        self.gps_frame = tk.Frame(self.info_frame, bg="#404040", bd=2, relief=tk.SOLID)  # Box around GPS info
        self.gps_frame.pack(anchor="w", padx=8, pady=(4, 0), fill=tk.X)

        self.gps_label = tk.Label(self.gps_frame, text="GPS", anchor="w", bg="#404040", fg="white",
                                  font=("Arial bold", 10))  # GPS label
        self.gps_label.pack(anchor="w")

        self.latitude_label = tk.Label(self.gps_frame, text="Latitude: Waiting for data...", anchor="w",
                                       bg="#404040", fg="white", font=("Arial", 8))  # White text color
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

    def update_video_frame(self, photo):
        self.frame_canvas.create_image(0, 0, image=photo, anchor=tk.NW)

    def update_gps(self):
        latitude_text = f"Latitude: {self.info.drone_latitude:.5f}"
        longitude_text = f"Longitude: {self.info.drone_longitude:.5f}"

        self.latitude_label.config(text=latitude_text)
        self.longitude_label.config(text=longitude_text)

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

    # Define a method for stopping the display
    def stop_display(self):
        self.window.destroy()


if __name__ == "__main__":
    info = class_Drone_Controller_Information()
    dc_display = class_drone_controller_display_master(info)
    dc_display.run_display()
