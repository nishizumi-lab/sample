#include <stdio.h>
#include <stdlib.h>

int main()
{
    FILE *fpImage, *fpTxt;
    int i;
    int width, height, data;
    int offset;
	char bmpfilename,j3gfilename;
	printf("Input BMP_filenameÅÑ");scanf("%s",bmpfilename);
	printf("Onput J3G_filenameÅÑ");scanf("%s",j3gfilename);
    fpImage = fopen("bmpfilename", "rb");
    fseek(fpImage, 10, SEEK_SET);
    fread(&offset, 4, 1, fpImage);
    fseek(fpImage, 4, SEEK_CUR);
    fread(&width, 4, 1, fpImage);
    fread(&height, 4, 1, fpImage);

    fseek(fpImage, offset, SEEK_SET);

    fpTxt = fopen("j3gfilename", "w");
    fprintf(fpTxt, "%d %d\n", width, -height);
    i = 0;
    while ((data = fgetc(fpImage)) != EOF) {
        fprintf(fpTxt,"%d%c%d%c", !! (data & 0x10),((i+1)%width) ? ' ' : '\n', !! (data & 0x01),((i+2)%width) ? ' ' : '\n' );
        i+=2;
    }
    fclose(fpTxt);
    fclose(fpImage);

    return EXIT_SUCCESS;
}