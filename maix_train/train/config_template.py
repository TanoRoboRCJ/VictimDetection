# Mobilenet（分類器）
classifier_train_epochs = 40  # 分類器の訓練エポック数
classifier_train_batch_size = 5  # 分類器の訓練バッチサイズ
classifier_train_max_classes_num = 15  # 分類器の訓練で扱う最大クラス数
classifier_train_one_class_min_img_num = 40  # クラスに必要な最小画像数

# Yolo（物体認識）
detector_train_epochs = 40  # Yoloの訓練エポック数
detector_train_batch_size = 5  # Yoloの訓練バッチサイズ（下げると学習が遅いが精度高）
detector_train_learn_rate = 1e-4  # Yoloの訓練学習率
detector_train_max_classes_num = 15  # Yoloの訓練で扱う最大クラス数
detector_train_one_class_min_img_num = 100  # Yoloの訓練で一つのクラスに必要な最小画像数

## 以下はいじるな！！
classifier_train_gpu_mem_require = 2 * 1024 * 1024 * 1024
detector_train_gpu_mem_require = 2 * 1024 * 1024 * 1024

classifier_result_file_name_prefix = "maixhub_classifier_result"
detector_result_file_name_prefix = "maixhub_detector_result"

classifier_train_one_class_max_img_num = 20000
detector_train_one_class_max_img_num = 20000

import os

curr_dir = os.path.abspath(os.path.dirname(__file__))

ncc_kmodel_v3 = os.path.join(curr_dir, "..", "tools", "ncc", "ncc_v0.1/ncc")
sample_image_num = 20  # convert kmodel sample image (for quantizing)

allow_cpu = True
