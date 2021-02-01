void setup(){ 
    /* シリアル通信の準備 */
    Serial.begin(9600);  
    /* 13番ピン(LED)を出力ピンに設定 */
    pinMode(13, OUTPUT);
}

void loop(){
    /* Cdsセンサー(0番ピン)の明るさを取得 */
    int light = analogRead(0);
    /* 明るさ（0～1023）をLEDの輝度（0～255）に変換 */
    int led_light = map(light, 0, 1023, 255, 0);
    /* センサーの明るさ, LEDの輝度をシリアル通信でPCに送信 */
    Serial.print(light+","+led_light);
    /* 13番のLEDを点灯 */
    analogWrite(13, led_light);
    /* 100?待機 */
    delay(100);
}
