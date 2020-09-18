#include < M5Stack.h >
#include < mcp_can.h >

#define CAN0_INT 15                              // Set INT to pin 2
MCP_CAN CAN0(12);     // Set CS to pin 10
int cnt = 0;
int CANID = 0x100;
int TYPE = 0; //Standard Format
int DLC = 8;

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
  byte datas[8] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
  if(cnt > 30){
    byte datas[8] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};  
    cnt = 0;
  }
  else{
    for(byte i = 0; i < DLC; i++){
      datas[i] = datas[i] + cnt;
    }
    cnt++;
  }
  if(M5.BtnA.wasPressed())
  {
    M5.Lcd.clear();
    M5.Lcd.fillScreen(0x0000);
    init_can();
  }

  sendData(CANID, TYPE, DLC, datas);
  delay(1000);
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

  M5.Lcd.drawString("CAN ID:0x" + String(canId, HEX) + "  (" + String(canId) + ")", 0, 40);

  for(byte i = 0; i < DLC; i++){
    data = String(datas[i], HEX);
    M5.Lcd.drawString("data" + String(i) + ":0x" + data + "  (" + String(datas[i]) + ")", 10, i*20 + 60);
  }
    
  delay(200);   // send data per 200ms
}
