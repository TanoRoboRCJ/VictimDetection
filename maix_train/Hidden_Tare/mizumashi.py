import os
from PIL import Image

def rotate_images_in_folder(folder_path):
    # フォルダ内のすべてのファイルを取得
    for filename in os.listdir(folder_path):
        # ファイルが画像であることを確認
        print(filename)
        if filename.endswith('.jpg') or filename.endswith('.png'):
            # 画像を開く
            img = Image.open(os.path.join(folder_path, filename))
            # 90, 180, 270度で画像を回転させて保存
            for angle in [90, 180, 270]:
                rotated_img = img.rotate(angle)
                rotated_img.save(os.path.join(folder_path, f'rotated_{angle}_{filename}'))

# フォルダパスを指定
folder_path = './LTR_U'
rotate_images_in_folder(folder_path)