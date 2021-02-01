import processing.serial.*;
Serial ser;

void setup() {
  // 画面サイズ
  size(400, 400);
  background(0,0,0);
  // シリアル通信の設定（接続するCOMポートと通信速度）
  ser = new Serial(this,"COM5", 9600);
}

void draw() {
}

void mousePressed(){
  // 画面を赤色に
  background(200,0,0);
  // 数値1を送信
  ser.write(1);
}

void mouseReleased(){
  // 画面を黒色に
  background(0,0,0);
  // 数値0を送信
  ser.write(0);
}
