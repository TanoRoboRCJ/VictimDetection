# Original: https://iotdiary.blogspot.com/2019/07/maixpy-go-mobilenet-transfer-learning.html
# Slightly modified for M5UnitV

import sensor
import image
import KPU as kpu
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((0, 0, 224, 224)
sensor.run()

labels = ['H', 'S', 'U']
BLACK = (0, 22, -32, 26, -34, 26)
print(labels)
task = kpu.load("/sd/m.kmodel")

while(True):
    img = sensor.snapshot()
    img.binary([BLACK])

    # モデル入力用の画像サイズに変換
    img2 = img.resize(224, 224)
    # K210のRGB565 データを推論処理用のメモリブロック ​​RGB888 にコピー

    img2.pix_to_ai()
    # モデルの実行
    fmap = kpu.forward(task, img2)

    plist = fmap[:]
    print("plist:" + str(plist) )
    pmax = max(plist)
    print("pmax:" + str(pmax) )
#   Avoiding Exception for index of undef result.
    if pmax >=0 and pmax <=1:
        max_index = plist.index(pmax)
        print("DETECT:" + labels[max_index].strip())
    else:
        print("NOT DETECT")
a = kpu.deinit(task)