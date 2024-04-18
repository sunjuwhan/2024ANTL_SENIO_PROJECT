import cv2
import numpy
import socket
AP_IP="192.168.32.1"
PORT=8005
MY_IP="192.168.50.52"
class class_Drone_Controller_VideoStreamer:
    def __init__(self):
        self.ip_address = MY_IP    #내 ip   ap로 
        self.port = PORT  #고정
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.ip_address, self.port))

    def receive_video(self):
        s = [b'\xff' * 11520 for x in range(20)]

        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        out = cv2.VideoWriter('output.avi', fourcc, 25.0, (640, 480))
        while True:
            picture = b''

            data, addr = self.socket.recvfrom(46081)
            s[data[0]] = data[1:46081]

            if data[0] == 19:
                for i in range(20):
                    picture += s[i]

                frame = numpy.fromstring(picture, dtype=numpy.uint8)
                frame = frame.reshape(480, 640, 3)
                cv2.imshow("frame", frame)
                out.write(frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break

    def run_VideoStreamer(self):
        self.receive_video()