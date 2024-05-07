import spidev
import time

# SPI 장치 설정
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI 포트 0, 장치 0에 연결된 MCP3008에 연결된 경우

# MCP3008을 사용하여 아날로그 값을 디지털로 읽는 함수
def read_adc(channel):
    # MCP3008은 0 ~ 7 사이의 채널을 가지고 있음
    if channel > 7 or channel < 0:
        return -1
    # SPI 데이터 전송
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    # 디지털 값을 계산하여 반환
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

try:
    while True:
        # X 및 Y 축의 아날로그 값을 읽음
        x_value = read_adc(0)
        y_value = read_adc(1)

        # 값을 출력하거나 다른 작업 수행
        print("X 값:", x_value)
        print("Y 값:", y_value)

        # 작업 간 딜레이
        time.sleep(0.1)

except KeyboardInterrupt:
    print("프로그램 종료")
finally:
    spi.close()  # SPI 연결 종료
