#include <M5Stack.h>
#include "DHT12.h"
#include <Wire.h> //The DHT12 uses I2C comunication.
#include "Adafruit_Sensor.h"
#include <Adafruit_BMP280.h>

DHT12 dht12; //Preset scale CELSIUS and ID 0x5c.
Adafruit_BMP280 bme;

void setup() {
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
}

void loop() {
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

    delay(100);
} 
