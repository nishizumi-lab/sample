#include <M5Stack.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "DHT12.h"
#include <Wire.h> //The DHT12 uses I2C comunication.
#include "Adafruit_Sensor.h"
#include <Adafruit_BMP280.h>

DHT12 dht12; //Preset scale CELSIUS and ID 0x5c.
Adafruit_BMP280 bme;

// Wi-FiのSSID
char *ssid = "XXXXXX";

// Wi-Fiのパスワード
char *password = "XXXXXX";

// GoogleスプレッドシートのデプロイされたURLを設定
const char* published_url = "https://script.google.com/macros/s/XXXXXX/exec";

void setup_serial(){
  Serial.begin(115200);
  while (!Serial) continue;
}

void setup_wifi(){
  
  Serial.println("Connecting to ");
  Serial.print(ssid);

  // WiFi接続性改善のため、いったん切断
  WiFi.disconnect();
  delay(500);

  // WiFi開始
  WiFi.begin(ssid, password);
 
  // Wi-Fi接続待ち
  while (WiFi.status() != WL_CONNECTED){
    delay(500);
    M5.Lcd.print(".");
  }

  // WiFi接続成功メッセージの表示
  Serial.println("\nWiFi Connected.");
  M5.Lcd.setCursor(10, 40);
  M5.Lcd.setTextColor(WHITE);
  M5.Lcd.setTextSize(2);
  M5.Lcd.println("WiFi Connected.");

  // M5StackのIPアドレスを表示
  M5.Lcd.print("IP address: ");
  M5.Lcd.println(WiFi.localIP());
  
  M5.Lcd.print("Please push button A \n");
}

void setup(){

    M5.begin();
    Wire.begin();

    M5.Lcd.setBrightness(10);

    Serial.println(F("ENV Unit(DHT12 and BMP280) test..."));

    while (!bme.begin(0x76)){  
      Serial.println("Could not find a valid BMP280 sensor, check wiring!");
      M5.Lcd.println("Could not find a valid BMP280 sensor, check wiring!");
    }
    // LCD初期化
    M5.Lcd.clear(BLACK);
    M5.Lcd.println("ENV Unit test...");

  setup_serial();

  // Wi-Fi処理の開始
  setup_wifi();

}

void loop(){

  StaticJsonDocument<500> doc;
  char pubMessage[256];

  M5.update();
  
    // 温度の取得
    float tmp = dht12.readTemperature();

    // 湿度の取得
    float hum = dht12.readHumidity();

    // 気圧の取得[hPa = Pa * 0.01]
    float pressure = bme.readPressure() * 0.01;

    // 温度、湿度、気圧をシリアル通信で送信
    Serial.printf("Temperatura: %2.2f*C  Humedad: %0.2f%%  Pressure: %0.2fPa\r\n", tmp, hum, pressure);

    // LCDに温度、湿度、気圧を表示
    M5.Lcd.setCursor(0, 0); // カーソル
    M5.Lcd.setTextColor(WHITE, BLACK);  // 色
    M5.Lcd.setTextSize(4);  // 文字サイズ
    M5.Lcd.printf("Temp:%2.1f \nHumi:%2.0f%% \nPres:%2.0fhPa \n", tmp, hum, pressure);

    // JSONメッセージの作成
    JsonArray tmpValues = doc.createNestedArray("temp");
    tmpValues.add(String(tmp));
    
    JsonArray humValues = doc.createNestedArray("humid");
    humValues.add(String(hum));

    JsonArray pressValues = doc.createNestedArray("pressure");
    pressValues.add(String(pressure));

    serializeJson(doc, pubMessage);

    // HTTP通信開始
    HTTPClient http;

    Serial.print(" HTTP通信開始　\n");
    http.begin(published_url);
   
    Serial.print(" HTTP通信POST　\n");
    int httpCode = http.POST(pubMessage);
   
    if(httpCode > 0){
      M5.Lcd.printf(" HTTP Response:%d\n", httpCode);
   
      if(httpCode == HTTP_CODE_OK){
        M5.Lcd.println(" HTTP Success!!");
        String payload = http.getString();
        Serial.println(payload);
      }
    }else{
      M5.Lcd.println(" FAILED");
      Serial.printf("　HTTP　failed,error: %s\n", http.errorToString(httpCode).c_str());
    }
   
    http.end();

    delay(3600000);
   
}
