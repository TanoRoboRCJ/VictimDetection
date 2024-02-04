import sensor
import image
from fpioa_manager import *
from Maix import GPIO
from machine import UART
import time
import math
from modules import ws2812

## CONFIG 試合前にここを調整
CALIBRATION = None  ######### 試合時は絶対コメントアウトしない！！！#########
GAIN = 3.0
WHITE_BAL = [(76.0, 64.0, 136.0)]

RED = (66, 79, 9, 56, -17, 15)
YELLOW = (87, 97, -22, -8, 16, 46)
GREEN = (57, 76, -19, -1, -23, -8)

BLACK = (26, 60, -8, 7, -23, -7)

AREA = 4000

## GPIO
fm.register(18, fm.fpioa.GPIO1)
btn_a = GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)
fm.register(19, fm.fpioa.GPIO2)
btn_b = GPIO(GPIO.GPIO2, GPIO.IN, GPIO.PULL_UP)

fm.register(34,fm.fpioa.UART1_TX) #逆じゃね？
fm.register(35,fm.fpioa.UART1_RX)
uart = UART(UART.UART1, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)

led = ws2812(8,1)

## CONSTANT いじるな！！！
HIGH = 0
LOW = 1
COLOR = [(255, 0, 0), (255, 255, 0), (0, 255, 0)]
LETTER = ['R', 'N', 'G']

def calibration():
    if not ('CALIBRATION' in globals()):
        sensor.set_auto_gain(True)
        sensor.set_auto_whitebal(True)

        while(1):
            img = sensor.snapshot()

            try :
                print("GAIN = ", end="")
                print(sensor.get_gain_db())
                print("WHITE_BAL = [", end="")
                print(sensor.get_rgb_gain_db(),end="")
                print("]")
            except:
                print("Point the camera at the white surface.")

def init():
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)

    sensor.set_auto_gain(False, gain_db = GAIN, gain_db_ceiling = GAIN)
    sensor.set_auto_whitebal(False, rgb_gain_db = WHITE_BAL[0])

    led.set_led(0, (100,100,100))
    led.display()

    sensor.skip_frames(time = 2000)

    led.set_led(0, (0, 0, 0))
    led.display()

def main():
    init ()
    calibration()

    while(True):
        led.set_led(0, (0, 0, 0))
        img = sensor.snapshot()           # 画像を取得

        #img.draw_rectangle(0, 0, int(math.sqrt(AREA)), int(math.sqrt(AREA)))

        victim_exists = False

        # 色認識
        for i in range(3):
            threshold = [RED, YELLOW, GREEN]
            blobs = img.find_blobs([threshold[i]])

            if blobs:
                for b in blobs:
                    if (b[2] * b[3] >= AREA):
                        victim_exists = True

                        img.draw_rectangle(b[0:4], color = COLOR[i], thickness=3)
                        img.draw_cross(b[5], b[6])

                        uart.write(LETTER[i])
                        print(LETTER[i])

                        led.set_led(0, (5, 5, 5))

        if not victim_exists:
            uart.write('N')
            print('N')

        led.display()


if __name__ == "__main__":
    main()
