#include <Servo.h>

// オブジェクトの宣言
Servo servo1;
// グローバル変数の宣言
char input[4];  // 文字列格納用
int i = 0;      // 文字数のカウンタ
int val = 0;    // 受信した数値
int deg = 0;    // サーボの角度

// 初期設定
void setup() {
  Serial.begin(9600);  // シリアルポートを9600 bps[ビット/秒]で初期化
  servo1.attach(9);     // 制御信号を送る出力ピンの設定
}

// シリアル通信で受信したデータを数値に変換
int serialNumVal(){
  // データ受信した場合の処理
  if (Serial.available()) {
    input[i] = Serial.read();
     // 文字数が3以上 or 末尾文字がある場合の処理
    if (i > 2 || input[i] == '.') {
      input[i] = '\0';      // 末尾に終端文字の挿入
      val = atoi(input);    // 文字列を数値に変換
      Serial.write(input); // 文字列を送信
      Serial.write("\n");
      i = 0;      // カウンタの初期化
    }
    else { i++; }
  }
  return val;
}

// メインループ
void loop() {
  deg = serialNumVal();
  servo1.write(deg);  // deg度まで回転
}
