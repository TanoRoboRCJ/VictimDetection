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

## CONFIG 試合前にここを調整
CALIBRATION = None      ######### 試合時は絶対コメントアウトしない！！！#########
ENABLE_BINARY = None    ######### 試合時は絶対コメントアウトしない！！！#########
FOR_DEBUGGING = None

IS_LEFT = False
IS_LEFT = True

GAIN = 20.0
WHITE_BAL = [(79.0, 64.0, 107.0)]

RED = (38, 87, 29, 71, 20, 62)
YELLOW = (47, 100, -18, 22, 32, 81)
GREEN = (39, 76, -48, -15, -10, 32)

BLACK = (2, 67, -44, 29, -44, 27)
AREA = 3000

SENSIBILITY = [0.90, 0.90, 0.82]

## CONFIG YOLO
#LABELS = ['U', 'S', 'H']
LABELS = ['S', 'H', 'U'] #45, 47モデルの例外
anchors = [2.25, 2.78, 2.62, 3.28, 3.25, 4.09, 4.12, 5.03, 1.78, 2.41]
model_addr = "/sd/model-100645.kmodel"

## GPIO
if ('FOR_DEBUGGING' in globals()):
    fm.register(34,fm.fpioa.UART1_TX)
    fm.register(35,fm.fpioa.UART1_RX)
    uart = UART(UART.UART1, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)
else :
    tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
    light = PWM(tim, freq=500000, duty=50, pin=34)
    light.duty(70)


led = ws2812(8,1)

## CONSTANT いじるな！！！
HIGH = 0
LOW = 1

COLOR = [(255, 0, 0), (255, 255, 0), (0, 255, 0)]
LED_OFF = (0, 0, 0)
LED_DETECT = [(10, 10, 0), (0, 10, 10), (10, 0, 10)]

LETTER = ['R', 'Y', 'G']

## GLOBAL
yolo_counter = 0

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
    sensor.set_windowing((0, 0, 224, 224))

    if IS_LEFT:
        sensor.set_hmirror(True)
        sensor.set_vflip(True)

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

    task = kpu.load(model_addr)
    kpu.init_yolo2(task, 0.82, 0.0001, 5, anchors)

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

                        if ('FOR_DEBUGGING' in globals()):
                            uart.write(LETTER[i])
                        print(LETTER[i])

                        led.set_led(0, (5, 5, 5))

        if victim_exists:
            led.display()
            continue

        ######### 文字認識 #########
        if ('ENABLE_BINARY' in globals()):
            img.binary([BLACK])

        img.pix_to_ai()

        yolo_objects = kpu.run_yolo2(task, img)

        global yolo_counter

        yolo_exists = 0
        yolo_label = 0

        if yolo_objects:
            for obj in yolo_objects:
                obj_width = obj.rect()[2]
                obj_height = obj.rect()[3]

                if (obj_width * obj_height >= AREA):
                    if (obj.value() >= SENSIBILITY[obj.classid()]):
                        yolo_exists += 1
                        yolo_label = obj.classid()
                        img.draw_rectangle(obj.rect(), color = (255, 0, 0) ,tickness = 5)


        if yolo_exists == 1:
            yolo_counter += 1
        else :
            yolo_counter = 0

        if yolo_counter >= 2:
            victim_exists = True

            if ('FOR_DEBUGGING' in globals()):
                uart.write(LABELS[obj.classid()])

            print(obj.value())
            print(LABELS[obj.classid()])

            led.set_led(0, LED_DETECT[obj.classid()])

        #########

        led.display()

        if not victim_exists:
            if ('FOR_DEBUGGING' in globals()):
                uart.write('N')
            print('No Victim Detected')

        #except:
            #pass


if __name__ == "__main__":
    main()
