#include <M5StickC.h>
#include "RoverC.h"

void setup(){ 
  
  M5.begin();
  RoverC_Init();
}

void loop() {

  // 前進(3秒間)
  moveForward(30);
  delay(3000);

  // 後進(3秒間)
  moveBack(30);
  delay(3000);

  // 左進(3秒間)
  moveLeft(30);
  delay(3000);

  // 右進(3秒間)
  moveRight(30);
  delay(3000);

  // 左旋回(3秒間)
  turnLeft(30);
  delay(3000);

  // 右旋回(3秒間)
  turnRight(30);
  delay(3000);

}
