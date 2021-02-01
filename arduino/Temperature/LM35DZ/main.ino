float a_in;          // アナログ入力値(0〜203)
float temp_c = 0;  // 摂氏値( ℃ )

void setup(){
  Serial.begin(9600);  // シリアル通信速度
}

void loop(){
  // アナログピンから計測値を取得(0〜203)
  a_in = analogRead(0);
  // 入力値を摂氏に換算
  temp_c = ((5 * a_in) / 1024) * 100;
  // 改行しながら出力
  Serial.println( temp_c );
  // 1000ms待機
  delay(1000);
}
