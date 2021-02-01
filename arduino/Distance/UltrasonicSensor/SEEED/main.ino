void setup() {
  Serial.begin(9600) ;   // シリアル通信速度（9600bps）
}

void loop() {
     int cm ;   
     distance = calcDistance(7) ;  // 7番ピンからセンサーの値（距離データ）を取得
     Serial.print(distance) ;      // 距離をシリアルモニタに表示(cm単位)
     Serial.println("cm") ;
     delay(1000) ;                 // 1000ms後に繰り返す
}
// 超音波センサーから取得したセンサ値を距離に換算
int calcDistance(int pin)
{
     long t ;
     int ans ;   
     // 超音波センサーに5usのパルスを出力
     pinMode(pin, OUTPUT) ;             // ピンを出力モード
     digitalWrite(pin, LOW) ;
     delayMicroseconds(2) ;
     digitalWrite(pin, HIGH) ;
     delayMicroseconds(5) ;
     digitalWrite(pin, LOW) ;
     // センサーからの反射パルスを受信する
     pinMode(pin, INPUT) ;              // ピンを入力モード
     t = pulseIn(pin, HIGH) ;           // パルス幅の時間を測る
     if (t < 18000) {                   // ３ｍ以内から距離計算
          ans = (t / 29) / 2 ;          // 往復なので２で割る
     } else ans = 0 ;                   // 3m以上なら0を返す    
     return ans ;
}
