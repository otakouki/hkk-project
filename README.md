# hkk-project
[githubからソースコード取ってくる](https://github.com/otakouki/hkk-project)（zipを解凍しその中に入る）
## 必要備品
* esp32 １台以上
* rfid reader １つ
* rfid card 複数枚
* 超音波センサ(HC-SR04) 1つ
* raspberry pi １台（今回使ったものraspberry pi 4B）
* raspberry pi cameraかwebカメラ　１台
* nfcが使えるスマートフォン １台

## esp32での準備
### RFIDの配線
| rfidのPIN | esp32のGPIOPIN |
| :--------: | :--------: |
| 3V3      | 3V3      |
| RST      | GPIO25   |
| GND      | GND      |
| MISO     | GPIO19   |
| MOSI     | GPIO23   |
| SCK      | GPIO18   |
| CS       | GPIO4    |

### HC-SR04の配線
| HC-SR04のPIN | esp32のGPIOPIN |
|:------------:| :----------: |
| 5V         | VOUT      |
| TRIG       | GPIO17    |
| ECHO       | GPIO16    |
| GND        | GND       |

### Arduino IDE libraries
* ArduinoJson
* HttpClient
* MFRC522

### Arduino IDE コード

rfidのコード(rfid.ino)
* esp32にrfid.inoを書き込む
hc-sr04のコード(hc-sr04.ino)

* esp32にhc-sr04を書き込む

## raspberry piでの設定

## installしたライブラリ
*  tensorflow-2.7.0
*  mtcnn
*  numpy
*  opencv-python
*  libatlas-base-dev 
*  libqt4-test 
*  libjasper1 
*  libhdf5-dev
*  qt4-dev-tools 
*  qt4-doc 
*  qt4-qtconfig 
*  libqt4-test

1. [GitHubから tensorflow-2.7.0-cp37-none-linux_armv7l.whlを取ってくる](https://github.com/otakouki/hkk-project/releases/tag/tensorflow)
2. tensorflow-2.7.0-cp37-none-linux_armv7l.whlをraspberry piの/home/pi/に入れる 

### package install
ホームディレクトリ上で(/home/pi/)
``` shell=
cd
sudo apt install -y libatlas-base-dev libqt4-test libjasper1 libhdf5-dev
sudo apt-get install -y qt4-dev-tools qt4-doc qt4-qtconfig libqt4-test
pip3 ./tensorflow-2.7.0-cp37-none-linux_armv7l.whl
pip3 install mtcnn
pip3 install numpy
pip3 install numpy --upgrade
pip3 install opencv-python
```

### パッケージインストール後の作業
* 新規で「/home/pi/embedded/」ディレクトリ作成
* 「/home/pi/embedded/」にgitからとてきたembedded内のpython fileを全て入れる
* カメラモジュールの場合設定でカメラ有効化する（Webカメラの場合しなくても良い）
* embeddedディレクトリに入り```python3 main.py```で実行する

## local fast api
### 事前準備
* gitからダウンロードしたhkk_project_apiの中に入る
* README.txtに書いてある通りに進める。
```shell=
cd hkk_project_api
uvicorn main:app --reload　--host ipアドレス(学内Wi-Fiなら10.200.5.73だと他の部分を変えなくても良い) --port 8000
```

## Androidの作業
* NFCの使えるスマートフォンに[HKK_PROJECT.zip]を解凍しインストールする
