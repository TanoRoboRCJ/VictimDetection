BLACK = (20, 71, -17, 5, -12, 8)

GAIN = 50.0
WHITE_BAL = [(64.0, 81.0, 231.0)]

import gc
import image
import sensor
import sys
import time
import uos
import os
import KPU as kpu
from fpioa_manager import *
from machine import I2C
from Maix import I2S, GPIO
from modules import ws2812

a = class_ws2812 = ws2812(8,1)
BRIGHTNESS = 0x10

fm.register(18, fm.fpioa.GPIO1)
but_a=GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP) #PULL_UP is required here!

fm.register(19, fm.fpioa.GPIO2)
but_b = GPIO(GPIO.GPIO2, GPIO.IN, GPIO.PULL_UP) #PULL_UP is required here!

def findMaxIDinDir(dirname):
    larNum = -1
    try:
        dirList = uos.listdir(dirname)
        for fileName in dirList:
            currNum = int(fileName.split(".jpg")[0])
            if currNum > larNum:
                larNum = currNum
        return larNum
    except:
        return 0


def initialize_camera():
    while 1:
        try:
            sensor.reset() #Reset sensor may failed, let's try some times
            break
        except:
            time.sleep(0.1)
            continue
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA) #QVGA=320x240
    sensor.set_auto_gain(False, gain_db = GAIN, gain_db_ceiling = GAIN)
    sensor.set_auto_whitebal(False, rgb_gain_db = WHITE_BAL[0])
    sensor.run(1)


def RGB_LED():
    a = class_ws2812.set_led(0,(0,BRIGHTNESS,0))
    a = class_ws2812.display()
    time.sleep(0.5)
    a = class_ws2812.set_led(0,(0,0,0))
    a = class_ws2812.display()


initialize_camera()

currentDirectory = 1

if "sd" not in os.listdir("/"):
    print("Error: Cannot read SD Card")

try:
    os.mkdir("/sd/train")
except Exception as e:
    pass

try:
    os.mkdir("/sd/vaild")
except Exception as e:
    pass

try:
    currentImage = max(findMaxIDinDir("/sd/train/" + str(currentDirectory)), findMaxIDinDir("/sd/vaild/" + str(currentDirectory))) + 1
except:
    currentImage = 0
    pass

isButtonPressedA = 0
isButtonPressedB = 0

try:
    while(True):
        img = sensor.snapshot()
        img.binary([BLACK])
        if but_a.value() == 0 and isButtonPressedA == 0:
            if currentImage <= 30 or currentImage > 35:
                try:
                    if str(currentDirectory) not in os.listdir("/sd/train"):
                        try:
                            os.mkdir("/sd/train/" + str(currentDirectory))
                        except:
                            pass
                    photo = img.save("/sd/train/" + str(currentDirectory) + "/" + str(currentImage) + ".jpg", quality=95)
                    print("ok Class" + str(currentDirectory) + " -> " + str(currentImage) + "/35")
                    RGB_LED()
                except:
                    print("Error: Cannot Write to SD Card")
                    time.sleep(1)
            else:
                try:
                    if str(currentDirectory) not in os.listdir("/sd/vaild"):
                        try:
                            os.mkdir("/sd/vaild/" + str(currentDirectory))
                        except:
                            pass
                    photo = img.save("/sd/vaild/" + str(currentDirectory) + "/" + str(currentImage) + ".jpg", quality=95)
                    print("ok Class" + str(currentDirectory) + " -> " + str(currentImage) + "/35")
                    RGB_LED()
                except:
                    print("Error: Cannot Write to SD Card")
                    time.sleep(1)
            currentImage = currentImage + 1
            isButtonPressedA = 1

        if but_a.value() == 1:
            isButtonPressedA = 0

        if but_b.value() == 0 and isButtonPressedB == 0:
            currentDirectory = currentDirectory + 1
            if currentDirectory == 11:
                currentDirectory = 1
            currentImage = max(findMaxIDinDir("/sd/train/" + str(currentDirectory)), findMaxIDinDir("/sd/vaild/" + str(currentDirectory))) + 1
            print("ok Class" + str(currentDirectory) + " -> " + str(currentImage) + "/35")
            isButtonPressedB = 1

        if but_b.value() == 1:
            isButtonPressedB = 0

except KeyboardInterrupt:
    pass
