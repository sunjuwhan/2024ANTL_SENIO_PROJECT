import socket
import numpy
import cv2

UDP_IP = "192.168.50.47"
UDP_PORT = 9505
import time
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

s = [b'\xff' * 46080 for x in range(5)]

#fourcc = cv2.VideoWriter_fourcc(*'DIVX')
#out = cv2.VideoWriter('output.avi', fourcc, 25.0, (640, 480))
start_time=time.time()
while True:
    picture = b''
    data, addr = sock.recvfrom(46081)
    s[data[0]] = data[1:46081]
    if data[0] == 5:
        for i in range(5):
            picture += s[i]

        frame = numpy.fromstring(picture, dtype=numpy.uint8)
        frame = frame.reshape(240, 320, 3)
        cv2.imshow("frame", frame)
        #out.write(frame)
        end_time=time.time()
        print(end_time-start_time)
        start_time=time.time()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break