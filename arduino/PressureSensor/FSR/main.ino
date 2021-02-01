double R1 = 5.1;

void setup(){
  Serial.begin(9600);  // シリアル通信速度
}

void loop(){
  // 変数の宣言
  double Vo, Rf, fg;
  int ain = analogRead(1);
  // アナログ入力値から出力電圧を計算
  Vo = ain * 5.0 / 1024;
  // 出力電圧からFRSの抵抗値を計算
  Rf = R1*Vo / (5.0 - Vo);
  // FRSの抵抗値から圧力センサの荷重を計算
  fg = 880.79/Rf + 47.96;
  // 荷重データをシリアル通信で送る
  Serial.println(fg);
  delay(1000);
}
