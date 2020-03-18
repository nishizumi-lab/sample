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
    //M5.Lcd.println(". ");
    WiFiClient client = server.available();  // クライアントのアクセスを待つ
        if (client) {                        // クライアントがサクセスしてきたら
        M5.Lcd.println("Connected.");
        // クライアントからの受信データを保持する文字列
        String currentLine = "";
        // クライアントが接続している間ループ
        while (client.connected()) {
            if (client.available()) {  
                char c = client.read(); 
                // もし改行コードが送られてきたら
                if (c == '\n') {
                    if (currentLine.length() == 0) {
                        // HTTPヘッダーの応答コードとコンテンツタイプ
                        client.println("HTTP/1.1 200 OK");
                        client.println("Content-type:text/html");
                        client.println();

                        // 色を変更するためにリンクを表示
                        client.print("<a href=\"/R\">Red</a><br>");
                        client.print("<a href=\"/B\">here</a><br>");

                        // HTTP応答は、別の空白行で終了しループを抜ける
                        client.println();
                        break;
                    } else {            // if you got a newline, then clear currentLine:
                        currentLine = "";
                    }
                // CR文字でなければcurrentLineに文字を追加
                } else if (c != '\r') {
                    currentLine += c;
                }

                // currentLineが「GET /R」で後方一致すれば赤色背景
                if (currentLine.endsWith("GET /R")) {
                    M5.Lcd.fillScreen(RED);
                }

                // currentLineが「GET /B」で後方一致すれば青色背景
                if (currentLine.endsWith("GET /B")) {
                    M5.Lcd.fillScreen(BLUE);
                }
            }
        }
        // 接続解除
        client.stop();
        M5.Lcd.println("Disconnected.");
    }
    M5.update();
}
