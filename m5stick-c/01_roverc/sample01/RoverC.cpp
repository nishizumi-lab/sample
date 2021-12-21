
#include "RoverC.h"

// 初期化
void rovercInit(void)    //sda  0     scl  26
{
    Wire.begin(0,26,100);
}

// I2C通信で送信
void sendIic(uint8_t registerNum, uint8_t speed)
{
  // 指定したアドレスのI2Cスレーブに対して送信処理を開始
  Wire.beginTransmission(ROVER_ADDRESS); // 0X38
  // 1バイト(レジスタ)をキューへ送信
  Wire.write(registerNum);
  // 1バイト(速度)をキューへ送信
  Wire.write(speed);
  // 指定したアドレスのI2Cスレーブに対して送信処理を終了
  Wire.endTransmission();
}

// 前進
void moveForward(int8_t speed)
{
  // 4輪とも同じ速度で前進方向に回転
  sendIic(0x00, speed ); // 前輪(左)
  sendIic(0x01, speed ); // 前輪(右)
  sendIic(0x02, speed ); // 後輪(左)
  sendIic(0x03, speed ); // 後輪(右)
}

// 後進
void moveBack(int8_t speed)
{
  // 4輪とも同じ速度で後進方向に回転
  sendIic(0x00, (-1) * speed );
  sendIic(0x01, (-1) * speed );
  sendIic(0x02, (-1) * speed );
  sendIic(0x03, (-1) * speed );
}

// 左旋回
void turnLeft(int8_t speed)
{
  // 前輪(左)と後輪(左)は同じ速度で前進方向に回転
  // 前輪(右)と後輪(右)は同じ速度で後進方向に回転
  sendIic(0x00, speed );
  sendIic(0x01, (-1) * speed );
  sendIic(0x02, speed );
  sendIic(0x03, (-1) * speed );
}

// 右旋回
void turnRight(int8_t speed)
{
  // 前輪(左)と後輪(左)は同じ速度で後進方向に回転
  // 前輪(右)と後輪(右)は同じ速度で前進方向に回転
  sendIic(0x00, (-1) * speed );
  sendIic(0x01, speed );
  sendIic(0x02, (-1) * speed );
  sendIic(0x03, speed );
}

// 左進
void moveLeft(int8_t speed)
{
  // 前輪(左)と後輪(右)は同じ速度で後進方向に回転
  // 前輪(右)と後輪(左)は同じ速度で前進方向に回転
  sendIic(0x00, (-1) * speed );
  sendIic(0x01, speed );
  sendIic(0x02, speed );
  sendIic(0x03, (-1) * speed );
}

// 右進
void moveRight(int8_t speed)
{
  // 前輪(左)と後輪(右)は同じ速度で前進方向に回転
  // 前輪(右)と後輪(左)は同じ速度で後進方向に回転
  sendIic(0x00, speed );
  sendIic(0x01, (-1) * speed );
  sendIic(0x02, (-1) * speed );
  sendIic(0x03, speed );
}

// 停止
void moveStop(int8_t speed)
{
  sendIic(0x00, 0 );
  sendIic(0x01, 0 );
  sendIic(0x02, 0 );
  sendIic(0x03, 0 );
}
