import socket
import time
import cv2
import numpy as np
import socket
import numpy
sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(("192.168.50.52",8080))
def receive_video():
    s = [b'\xff' * 46080 for x in range(5)]

    #fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    #out = cv2.VideoWriter('output.avi', fourcc, 25.0, (640, 480))
    while True:
        picture = b''
        data, addr = sock.recvfrom(46081)
        s[data[0]] = data[1:46081]

        if data[0] == 4:
            for i in range(5):
                picture += s[i]
            frame = numpy.fromstring(picture, dtype=numpy.uint8)
            frame = frame.reshape(240, 320, 3)
            cv2.imshow("frame", frame)
            #out.write(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
            
receive_video()