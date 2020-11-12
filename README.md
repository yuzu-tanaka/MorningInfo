# MorningInfo

## 環境構築

### 各種モジュールのインストール
sudo apt-get update && sudo apt-get install python3-dev python3-pillow -y
sudo apt install build-essential
sudo apt install python3-rpi.gpio python3-numpy python3-bs4 -y

### rpi-rgb-led-matrix のセットアップ

cd ~/

git clone https://github.com/hzeller/rpi-rgb-led-matrix.git

cd rpi-rgb-led-matrix/
make -C examples-api-use

cd bindings/python/
make build-python PYTHON=$(which python3)
sudo make install-python PYTHON=$(which python3)


### MorningInfo のセットアップ
cd ~/

#### 標準サウンドモジュールの停止
sudo nano /boot/config.txt

```
# Enable audio (loads snd_bcm2835)
#dtparam=audio=on　　コメントアウト
```

#### プログラムの取得
git clone https://github.com/yuzu-tanaka/MorningInfo.git

cd MorningInfo

sudo cp ./morninginfo.service /etc/systemd/system/
sudo systemctl enable morninginfo.service
sudo systemctl start morninginfo.service
