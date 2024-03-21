mkdir -p tools/ncc/ncc_v0.1/
cd tools/ncc/ncc_v0.1/
wget https://github.com/kendryte/nncase/releases/download/v0.1.0-rc5/ncc-linux-x86_64.tar.xz
tar Jxf ncc-linux-x86_64.tar.xz\

docker compose up -d --build
sh start_env.sh