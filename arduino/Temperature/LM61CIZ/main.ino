void setup() {
  // シリアル通信の伝送速度
  Serial.begin(9600);
}

void loop() {
  // 変数宣言
  int analog , temp , vt; 
  // アナログ０番ピンからセンサの値を取得(０～５Ｖの電圧を０～１０２３の範囲に変換して取得)
  analog = analogRead(0); 
  // センサの値を電圧に変換(数値を０～１０２３から0~5000mVの範囲に変換)
  vt  = map(analog,0,1023,0,5000);    
  // 電圧を温度に変換(数値を300～1600mvから-30~100度の範囲に変換)
  temp = map(vt,300,1600,-30,100); 
  // 温度をシリアルモニタに表示
  Serial.println(temp);     
  // １秒毎に繰り返す
  delay(1000) ; 
}
