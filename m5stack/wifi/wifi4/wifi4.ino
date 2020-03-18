#include <WiFi.h>
#include <M5Stack.h>
#include "DHT12.h"
#include <Wire.h> //The DHT12 uses I2C comunication.
#include "Adafruit_Sensor.h"
#include <Adafruit_BMP280.h>

const char* ssid = "SSID"; // SSID
const char* password = "PASSWORD"; // PASSWORD
DHT12 dht12; //Preset scale CELSIUS and ID 0x5c.
Adafruit_BMP280 bme;
float temp = 0;
float hum = 0;
float pressure = 0;
String html = "";

// IP固定する場合
IPAddress ip(192, 168, 128, 20);
IPAddress gateway(192,168, 128, 1);
IPAddress subnet(255, 255, 255, 0);
WiFiServer server(80);

// Wifiに接続
void setup()
{
    WiFi.config(ip, gateway, subnet); //static_ip
    M5.begin();
    Wire.begin();

    while (!bme.begin(0x76)){  
      Serial.println("Could not find a valid BMP280 sensor, check wiring!");
      M5.Lcd.println("Could not find a valid BMP280 sensor, check wiring!");
    }
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

void getData(){
    // 温度の取得
    temp = dht12.readTemperature();

    // 湿度の取得
    hum = dht12.readHumidity();

    // 気圧の取得[hPa = Pa * 0.01]
    pressure = bme.readPressure() * 0.01;
    html ="";
    // グラフを描くHTML
    html += "<html><head><script type='text/javascript' src='https://www.gstatic.com/charts/loader.js'></script>"; 
    html += "<script type='text/javascript'>";     
    html += "google.charts.load('current', {'packages':['gauge']});";   
    html += "google.charts.setOnLoadCallback(drawChart);";   
    html += "function drawChart() {";   
    html += "var data = google.visualization.arrayToDataTable([";     
    html += "['Label', 'Value'],"; 
    html += "['Temp[C].', " + String(temp) + "],";     
    html += "['Hum[%].', " + String(hum) + "],";     
    html += "['Press[hPa]', " + String(pressure) + "],";     
    html += "]);";   
    html += "var options = {width: 400, height: 120,redFrom: 80, redTo: 100, yellowFrom:60, yellowTo: 80,minorTicks: 5};";
    html += "var chart = new google.visualization.Gauge(document.getElementById('chart_div'));";
    html += "chart.draw(data, options);";
    html += "setInterval(function() {";
    html += "data.setValue(0, 1, " + String(temp) + ");";
    html += "chart.draw(data, options);";
    html += "}, 5000);";
    html += "setInterval(function() {";
    html += "data.setValue(1, 1, " + String(hum) + ");";
    html += "chart.draw(data, options);";
    html += "}, 5000);";
    html += "setInterval(function() {";
    html += "data.setValue(2, 1, " + String(pressure) + ");";
    html += "chart.draw(data, options);";
    html += "}, 5000);";
    html += "}";
    html += "</script>";
    html += "</head>";
    html += "<body>";
    html += "<div id='chart_div' style='width: 400px; height: 120px;'></div>";
    html += "</body>";
    html += "</html>";
}

void loop(){
    //M5.Lcd.println(". ");
    WiFiClient client = server.available(); 
        if (client) {
        M5.Lcd.println("New Client."); 
        String currentLine = ""; 
        while (client.connected()) {  
            if (client.available()) {  
                char c = client.read();
                M5.Lcd.write(c); 
                if (c == '\n') { 
                    if (currentLine.length() == 0) {
                        // HTTPヘッダー
                        client.println("HTTP/1.1 200 OK");
                        client.println("Content-type:text/html");
                        client.println();
                        getData();
                        // クライアントにHTMLを返す
                        client.print(html);
                        
                        client.println();
 
                        break;
                    } else {            // if you got a newline, then clear currentLine:
                        currentLine = "";
                    }
                } else if (c != '\r') {
                    currentLine += c; 
                }


                if (currentLine.endsWith("GET /H")) {
                    getData();
                }
                if (currentLine.endsWith("GET /L")) {
                    M5.Lcd.fillScreen(RED);
                }
            }
        }
        // close the connection:
        client.stop();
        M5.Lcd.println("Client Disconnected.");
    }
    M5.update();
}
