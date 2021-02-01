char data[30];   // 文字列格納用
int i = 0;  // 文字数のカウンタ
      
void setup() {
  Serial.begin(9600);
　　pinMode(13, OUTPUT); // 13番ピンを出力ピンに設定
}
      
void loop() {
  // データ受信したとき
  if (Serial.available()) {
    data[i] = Serial.read();  // 1文字ずつ受信
     // 文字数が30以上 or 終端文字が来たら
    if (i > 30 || data[i] == '\0') {
      data[i] = '\0';         // 末尾に終端文字の挿入
      Serial.write(data);    // 受信文字列を送信
      i = 0;                  // カウンタの初期化
    }
    else { i++; }
  }
}
