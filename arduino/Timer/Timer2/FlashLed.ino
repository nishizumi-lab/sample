---------------------------------------------------------------------
#include <MsTimer2.h>            // タイマー割り込みを利用する為に必要なヘッダファイル

// 割り込み時に処理される関数
void flash() {
  static boolean output = HIGH;  // プログラム起動前に１回だけHIGH(1)で初期化
  digitalWrite(13, output);      // 13番ピン(LED)を出力する(HIGH>ON LOW>OFF)
  output = !output;              // outputの内容を反転させる
}

void setup() {
  pinMode(13, OUTPUT);           // 13番ピンを出力に設定(LED)
  MsTimer2::set(500, flash);     // 500ms毎の割り込み、その時に処理する関数flash( )を呼び出し
  MsTimer2::start();             // タイマー割り込み開始
}

// 繰り返し実行される処理
void loop() {
}
