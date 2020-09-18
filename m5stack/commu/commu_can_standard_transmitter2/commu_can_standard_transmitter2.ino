#include < M5Stack.h >
#include < mcp_can.h >

#define CAN0_INT 15                              // Set INT to pin 2
MCP_CAN CAN0(12);     // Set CS to pin 10
int cnt = 0;
int CANID = 0x031;
int TYPE = 0; //Standard Format
int DLC = 8;
int timeCycle = 100; // サイクル[ms]

// 最大・最小セル電圧（mv）
int maxCellVoltage = 3000;
int minCellVoltage = 2900;

// 最大・最小セル温度（C）
int maxCellTemp = 26;
int aveCellTemp = 25;
int minCellTemp = 24;


byte datas[8] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};

void init_can();
void test_can();

void setup() {
  M5.begin();
  Serial.begin(9600);
  Serial2.begin(9600, SERIAL_8N1, 16, 17);
  delay(500);
  M5.Lcd.setTextColor(WHITE);
  M5.Lcd.setTextSize(2);
  init_can();
}

void loop() {
  // バイトオーダがMotorola（ビッグエンディアンのとき）
  // 1～2バイト目
  datas[1] = byte( maxCellVoltage >> 8 ); // 上位バイト
  datas[2] = byte( maxCellVoltage );      // 下位バイト
  // 3～4バイト目
  datas[3] = byte( minCellVoltage >> 8 ); // 上位バイト
  datas[4] = byte( minCellVoltage);      // 下位バイト


  /* バイトオーダがintel（リトルエンディアンのとき）
  // 1～2バイト目
  datas[1] = byte( maxCellVoltage );
  datas[2] = byte( maxCellVoltage >> 8 );
  
  // 3～4バイト目
  datas[3] = byte( minCellVoltage );
  datas[4] = byte( minCellVoltage >> 8 );
  */

  // 5～7バイト目
  datas[5] = byte( maxCellTemp );
  datas[6] = byte( aveCellTemp );
  datas[7] = byte( minCellTemp );

  // Aボタンが押されたら最大セル電圧を100mV加算
  if(M5.BtnA.wasPressed())
  {
    maxCellVoltage = maxCellVoltage + 100;
    M5.Lcd.clear();
    M5.Lcd.fillScreen(0x0000);
    init_can();
  }

  // Aボタンが押されたら最大セル電圧を100mV減算
  if(M5.BtnB.wasPressed())
  {
    maxCellVoltage = maxCellVoltage - 100;
    M5.Lcd.clear();
    M5.Lcd.fillScreen(0x0000);
    init_can();
  }

  // Cボタンが押されたら初期化
  if(M5.BtnC.wasPressed())
  {
    M5.Lcd.clear();
    M5.Lcd.fillScreen(0x0000);
    init_can();
  }

  // データ送信
  sendData(CANID, TYPE, DLC, datas);

  M5.Lcd.fillScreen(0x0000);
  M5.update();
}

void init_can(){
  M5.Lcd.setTextSize(2);
  M5.Lcd.setCursor(0, 10);
  M5.Lcd.fillScreen(0x0000);

  // ビットレート500kb/s 
  if(CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ) == CAN_OK) {
  }
  else {
  }
  CAN0.setMode(MCP_NORMAL);   // Change to normal mode to allow messages to be transmitted
  int maxCellVoltage = 3000;
  int minCellVoltage = 2900;
  int maxCellTemp = 26;
  int aveCellTemp = 25;
  int minCellTemp = 24;
}

void sendData(int canId, int flameType, int DLC, byte datas[]){
  
  byte sndStat = CAN0.sendMsgBuf(canId, flameType, DLC, datas);
  String data = "None";
  
  // 送信成功した場合
  if(sndStat == CAN_OK){
    Serial.println("Send Successfully!");
    M5.Lcd.drawString("Send Successfully!", 10, 10);
  } else { // 送信失敗した場合
    Serial.println("Send Error");
    M5.Lcd.drawString("Send Error", 10, 10);
  }

  M5.Lcd.drawString("CAN ID:0x" + String(canId, HEX) + "  (" + String(canId) + ")", 0, 30);

  for(byte i = 0; i < DLC; i++){
    data = String(datas[i], HEX);
    M5.Lcd.drawString("data" + String(i) + ":0x" + data + "  (" + String(datas[i]) + ")", 0, i*20 + 50);
  }
  M5.Lcd.drawString("maxCellVoltage:" + String(maxCellVoltage), 0, 210);
  delay(timeCycle); 
}
