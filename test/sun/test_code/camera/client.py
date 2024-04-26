
import socket
import cv2
import time
UDP_IP = "192.168.50.47"
UDP_PORT = 9505

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,240)
while True:
    ret, frame = cap.read()
    d = frame.flatten()
    s = d.tostring()
    start_time=time.time()
    cv2.imshow("video",frame)
    for i in range(5):
        sock.sendto(bytes([i]) + s[i*46080:(i+1)*46080], (UDP_IP, UDP_PORT))
    end_time=time.time()
    print(end_time-start_time)
 

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break