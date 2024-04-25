import cv2
import socket
import pickle
import struct

# 수신 라즈베리파이의 IP 주소와 포트 번호 설정
receiver_ip = "192.168.50.47"
port = 8005

# 소켓 초기화
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((receiver_ip, port))

# 영상을 표시할 창 생성
cv2.namedWindow("Received", cv2.WINDOW_NORMAL)

received_data = b""
num_packets = None

while True:
    # 데이터 수신
    data, addr = server_socket.recvfrom(65507)

    # 첫 번째 패킷에서 총 패킷 수를 가져옴
    if num_packets is None:
        num_packets = struct.unpack(">H", data[:2])[0]

    # 수신된 데이터를 저장
    received_data += data[2:]

    # 모든 패킷을 수신했을 때 영상 표시
    if len(received_data) >= num_packets:
        # 직렬화된 데이터를 디코딩하여 영상 표시
        frame = pickle.loads(received_data[:num_packets])
        cv2.imshow("Received", frame)
        received_data = received_data[num_packets:]
        num_packets = None

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 리소스 정리
cv2.destroyAllWindows()
server_socket.close()