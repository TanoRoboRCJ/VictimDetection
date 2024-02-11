import sensor
import image
from fpioa_manager import *
from Maix import GPIO
from machine import UART
import time
import math
from modules import ws2812

import KPU as kpu

## CONFIG 試合前にここを調整
CALIBRATION = None  ######### 試合時は絶対コメントアウトしない！！！#########
GAIN = 3.0
WHITE_BAL = [(64.0, 81.0, 195.0)]

AREA = 3000

## CONFIG YOLO
BLACK = (22, 62, -40, 15, -36, 11)
LABELS = ['H', 'S', 'U']

anchors = [4.3125, 5.25, 2.46875, 3.09375, 2.03125, 2.5625, 3.0, 3.8124999999999996, 3.5, 4.4375]
model_addr = "/sd/m0211.kmodel"

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
LED_OFF = (0, 0, 0)
LED_DETECT = [(10, 10, 0), (0, 10, 10), (10, 0, 10)]

LETTER = ['R', 'N', 'G']

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
    #sensor.set_hmirror(True)
    #sensor.set_vflip(True)

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
    kpu.init_yolo2(task, 0.3, 0.3, 5, anchors)

    while(True):
        led.set_led(0, LED_OFF)
        img = sensor.snapshot()           # 画像を取得

        #img.rotation_corr(z_rotation = 90)

        victim_exists = False

        # 文字認識
        img.binary([BLACK])
        img.pix_to_ai()
        #try:
        objects = kpu.run_yolo2(task, img)

        global yolo_counter

        yolo_exists = 0
        yolo_label = 0

        if objects:
            for obj in objects:
                obj_width = obj.rect()[2]
                obj_height = obj.rect()[3]

                if (obj_width * obj_height >= AREA):
                    yolo_exists += 1
                    yolo_label = obj.classid()

                    img.draw_rectangle(obj.rect(), color = (255, 0, 0) ,tickness = 5)

        #except:
            #pass

        if yolo_exists == 1:
            yolo_counter += 1
        else :
            yolo_counter = 0

        if yolo_counter >= 3:
            victim_exists = True

            uart.write(LABELS[obj.classid()])
            print(obj.value())
            print(LABELS[obj.classid()])

            led.set_led(0, LED_DETECT[obj.classid()])


        led.display()

        if not victim_exists:
            uart.write('N')
            print('No Victim Detected')



if __name__ == "__main__":
    main()
