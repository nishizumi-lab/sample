#include <stdio.h>
#include <winsock.h>

int main(void){
    // 変数の宣言
    int soc; 
    int nBytesRecv;
    char recv_buf[65536];
    char request[256];
	char ServerName[] = "networks.blog.jp"; 				// 接続先のホスト名
	char Html[] = "";    											// 目的のhtmlのパス
	unsigned short Port = 80;                        			//ポート番号
    unsigned long ulIPAddress;                  				// サーバのIPアドレス格納変数

    // WinSock初期化
    WORD wVersionRequested = MAKEWORD(1, 1);    // 使用するWinSockのバージョン要求
    WSADATA wsaData;                            				// WinScokデータ構造体
    PHOSTENT phostent;                          				// サーバの情報を指すポインタ
    SOCKADDR_IN     addrServer;							// サーバのアドレス

    WSAStartup(wVersionRequested, &wsaData);
    if(atexit((void (*)(void))(WSACleanup))){    			// 終了時にWinSockのリソースを解放
        printf("atexit(WSACleanup)失敗\n");
        return -1;
    }

    soc = socket(AF_INET, SOCK_STREAM, 0);

    ulIPAddress = inet_addr(ServerName);        			// サーバーのIPアドレスを取得
    // inet_addr()関数が失敗　ServerNameがホスト名であった場合下の処理に入る
    if(ulIPAddress == -1){
        if( (phostent = gethostbyname(ServerName)) != NULL){
            ulIPAddress = *((unsigned long *)(phostent->h_addr));
        }else{
            printf("ホストアドレス取得失敗です\n");
            printf("エラー%dが発生しました\n", WSAGetLastError());
            closesocket(soc);                    	// ソケットの破棄
            return -1;            
        }
    }

    // サーバへ接続
    addrServer.sin_family       = AF_INET;                            	// アドレスファミリの指定
    addrServer.sin_addr.s_addr  = ulIPAddress;                        // サーバのIPアドレスの指定
    addrServer.sin_port         = htons((unsigned short)Port); 	// ポート番号の指定
    if(connect(soc, (LPSOCKADDR)&addrServer, sizeof(addrServer)) == SOCKET_ERROR){
        printf("サーバへの接続失敗です\n");
        printf("エラー%dが発生しました\n", WSAGetLastError());
        closesocket(soc);                        // ソケットの破棄
        return -1;
    }


    sprintf(request, "GET http://%s%s HTTP/1.0\r\n\r\n", ServerName, Html);
    if( send(soc, request, sizeof(request), 0) == SOCKET_ERROR){
        printf("サーバへの送信失敗です\n");
        printf("エラー%dが発生しました\n", WSAGetLastError());
        shutdown(soc, 2);                        // 送受信を無効にする
        closesocket(soc);                        // ソケットの破棄
        return -1;
    }

	// 受信が終わるまで繰り返す
    while(1){    
        nBytesRecv = recv(soc, recv_buf, sizeof(recv_buf), 0);
        if(nBytesRecv == SOCKET_ERROR){
            printf("サーバからの受信失敗です\n");
            printf("エラー%dが発生しました\n", WSAGetLastError());
            break;
        }else if(nBytesRecv == 0){ 			// 受信終わり
            break;
        }
        recv_buf[nBytesRecv] = '\0'; 			// 受信バッファの後ろにNULLを付加する
        printf("%s",recv_buf);                  	// 画面に受信したhtmlを表示
    }

    shutdown(soc,2);                            // 送受信を無効にする
    closesocket(soc);                           // ソケットの破棄

    return 0;
}
