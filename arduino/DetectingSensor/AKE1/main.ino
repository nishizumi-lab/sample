void setup(){
  // LEDに接続した13番ピンを出力ピンに設定
  pinMode(13, OUTPUT);
}

void loop(){
    // 入力ピン(2番)がHIGHならTrue
    boolean pin2 = (digitalRead(2) == HIGH);  

    // 入力ピン(2番)がHIGHならばLED点灯
    if (pin2==true){
        digitalWrite(13, HIGH);
    }
    // 入力ピン(2番)がLOWならばLED消灯
    else{
        digitalWrite(13, LOW);
    }
    // 10ms待機
    delay(10);
}
