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
