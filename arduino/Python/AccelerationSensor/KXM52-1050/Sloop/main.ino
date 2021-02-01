void setup(){
  // シリアルポートを9600 bps[ビット/秒]で初期化
  Serial.begin(9600) ;
}
 
float mapFloat(float x, float iMin, float iMax, float oMin, float oMax) {
  return (x - iMin) * (oMax - oMin) / (iMax - iMin) + oMin;
}
 
void loop(){
  int i ;
  long x , y , z ;
  // 加速度センサの各軸からデータ取得
  x = analogRead(0);
  y = analogRead(1);
  z = analogRead(2);
  // 読み取ったデータを-1から1までの範囲にスケーリング
  float xSinTheta = mapFloat(x, 340, 777, -1, 1);
  float ySinTheta = mapFloat(y, 306, 716, -1, 1);
  // 各値を-1から1までの範囲に制限
  xSinTheta = constrain(xSinTheta,-1,1);
  ySinTheta = constrain(ySinTheta,-1,1);
  // 逆サインの値[rad]を[deg]に変換
  int xdeg = float(asin(xSinTheta) * 180 / PI );
  int ydeg = float(asin(ySinTheta) * 180 / PI );
  // 計算した傾斜角をシリアルモニターに表示
  Serial.println(String(xdeg) + "," + String(ydeg));
  delay(500) ;
}
