import cv2
import socket
import pickle
import struct

# 카메라 초기화
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # 영상 가로 크기 설정
cap.set(4, 480)  # 영상 세로 크기 설정

# 수신 라즈베리파이의 IP 주소와 포트 번호 설정
receiver_ip = "192.168.50.47"
port = 8005

# 소켓 초기화
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    ret, frame = cap.read()

    # 영상을 직렬화하여 전송
    data = pickle.dumps(frame)
    size = len(data)
    max_packet_size = 65507  # UDP 패킷 최대 크기
    num_packets = size // max_packet_size + 1

    # 패킷을 여러 번에 걸쳐 전송
    for i in range(num_packets):
        start = i * max_packet_size
        end = min((i + 1) * max_packet_size, size)
        packet_data = data[start:end]

        # 마지막 패킷인 경우에는 추가 정보를 포함하여 전송
        if i == num_packets - 1:
            packet_data = b"LAST_PACKET" + struct.pack(">HH", i, num_packets) + packet_data
        else:
            packet_data = struct.pack(">HH", i, num_packets) + packet_data

        client_socket.sendto(packet_data, (receiver_ip, port))

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 리소스 정리
cap.release()
cv2.destroyAllWindows()
client_socket.close()