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
