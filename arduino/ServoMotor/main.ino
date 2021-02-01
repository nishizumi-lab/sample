#include <Servo.h>

Servo servo1;

void setup() {
  // 制御信号を送る出力ピンの設定
  servo1.attach(9);
}

void loop() {
  int deg=0;  // 初期の回転角
  // 0-180度回転
  for (deg=0; deg<180; deg++) {
    servo1.write(deg);  // deg度まで回転
    delay(20);          // 20ms待機
  }
  // 180-0度回転
  for (deg=180; deg>0; deg--) {
    servo1.write(deg);  // deg度まで回転
    delay(20);          // 20ms待機
  }
}
