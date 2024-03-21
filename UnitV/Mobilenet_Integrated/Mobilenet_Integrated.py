import sensor
import image
from fpioa_manager import *
from Maix import GPIO
from machine import UART
from machine import Timer,PWM
import time
import math
from modules import ws2812
from board import board_info

import KPU as kpu

# CONFIG 試合前にここを調整
CALIBRATION = None      ######### 試合時は絶対コメントアウトしない！！！#########
ENABLE_BINARY = True    ######### 試合時は絶対コメントアウトしない！！！#########

IS_LEFT = False
#IS_LEFT = True

GAIN = 40.0
WHITE_BAL = [(75.0, 64.0, 108.0)]

RED = (29, 62, 32, 92, -2, 51)
YELLOW = (57, 90, -26, 16, 31, 79)
GREEN = (48, 76, -41, -11, -26, 7)

BLACK = (0, 55, -87, 85, -86, 86)
AREA = 2500

SENSIBILITY = [0.90, 0.90, 0.82]

## CONFIG MOBILENET
LABELS = ["H", "S", "U", "N"]
model_addr = "/sd/0320.kmodel"

## GPIO
fm.register(34,fm.fpioa.UART1_TX)
fm.register(35,fm.fpioa.UART1_RX)
uart = UART(UART.UART1, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)

led = ws2812(8,1)

## CONSTANT いじるな！！！
HIGH = 0
LOW = 1

COLOR = [(255, 0, 0), (255, 255, 0), (0, 255, 0)]
LED_OFF = (0, 0, 0)
LED_DETECT = [(10, 10, 0), (0, 10, 10), (10, 0, 10)]

LETTER = ['R', 'Y', 'G']

## GLOBAL
mobilenet_counter = 0

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
    sensor.reset(dual_buff=True)
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_windowing((0, 0, 224, 224))
    sensor.set_contrast(2)

    if IS_LEFT:
        sensor.set_hmirror(True)
        sensor.set_vflip(True)

    sensor.set_auto_gain(False, gain_db = GAIN, gain_db_ceiling = GAIN)
    sensor.set_auto_whitebal(False, rgb_gain_db = WHITE_BAL[0])

    #sensor.set_auto_whitebal(True)

    led.set_led(0, (100,100,100))
    led.display()

    sensor.skip_frames(time = 2000)

    led.set_led(0, (0, 0, 0))
    led.display()

def main():
    init ()
    calibration()

    task = kpu.load(model_addr)

    while(True):
        #try:

        led.set_led(0, LED_OFF)
        img = sensor.snapshot()           # 画像を取得

        victim_exists = False

        ######### 色認識 #########
        for i in range(3):
            threshold = [RED, YELLOW, GREEN]
            try:
                blobs = img.find_blobs([threshold[i]])
            except:
                pass

            if blobs:
                for b in blobs:
                    if (b[2] * b[3] >= AREA):
                        victim_exists = True

                        img.draw_rectangle(b[0:4], color = COLOR[i], thickness=3)
                        img.draw_cross(b[5], b[6])

                        uart.write(LETTER[i])
                        print(LETTER[i])

                        led.set_led(0, (5, 5, 5))

        if victim_exists:
            led.display()
            continue

        ######### 文字認識 #########
        if ('ENABLE_BINARY' in globals()):
            img.binary([BLACK])
            #img.invert()
            img.pix_to_ai()

        fmap = kpu.forward(task, img)

        plist = fmap[:]
        pmax = max(plist)
        max_index = plist.index(pmax)

        global mobilenet_counter
        mobilenet_exists = False

        if pmax >=0.5 and pmax <=1 and not LABELS[max_index] == "N":
            max_index = plist.index(pmax)
            mobilenet_exists = True
            print("DETECT:" + LABELS[max_index])

        if mobilenet_exists == True:
            mobilenet_counter += 1
        else :
            mobilenet_counter = 0

        if mobilenet_counter >= 1:
            victim_exists = True

            uart.write(LABELS[max_index])

            print(pmax)
            print(LABELS[max_index])

            led.set_led(0, LED_DETECT[max_index])

        led.display()

        if not victim_exists:
            uart.write('N')
            if (LABELS[max_index] == "N"):
                print('MODEL_N:', pmax)
            else :
                print('No Victim Detected')

        #except:
            #pass


if __name__ == "__main__":
    main()
