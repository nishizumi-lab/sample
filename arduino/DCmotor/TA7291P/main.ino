// 出力ピンの定義
const int motor1A = 7;
const int motor1B = 8;
const int motor1P = 9;

// 初期設定
void setup(){
  pinMode(motor1A,OUTPUT); // 信号用ピン
  pinMode(motor1B,OUTPUT); // 信号用ピン
}

// 繰り返し
void loop(){
    // 回転
    digitalWrite(motor1A,HIGH);
    digitalWrite(motor1B,LOW);
    analogWrite(motor1P,100); 
    delay(2000);
    // 静止
    digitalWrite(motor1A,LOW);
    digitalWrite(motor1B,LOW);
    delay(2000);
}
