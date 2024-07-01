import matplotlib.pyplot as plt

# ログから損失の値を抽出
train_loss = []
val_loss = []
epochs = []

with open("out/train_log.log", "r") as log_file:
    for line in log_file:
        if "epoch" in line and "end" in line:
            # epoch番号の部分のみを抽出して整数に変換
            epoch_str = line.split("epoch")[1].split("end")[0].strip()
            try:
                epoch_num = int(epoch_str)
                epochs.append(epoch_num)
                train_loss.append(float(line.split("'loss':")[1].split(",")[0]))
                val_loss.append(float(line.split("'val_loss':")[1].split(",")[0]))
            except ValueError:  # 変換できない場合はスキップ
                continue

plt.figure(figsize=(10, 6))

# linewidth引数を指定して線の太さを調整 (例: 2)
plt.plot(epochs, train_loss, label='Training Loss', linewidth=2)  
plt.plot(epochs, val_loss, label='Validation Loss', linewidth=2)  

plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Model Loss')
plt.legend()
plt.grid(True)
plt.show()