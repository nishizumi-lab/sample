#include < M5Stack.h >
#include < mcp_can.h >

long unsigned int canId;
unsigned char len = 0;
unsigned char datas[8];

#define CAN0_INT 15
MCP_CAN CAN0(12);

// 初期設定
void setup() {
  M5.begin();
  Serial.begin(9600);
  Serial2.begin(9600, SERIAL_8N1, 16, 17);
  delay(5000);
  M5.Lcd.setTextColor(WHITE);
  init_can();
}

// CANモジュールの初期化
void init_can(){
  M5.Lcd.setTextSize(2);
  M5.Lcd.setCursor(0, 10);
  delay(500);

  // MCP2515の初期化に成功した場合（ビットレート500kb/s ）
  if(CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ) == CAN_OK){
  }// 初期化に失敗した場合
  else{
  }
  // MCP2515を通常モードに設定
  CAN0.setMode(MCP_NORMAL);
  
  // CAN0_INTを入力ピンに設定（受信用）
  pinMode(CAN0_INT, INPUT);
}

// CAN通信データを受信
void receiveData(){
  String data = "None";
  // CAN0_INTピンがLowなら、受信したバッファを読み込む
  if(!digitalRead(CAN0_INT))
  {
    CAN0.readMsgBuf(&canId, &len, datas);

    // CAN IDを16進数/10進数で表示
    M5.Lcd.drawString("CAN ID:0x" + String(canId, HEX) + "  (" + String(canId & 0x1FFFFFFF) + ")", 0, 0);

    // データ（8byte）を16進数/10進数で表示
    for(byte i = 0; i < len; i++){
      data = String(datas[i], HEX);
      M5.Lcd.drawString("data" + String(i) + ":0x" + data + "  (" + String(datas[i]) + ")", 10, i*20 + 30);
    }

    delay(1000);
    M5.Lcd.fillScreen(0x0000);
  }
}

void loop() {
  receiveData();
  M5.update();
}
