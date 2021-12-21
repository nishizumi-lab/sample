#ifndef _ROVERC_H_
#define _ROVERC_H_

#include <M5StickC.h>

#define ROVER_ADDRESS	0X38

void rovercInit(void);	//sda  0     scl  26

void moveForward(int8_t speed);

void moveBack(int8_t speed);

void turnLeft(int8_t speed);

void turnRight(int8_t speed);

void moveLeft(int8_t speed);

void moveRight(int8_t speed);

void moveStop(int8_t speed);

void sendIic(uint8_t registerNum, uint8_t speed);

#endif
