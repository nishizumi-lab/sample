#include <M5Atom.h>

/// @brief グローバル変数
uint8_t r,g,b;
/// @brief Atom Lite 初期化
void setup() 
{
  int i;
  // 本体初期化（UART有効, I2C無効, LED有効）
  M5.begin(true,false,true);
  delay(50);
  
  //LEDを点滅させる。
  for(i=0; i<=1; i++)
  {
    M5.dis.drawpix(0, 0x0000FF);
    delay(500);
    M5.dis.drawpix(0, 0x000000);
    delay(500); 
  }
  r=g=b=0;
}

/// @brief メインループ
void loop() 
{
  CRGB color;//CRGB構造体

  for(r=0; r<0xFF; r++)
  {
    if(b!=0)b--;
    color.setRGB(r,g,b);//CRGBにrgb(8,8,8bits)をセット
    M5.dis.drawpix(0,color);//LEDに表示
    delay(10);
  }

  for(g=0; g<0xFF; g++)
  {
    r--;
    color.setRGB(r,g,b);
    M5.dis.drawpix(0,color);
    delay(10);
  }

  for(b=0; b<0xFF; b++)
  {
    g--;
    color.setRGB(r,g,b);
    M5.dis.drawpix(0,color);
    delay(10);
  }
}
