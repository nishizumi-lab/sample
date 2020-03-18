#include <stdio.h>
#include <winsock2.h>

int main(void){
	// 変数の宣言
	WSADATA wsa;
	struct sockaddr_in server;
	SOCKET soc;
	char buffer[32];															// バッファ格納用(受信データ)
	int n;

	WSAStartup(MAKEWORD(2,0), &wsa); 								// winsockの初期化
	soc = socket(AF_INET, SOCK_STREAM, 0); 						// ソケットの作成
	server.sin_family = AF_INET;
	server.sin_port = htons(12345);
	server.sin_addr.S_un.S_addr = inet_addr("127.0.0.1");			// 接続するサーバーのIPアドレスを指定
	connect(soc, (struct sockaddr *)&server, sizeof(server)); 	// サーバに接続
	memset(buffer, 0, sizeof(buffer)); 									// サーバからデータを受信
	recv(soc, buffer, sizeof(buffer), 0);
	printf("%s", buffer);														// 受信バッファ(データ)の表示
	WSACleanup(); 															// ソケット廃棄(終了)	
	
	return 0;
}
