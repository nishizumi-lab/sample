void setup(){
  // シリアルポートを9600 bps[ビット/秒]で初期化
  Serial.begin(9600) ;
}

void loop(){
  int i ;
  long x , y , z ;
  // 加速度センサの各軸からデータ取得
  x = analogRead(0);
  y = analogRead(1);
  z = analogRead(2);
  // 各軸のデータをそのまま表示
  Serial.print("(X, Y, Z) = (");
  Serial.println(String(x) + ", " + String(y) + ", " + String(z) + ")");
  delay(500) ;
}
