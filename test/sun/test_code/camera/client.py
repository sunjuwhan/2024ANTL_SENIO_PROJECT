import socket
import cv2
from picamera2 import Picamera2
__picam2=Picamera2()
__picam2.preview_configuration.main.size = (640, 480)
__picam2.preview_configuration.main.format = "RGB888"
__picam2.preview_configuration.align()
__picam2.configure("preview")
__picam2.start()
UDP_IP = '192.168.32.1'
UDP_PORT = 9505

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    d = frame.flatten()
    s = d.tostring()

    for i in range(20):
        sock.sendto(bytes([i]) + s[i*46080:(i+1)*46080], (UDP_IP, UDP_PORT))

 

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break