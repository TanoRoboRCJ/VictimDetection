# Original: https://iotdiary.blogspot.com/2019/07/maixpy-go-mobilenet-transfer-learning.html
# Slightly modified for M5UnitV

import sensor
import image
import KPU as kpu
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(1)
sensor.set_hmirror(1)
sensor.run(1)
labels = ['0', '1']
print(labels)
task = kpu.load("/sd/m.kmodel")
while(True):
    img = sensor.snapshot()

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
        img.draw_string(2, 10, "%s " % (labels[max_index].strip()), 20)
        print("DETECT:" + labels[max_index].strip())
        print(plist.index(pmax))
    else:
        print("NOT DETECT")
a = kpu.deinit(task)
