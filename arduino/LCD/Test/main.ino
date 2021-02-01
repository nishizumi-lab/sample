#include <LiquidCrystal.h>  // LCD表示用ライブラリ

//  RS, E, DB4, DB5, DB6, DB7に接続したピン番号
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

// 初期設定
void setup(){
  lcd.begin(16, 2);  //LCD の桁数, 行数
}

// ループ
void loop(){
  lcd.print("Arduino");  // LCDに文字(Arduino)を表示
  lcd.setCursor(0,1);    //カーソルの位置(0桁の1行目)
}
