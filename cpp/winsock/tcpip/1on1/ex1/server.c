#include <winsock2.h>

int main(void){
	// 変数宣言
	WSADATA wsa;
	SOCKET soc0, soc;
	struct sockaddr_in addr;
	struct sockaddr_in client;
	char data[] = "UNTAN";
	int client_n, data_n;

	WSAStartup(MAKEWORD(2,0), &wsa); 								// winsockの初期化
	soc0 = socket(AF_INET, SOCK_STREAM, 0); 					// ソケットの作成
	data_n = sizeof(addr);

	addr.sin_family = AF_INET;												// ソケットの設定
	addr.sin_port = htons(12345);
	addr.sin_addr.S_un.S_addr = INADDR_ANY;
	bind(soc0, (struct sockaddr *)&addr, sizeof(addr));
	listen(soc0, data_n); 														// クライアントからの接続待機
	client_n = sizeof(client);
	soc = accept(soc0, (struct sockaddr *)&client, &client_n);	// クライアントからの接続要求を受け付ける
	send(soc, data, data_n, 0); 												// ソケット通信でデータ「UNTAN」をクライアントに送信
	closesocket(soc); 														// TCP接続の終了
	WSACleanup(); 															// winsock2の終了処理

	return 0;
}
