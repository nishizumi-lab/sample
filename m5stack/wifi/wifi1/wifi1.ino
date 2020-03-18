#include <WiFi.h>
#include <M5Stack.h>

const char* ssid = "SSID"; // SSID
const char* password = "PASSWORD"; // PASSWORD

WiFiServer server(80);

// Wifiに接続
void setup()
{
    M5.begin();
    delay(100);
    M5.Lcd.setTextSize(3);  // 文字サイズ
    M5.Lcd.println("Connecting");

    // wifi接続開始
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        M5.Lcd.print(".");
    }

    // 接続完了したらIP表示
    M5.Lcd.println("Successed");
    M5.Lcd.println("IP: ");
    M5.Lcd.println(WiFi.localIP());
  
    server.begin();

}


void loop(){

}
