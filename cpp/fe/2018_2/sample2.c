#include <stdio.h>

#define InName "C:\\github\\sample\\cpp\\fe\\2018_2\\sample2.c"/* 入力ファイル名 */

void Swap(int *x, int *y)
{
    int temp;
    temp = *x;  /* xが指す変数の値を退避 */
    *x = *y;    /* yが指す変数の値をxが指す変数に代入 */
    *y = temp;  /* tempに退避しておいたxが指す変数の値をyが指す変数に代入*/
}

int main() {
    FILE   *infile;
    int    chr, i;
    long   cnt;
    long   freq[256];   /* freq[i]: 文字コード i の出現回数 */
    int    ih, ix, code[256];

    for (chr = 0; chr <= 255; chr++)
        freq[chr] = 0;


    infile = fopen(InName, "rb");
    cnt = 0;
    while ((chr = fgetc(infile)) != EOF) {
        cnt++;
        freq[chr]++;
    }
    fclose(infile);
    printf(" %10ld bytes processed\n\n", cnt);
    for (i = 0; i <= 64; i++) {
        for (chr = i; chr <= i + 192 ; chr += 64 ) {
            if ((0x20 <= chr) && (chr <= 0x7E))
                printf(" %10ld %02X '%c'", freq[chr], chr, chr);
            else
            printf(" %10ld %02X", freq[chr], chr);
         }
        printf("\n");
    }

    // ここから機能追加
    for(i = 0; i <=255; i++)
        code[i] = i;
    ih = 256;
    while(ih > 0) {
        ix = 0;
        for(i = 0; i < ih; i++) {
            if(freq[i] < freq[i+1]) {
                Swap(&code[i], &code[i+1]);
                Swap(&freq[i], &freq[i+1]);
                ix = i;
            }
        }
        ih--;
    }

    printf("\n");

    for (i = 0; i < 64; i++) {
        for (chr = i; chr <= i + 192 ; chr += 64 ) {
            if ((0x20 <= code[chr]) && (code[chr] <= 0x7E))
                printf(" %10ld %02X '%c'", freq[chr], code[chr], code[chr]);
            else
                printf(" %10ld %02X     ", freq[chr], code[chr]);
        }
        printf("\n");
    }
    return 0;
}