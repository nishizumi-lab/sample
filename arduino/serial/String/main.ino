char input[30];   // 文字列格納用
int i = 0;  // 文字数のカウンタ
	 
void setup() {
  Serial.begin(9600);
}
	 
void loop() {
  
  // データ受信したとき
  if (Serial.available()) {
    input[i] = Serial.read();
     // 文字数が30以上 or 末尾文字
    if (i > 30 || input[i] == '.') {
      // 末尾に終端文字の挿入
      input[i] = '\0';
      // 受信文字列を送信
      Serial.write(input);
      Serial.write("\n");
      // カウンタの初期化
      i = 0;
    }
    else { i++; }
  }
}
