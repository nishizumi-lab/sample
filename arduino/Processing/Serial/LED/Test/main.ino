void setup(){
  // シリアルポートを9600 bps[ビット/秒]で初期化
  Serial.begin(9600);
}
  
void loop(){
  if(Serial.available()>0){
    int input = Serial.read();    // シリアル通信で数値を受信
    if(input == 1 ){
      digitalWrite(13, HIGH);  // LED点灯
    }
    else{
      digitalWrite(13, LOW);   // LED消灯
    }
  }
}
