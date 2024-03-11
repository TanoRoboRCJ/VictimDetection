import sensor
import image
import KPU as kpu
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((0, 0, 224, 224))
sensor.run(1)

CALIBRATION = None
ENABLE_BINARY = None

labels = ["LTR_H", "LTR_S", "LTR_U", "N"]

GAIN = 53.0
WHITE_BAL = [(67.0, 64.0, 131.0)]

BLACK = (4, 34, -51, 35, -50, 35)



print(labels)
task = kpu.load("/sd/m.kmodel")

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

    sensor.set_auto_gain(False, gain_db = GAIN, gain_db_ceiling = GAIN)
    sensor.set_auto_whitebal(False, rgb_gain_db = WHITE_BAL[0])
    sensor.skip_frames(time = 2000)

def main():
    init ()
    calibration()

    while(True):
        img = sensor.snapshot()
        img.binary([BLACK])

        img2 = img.resize(224, 224)

        img2.pix_to_ai()
        fmap = kpu.forward(task, img2)

        plist = fmap[:]
        print("plist:" + str(plist) )
        pmax = max(plist)
        print("pmax:" + str(pmax) )

        if pmax >=0.7 and pmax <=1:
            max_index = plist.index(pmax)
            print("DETECT:" + labels[max_index].strip())
        else:
            print("NOT DETECT")


if __name__ == "__main__":
    main()

