import processing.serial.*;
Serial ser;
 
void setup() {
  // 画面サイズ
  size(400, 400);
  // 画面の背景色(黒)
  background(0,0,0);
  // シリアル通信の設定（接続するCOMポートと通信速度）
  ser = new Serial(this,"COM5", 9600);
}
 
void draw() {
  // 何かデータを受信したら
  if ( ser.available() > 0) {
    background(0,0,0);              // 画面クリア
    String data = ser.readString(); // 文字列を受信
    fill(255,0,0);                  // 文字色
    textSize(50);                   // 文字サイズ
    text(data, 100, 100);           // 画面に文字表示
  }
}

// マウスクリック時の処理
void mousePressed(){
  // 文字列を送信
  ser.write("XYZ\0");
}

// マウスクリック終了時の処理
void mouseReleased(){
  // 文字列を送信
  ser.write("ABC\0");
}
