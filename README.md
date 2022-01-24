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
```arduino=
/*
   This ESP32 code is created by esp32io.com
   This ESP32 code is released in the public domain
   For more detail (instruction and wiring diagram), visit https://esp32io.com/tutorials/esp32-rfid-nfc
*/
#include <SPI.h>
#include <MFRC522.h>
#include <WiFi.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>
//接続先のSSODとパスワード 学内CampusuIOT
const char ssid[] = "CampusIoT-WiFi";
const char passwd[] = "0b8b413f2c0fa6aa90e085e9431abbf1fa1b2bd2db0ecf4ae9ce4b2e87da770c";
WiFiServer server(80);
const int pinLed1 = 2;
const int pinLed2 = 4;
const int pinLed3 = 26;
#define SS_PIN  5  // ESP32 pin GIOP5 
#define RST_PIN 25 // ESP32 pin GIOP25
String ch1;
String ch2;
String ch3;
String ch4;
String uid1;
String uid2;
String uid3;
String uid4;
String uid;
MFRC522 rfid(SS_PIN, RST_PIN);
const int capacity = JSON_OBJECT_SIZE(2);
StaticJsonDocument<capacity> json_request;
char buffer[255];
const char *host = "http://10.200.5.73:8000/api/attendances";
void setup() {
  
  Serial.begin(115200);
  SPI.begin(); // init SPI bus
  rfid.PCD_Init(); // init MFRC522
  // WiFi接続シーケンス
  WiFi.begin(ssid, passwd);
  Serial.print("WiFi connecting...");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(100);
  }
  Serial.print(" connected. ");
  Serial.println(WiFi.localIP());
  server.begin();
  pinMode(pinLed1, OUTPUT);
  pinMode(pinLed2, OUTPUT);
  pinMode(pinLed3, OUTPUT);
  Serial.println("Tap an RFID/NFC tag on the RFID-RC522 reader");
}
void loop() {
  digitalWrite(pinLed2, LOW);
        digitalWrite(pinLed3, LOW);
        digitalWrite(pinLed1, HIGH);
  if (rfid.PICC_IsNewCardPresent()) { // new tag is available
    if (rfid.PICC_ReadCardSerial()) { // NUID has been readed
      MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
      Serial.print("RFID/NFC Tag Type: ");
      Serial.println(rfid.PICC_GetTypeName(piccType));
      // print UID in Serial Monitor in the hex format
      Serial.print("UID:");
      ch1 = String((rfid.uid.uidByte[0] < 0x10) ? "0" : "");
      uid1 = String(rfid.uid.uidByte[0], HEX);
      ch2 = String((rfid.uid.uidByte[1] < 0x10) ? "0" : "");
      uid2 = String(rfid.uid.uidByte[1], HEX);
      ch3 = String((rfid.uid.uidByte[2] < 0x10) ? "0" : "");
      uid3 = String(rfid.uid.uidByte[2], HEX);
      ch4 = String((rfid.uid.uidByte[3] < 0x10) ? "0" : "");
      uid4 = String(rfid.uid.uidByte[3], HEX);
      uid = ch1 + uid1 + ch2 + uid2 + ch3 + uid3 + ch4 + uid4;
      uid.toUpperCase();
      Serial.println(uid);
      json_request["uid"] = uid;
      serializeJson(json_request, Serial);
      Serial.println("");
      serializeJson(json_request, buffer, sizeof(buffer));
      HTTPClient http;
      http.begin(host);
      http.addHeader("Content-Type", "application/json");
//      delay(10);
      int status_code = http.POST((uint8_t*)buffer, strlen(buffer));
//      delay(10);
      Serial.printf("status_code=%d\r\n", status_code);
      if ( status_code == 200 ) {
        digitalWrite(pinLed1, LOW);
        digitalWrite(pinLed3, LOW);
        digitalWrite(pinLed2, HIGH);
        
        Stream* resp = http.getStreamPtr();
        DynamicJsonDocument json_response(255);
        deserializeJson(json_response, *resp);
        serializeJson(json_response, Serial);
        Serial.println("");
      }else {
        digitalWrite(pinLed1, LOW);
        digitalWrite(pinLed2, LOW);
        digitalWrite(pinLed3, HIGH);
      }
      http.end();
      //delay(10);
      Serial.println();
      rfid.PICC_HaltA(); // halt PICC
      rfid.PCD_StopCrypto1(); // stop encryption on PCD
    }
  }
}
```
* esp32にrfid.inoを書き込む
hc-sr04のコード(hc-sr04.ino)
```arduino=
//必要なライブラリー
#include <WiFi.h>
#include "ArduinoJson.h"
#include <HTTPClient.h>
//接続先のSSODとパスワード 学内CampusuIOT
//const char ssid[] = "CampusIoT-WiFi";
const char ssid[] = "ECCcomp4";
const char passwd[] = "0b8b413f2c0fa6aa90e085e9431abbf1fa1b2bd2db0ecf4ae9ce4b2e87da770c";
const char* apiServer = "http://192.168.0.32:8000/api/notification";
WiFiServer server(80);
#define Trigger_Pin 17
#define Echo_Pin 16
int V = 340;//音速
void setup() {
  Serial.begin(115200);
  // WiFi接続シーケンス
  WiFi.begin(ssid, passwd);
  Serial.print("WiFi connecting...");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(100);
  }
  Serial.print(" 接続できた！ ");
  Serial.println(WiFi.localIP());
  server.begin();
  pinMode(Trigger_Pin, OUTPUT);
  pinMode(Echo_Pin, INPUT);
  digitalWrite(Trigger_Pin, LOW);
}
//Send Trigger pulse
void sendTrigger() {
  digitalWrite(Trigger_Pin, HIGH);
  delayMicroseconds(10);
  digitalWrite(Trigger_Pin, LOW);
}
void loop() {
  sendTrigger();
  while (!digitalRead(Echo_Pin)) {
  }
  unsigned long t1 = micros();
  while (digitalRead(Echo_Pin)) {
  }
  unsigned long t2 = micros();
  unsigned long t = t2 - t1;
  Serial.print(V * t / 20000);
  Serial.println("cm");
  int num = V * t / 20000;
  if (num == 1400) {
    if ((WiFi.status() == WL_CONNECTED)) {
      HTTPClient http;
      //APIサーバに接続開始
      http.begin(apiServer);
      //HTTP Requestを作成する
      int httpCode = http.GET();
      //返り値を確認する
      if (httpCode > 0) {
        //レスポンスを文字列として取得する
        String payload = http.getString();
        //正常の場合は200
        //Serial.println(httpCode);
        //一回レスポンスを表示する
        Serial.println(payload);
        //jsonに変換するためにメモリを確保
        DynamicJsonDocument doc(1024);
        //payloadをjson objectに変換する
        deserializeJson(doc, payload);
        JsonObject obj = doc.as<JsonObject>();
        //その中のbpi.JPYを取り出す
        JsonObject result = obj[String("bpi")][String("JPY")];
        //ビットコインの価格を取り出す、同時に文字列に変換しておく
        String rate = result[String("rate")];
        //表示する
        Serial.println(rate);
      }
      else {
        Serial.println("HTTP request エラー");
        return;
      }
      //リソースを解放する
      http.end();
      delay(3000);
    }
  }
}
```
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
