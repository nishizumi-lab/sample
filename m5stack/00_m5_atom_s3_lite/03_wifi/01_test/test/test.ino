#include <WiFi.h>
// #include <M5AtomS3.h>

const char* ssid = "SSID"; // SSID
const char* password = "PASSWORD"; // PASSWORD

WiFiServer server(80);

void setup() {
  // M5.begin(true, true, false, false);
  Serial.begin(9600);
  Serial.print("connect start...");
  // wifi接続開始
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Attempting to connect...");
  }

  // 接続完了したらIP表示
  Serial.println("Su/Users/github/sample/m5stack/06_env_pro/02_serial/sample01/sample01.inoccessed");
  Serial.println("IP: ");
  Serial.println(WiFi.localIP());
  
  server.begin();
}

void loop() {

  delay(1000);
}