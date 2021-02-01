void setup() {
  pinMode(13, OUTPUT); // 13番ピンを出力ピンに設定
}

void loop() {
  digitalWrite(13, HIGH);   // 13番ピンでHigh(5V出力)
  delay(1000);              // 1000ms待機
  digitalWrite(13, LOW);    // 13番ピンにLow(0V出力)
  delay(1000);              // 1000ms待機
}
