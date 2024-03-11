mkdir -p tools/ncc/ncc_v0.1/
cd tools/ncc/ncc_v0.1/
wget https://github.com/kendryte/nncase/releases/download/v0.1.0-rc5/ncc-linux-x86_64.tar.xz
tar Jxf ncc-linux-x86_64.tar.xz\
mkdir -p datasets_img

docker pull tensorflow/tensorflow:2.11.0-gpu
docker compose up -d --build
docker run --gpus all -it --name python3_nvidia -v `pwd`:/root/maix_train tensorflow/tensorflow:2.11.0-gpu /bin/bash