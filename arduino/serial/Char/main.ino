void setup(){
  // シリアルポートを9600 bps[ビット/秒]で初期化
  Serial.begin(9600);
}
 
void loop(){
   
  int input;
  // シリアルポートより1文字読み込む
  input = Serial.read();
  
  if(input != -1 ){
    // 受け取った文字を送信
    Serial.write(input);
    Serial.write("\n");
  }
}
