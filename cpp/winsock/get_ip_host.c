#include <stdio.h>
#include <winsock2.h>

// IPアドレス/ホスト名の取得
int getIpHost(void){
	int i;
	HOSTENT *lpHost; 			//  ホスト情報を格納する構造体
	IN_ADDR inaddr; 				// IPアドレスを格納する構造体
	char szBuf[256], szIP[16]; // ホスト名/IPアドレスを格納する配列

	// ローカルマシンのホスト名を取得する
	gethostname(szBuf, (int)sizeof(szBuf));
	printf("HOST Name : %s\n", szBuf);

	// ホスト情報を取得
	lpHost = gethostbyname(szBuf);
	// IPアドレスを取得
	for(i = 0; lpHost->h_addr_list[i]; i++) {
		memcpy(&inaddr, lpHost->h_addr_list[i], 4);
		strcpy(szIP, inet_ntoa(inaddr));
		printf("IP Adress : %s\n", szIP);
	}

	return 0;
}

int main(void){
	// WinSockの初期化
	WSADATA wsaData;
	// エラー処理
	if (WSAStartup(MAKEWORD(1, 1), &wsaData) != 0) {
		printf("WSAStartup Error\n");
		return -1;
	}
	// IPアドレス/ホスト名の取得 
	getIpHost();
	WSACleanup();
	return 0;
}
