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

IS_LEFT = True

GAIN = 20.0
WHITE_BAL = [(79.0, 64.0, 107.0)]

BLACK = (0, 70, -33, 76, -89, 59)

## GPIO
if ('FOR_DEBUGGING' in globals()):
    fm.register(34,fm.fpioa.UART1_TX)
    fm.register(35,fm.fpioa.UART1_RX)
    uart = UART(UART.UART1, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)
else :
    tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
    light = PWM(tim, freq=500000, duty=50, pin=34)
    light.duty(0)


led = ws2812(8,1)

## CONSTANT いじるな！！！
HIGH = 0
LOW = 1

COLOR = [(255, 0, 0), (255, 255, 0), (0, 255, 0)]
LED_OFF = (0, 0, 0)
LED_DETECT = [(10, 10, 0), (0, 10, 10), (10, 0, 10)]

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

    while(True):
        #try:

        led.set_led(0, LED_OFF)
        img = sensor.snapshot()           # 画像を取得

        victim_exists = False


        if ('ENABLE_BINARY' in globals()):
            img.binary([BLACK])


if __name__ == "__main__":
    main()
