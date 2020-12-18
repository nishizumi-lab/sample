#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int main()
{
    int *map;
    int x=21, y=21, hx=1,hy=1, gx, gy;  // 迷路の大きさ, 主人公とゴールの位置
    int i, j, flag, cmd;
    gx;
    gy=y-2;
    clock_t start,end; // 時間計測用
    start = clock();   // 開始時間を記録
    srand((unsigned)time(NULL));//乱数の種
    map = (int *) malloc( x*y * sizeof(int) );
    if (map==NULL){ printf("メモリ不足エラー\n"); return -1; }

    // 全てを見えない壁(1)にする 
    for (j=0; j<y; j++){ for (i=0; i<x; i++) map[x*j+i]=1; }
    // 奇数番地は床(0)にする
    for (j=1; j<y-1; j++){ for (i=1; i<x-1; i++) 
        if ( i%2!=0|| j%2!=0) map[x*j+i]=0;
    }
    // 迷路生成（棒倒し法）
    for (j=2; j<y-2; j+=2){ for (i=2; i<x-2; i+=2) 
        if ( rand()%2 ) map[x*(j+1)+i]=1; else map[x*j+i+1]=1;
    }

    printf("迷路ゲームスタート！\n");
    while(1){
        // メモリ内の迷路を表示
        for (j=0; j<y; j++){ 
          for (i=0; i<x; i++){
            if (map[x*j+i]==3) printf("#");
            else if (i==hx && j==hy) printf("o");
                 else if (i==gx && j==gy) printf("G");
                    else printf(" ");
            
          }  printf("\n");
        }
        printf("【移動キー】 A:下 S:上 D:左 F:右\n");
		printf(">");
		// Enterキー無しの1文字入力
        cmd = getch(); 
		// 画面クリア
		system("cls");
		// キー入力に応じて自機を移動
        if (cmd=='e'){ flag=-1; break;}
        if (cmd=='a' && hy<y && map[x*(hy+1)+hx]%2!=1) hy+=1;
        if (cmd=='s' && hy>0 && map[x*(hy-1)+hx]%2!=1) hy-=1;
        if (cmd=='d' && hx>0 && map[x*hy+(hx-1)]%2!=1) hx-=1;
        if (cmd=='f' && hx<x && map[x*hy+(hx+1)]%2!=1) hx+=1;
        // 自分の周囲だけ見えるようにする（見える壁(3)にする）
        if (map[x*(hy+1)+hx]==1) map[x*(hy+1)+hx]=3 ;
        if (map[x*(hy-1)+hx]==1) map[x*(hy-1)+hx]=3;
        if (map[x*hy+(hx-1)]==1) map[x*hy+(hx-1)]=3;
        if (map[x*hy+(hx+1)]==1) map[x*hy+(hx+1)]=3;
        if (hx==gx && hy==gy){flag=1; break;} // ゴール到着
    }

    if (flag==1){
        end = clock();
        printf("ゲームクリア\n プレイ時間は%.2f秒です\n",(double)(end-start)/CLOCKS_PER_SEC);
    }
    else printf("ゲームを中断します\n");

    // メモリ内にある迷路をすべて表示する
    for (j=0; j<y; j++){ 
        for (i=0; i<x; i++){
            if (map[x*j+i]%2==1) printf("#");
            else if (i==hx && j==hy) printf("o");
                 else if (i==gx && j==gy) printf("G");
                    else printf(" ");
            
          }  printf("\n");
    }
    return 0;
}