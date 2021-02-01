int do = 262;
int re = 294;
imt mi = 330;

int beat = 300; // 音のビート（長さ）
int pin = 12; // ピン番号（圧電スピーカを接続している）

void setup()
{
}

void loop()
{
     tone(pin, do, beat) ;  // ドを鳴らす
     delay(1000) ;
     tone(pin, re, beat) ;  // レを鳴らす
     delay(1000) ;
     tone(pin, mi, beat) ;  // ミを鳴らす
     delay(1000) ;
}
