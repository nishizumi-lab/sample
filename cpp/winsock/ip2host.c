#include<stdio.h>
#include<winsock2.h>

int main(void) {
	// 変数宣言
	WSADATA wsaData;
	struct in_addr addr;
	struct hostent *host;
	
	WSAStartup(MAKEWORD(2,0), &amp;wsaData);	// 初期化
	addr.S_un.S_addr = inet_addr("127.0.0.1");		// IPアドレスをバイナリ値に変換
	// IPアドレスからホスト名を取得
	host = gethostbyaddr((const char *)&amp;addr.S_un.S_addr, sizeof(addr.S_un.S_addr), AF_INET);
	printf("%s\n", host-&gt;h_name);					// ホスト名を表示
	WSACleanup();

	return 0;
}
