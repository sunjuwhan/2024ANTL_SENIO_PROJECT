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

while True:
    # 데이터 수신
    data, addr = server_socket.recvfrom(65535)

    # 패킷에서 추가 정보를 추출
    header = data[:10]
    is_last_packet = data.startswith(b"LAST_PACKET")
    if is_last_packet:
        packet_index, num_packets = struct.unpack(">HH", header[10:])
        data = data[10:]
    else:
        packet_index, num_packets = struct.unpack(">HH", header)
        data = data[10:]

    # 모든 패킷을 수신하면 영상 표시
    if packet_index == 0:
        received_data = data
    else:
        received_data += data

    # 모든 패킷을 수신했을 때 영상 표시
    if packet_index == num_packets - 1:
        # 직렬화된 데이터를 디코딩하여 영상 표시
        frame = pickle.loads(received_data)
        cv2.imshow("Received", frame)
        received_data = b""

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 리소스 정리
cv2.destroyAllWindows()
server_socket.close()