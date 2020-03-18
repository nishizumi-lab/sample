#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <math.h>
 
typedef int (*NumReader)(FILE*);
typedef int Matrix33[3][3];
 
struct FilterData {
        Matrix33 x;
        Matrix33 y;
};
 
struct PgmData {
        int width;
        int height;
        int max;
        int *data; /* by malloc() */
};
 
struct PgmData* new_pgm_from_file( FILE* fp );
struct PgmData* new_pgm_from( struct PgmData* src );
struct PgmData* copy_pgm_from( struct PgmData* src );
int skipComment(FILE* binaryIn);
void write_pgm( FILE* fOut, struct PgmData* pgm, int isBinary );
int mult_mat(Matrix33 a, Matrix33 b);
void obtain_mat( struct PgmData* pgm, int x, int y, Matrix33 out );
void set_pgm_value(struct PgmData* pgm, int x, int y, int val);
struct PgmData* apply_filter(
        struct FilterData* m, struct PgmData* pgm, double level );
struct PgmData* apply_lapl(
        struct FilterData* m, struct PgmData* pgm, double level );
 
 
static struct FilterData g_grad =
 { { {0,0,0},{0,1,-1},{0,0,0}, },
   { {0,0,0},{0,0,1}, {0,-1,0} } };
 
static struct FilterData g_roberts =
 { { {0,0,0},{0,1,0},{0,0,-1}, },
   { {0,0,0},{0,1,0},{0,-1,0}, } };
 
static struct FilterData g_sobel =
 { { {1,0,-1}, {2,0,-2}, {1,0,-1} },
   { {1,2,1}, {0,0,0}, {-1,-2,-1} } };
 
static struct FilterData g_lapl =
 { { {0,1,0}, {1,4,1}, {0,1,0} },
   { {0,1,0}, {1,4,1}, {0,1,0} }};
 
struct PgmData* apply_filter(
        struct FilterData* m, struct PgmData* pgm, double level
){
        Matrix33 tmp = {{0,0,0}};
        struct PgmData* out;
        out = new_pgm_from(pgm);
 
        if( out == NULL ){ return NULL; }
 
        int i,j,x,y;
        for( i = 0; i < pgm->width; i++ ){
                for( j = 0; j < pgm->height; j++ ){
                        obtain_mat(pgm,i,j,tmp);
                        x = mult_mat(m->x,tmp);
                        y = mult_mat(m->y,tmp);
                        set_pgm_value(
                                out,i,j,
                                (int)(sqrt( (x*x)+(y*y) ) * level) 
                        );
                }
        }
        return out;
}
 
void set_pgm_value(struct PgmData* pgm, int x, int y, int val){
        if( 0 <= x && x < pgm->width && 0 <= y && y < pgm->height ){
                val = val < pgm->max ? val : pgm->max;
                *( pgm->data + ( (pgm->width * y) + x ) ) = val;
        }
}
 
void obtain_mat( struct PgmData* pgm, int x, int y, Matrix33 out ){
 
        int* p;
        int w,h;
        w = pgm->width;
        h = pgm->height;
        p = ( pgm->data + ( (y * w) + x ));
 
        if( x < 0 || y < 0 || x >= w || y >= h ){
                return;
        }
 
        out[1][1] = *p;
        out[1][0] = (x == 0)     ? *p : *(p-1);
        out[1][2] = (x == (w-1)) ? *p : *(p+1);
        out[0][1] = (y == 0)     ? *p : *(p-w);
        out[2][1] = (y == (h-1)) ? *p : *(p+w);
        
        out[0][0] = (x == 0) ? out[0][1] :
                ( (y == 0) ? out[1][0] : *(p-(w+1)) );
 
        out[0][2] = (x == (w-1)) ? out[0][1] :
                ( (y == 0) ? out[1][2] : *(p-(w-1)) );
 
        out[2][0] = (x == 0) ? out[2][1] :
                ( (y == (h-1)) ? out[1][0] : *(p+(w-1)) );
 
        out[2][2] = (x == (w-1)) ? out[2][1] :
                ( (y == (h-1)) ? out[1][2] : *(p+(w+1)) );
}
 
int mult_mat(Matrix33 a, Matrix33 b){
        int i,j,res;
        res = 0;
        for( i = 0; i < 3; i++ ){
                for(j=0;j<3;j++){
                        res += a[j][i] * b[j][i];
                }
        }
        return res;
}
 
 
void write_pgm( FILE* fOut, struct PgmData* pgm, int isBinary ){
        int remained;
        int *p;
        fprintf(fOut,"P%d\n%d %d\n%d\n",isBinary ? 5:2,
                pgm->width,pgm->height,pgm->max);
 
        remained = pgm->width * pgm->height;
        p = pgm->data;
 
        if( isBinary ){
                while( remained > 0 ){
                        fputc(*p,fOut);
                        p++; remained--;
                }
        }
        else if( remained > 0 ){
                while(remained > 0){
                        fprintf(fOut,"%d",*p);
                        p++; remained--;
 
                        if(remained > 0){
                                fputc(' ',fOut);
                        }
                }
        }
}
 
 
int numReader_Text( FILE* binaryIn ){
        int i = 0;
        if( fscanf(binaryIn,"%d",&i) != 1 || i < 0 ){
                return (-1);
        }
        return i;
}
 
int numReader_Binary( FILE* binaryIn ){
        int c;
        c = fgetc(binaryIn);
        return c == EOF ? (-1) : c;
}
 
/* skip comments. returns EOF if eof, or next char. */
int skip_comment(FILE* binaryIn){
        int i;
        while( ( i = fgetc(binaryIn) ) == '#' ){
                do {
                        i = fgetc(binaryIn);
                        if( i == EOF ){
                                return 0;
                        }
                }
                while( i != '\n' && i != '\r' );
        }
        if( i != EOF ){
                ungetc(i,binaryIn);
                return 1;
        }
        return 0;
}
 
struct PgmData* copy_pgm_from( struct PgmData* src ){
        struct PgmData* out;
        int size;
        int *psrc,*pdst;
        out = new_pgm_from(src);
 
        if( out == NULL ){ return NULL; }
 
        pdst = out->data;
        psrc = src->data;
        size = out->width * out->height;
 
        while(size>0){
                *pdst = *psrc;
                psrc++; pdst++;
        }
        return out;
}
 
struct PgmData* new_pgm_from( struct PgmData* src ){
        struct PgmData* out;
 
        out = (struct PgmData*)malloc(sizeof(struct PgmData));
        if( out == NULL ){
                fprintf(stderr,"failed to allocate memory for PgmData.");
                return NULL;
        }
 
        *out = *src;
 
        out->data = (int*)
                malloc( (out->width * out->height ) *sizeof(int));
 
        if( out->data == NULL ){
                fprintf(stderr,"failed to allocate memory for data.");
                free(out);
                return NULL;
        }
        return out;
}
 
struct PgmData* new_pgm_from_file( FILE* fp ){
        struct PgmData* out;
 
        out = (struct PgmData*)malloc(sizeof(struct PgmData));
 
        if( out == NULL ){
                fprintf(stderr,"failed to allocate memory for PgmData.");
                return NULL;
        }
 
        if( ( out->width  = numReader_Text(fp) ) == -1 ){
                fprintf(stderr,"failed to read [width].");
                goto invalid;
        }
        
        if( ( out->height  = numReader_Text(fp) ) == -1 ){
                fprintf(stderr,"failed to read [height].");
                goto invalid;
        }
 
        if( ( out->max  = numReader_Text(fp) ) == -1 ){
                fprintf(stderr,"failed to read [max].");
                goto invalid;
        }
 
        out->data   = (int*)
                malloc( (out->width * out->height ) *sizeof(int));
 
        if( out->data == NULL ){
                fprintf(stderr,"failed to allocate memory for data.");
                goto invalid;
        }
 
        return out;
invalid:
        free(out);
        return NULL;
}
 
/*
   @param binaryIn FILE pointer wichi was opened as binary read.
   @returns NULL if error occured, or valid PgmData*
*/
struct PgmData* read_pgm( FILE* binaryIn ){
        NumReader reader;
        struct PgmData* out;
 
        char header[4];
        int *buffer;
        int remain;
 
        if( fgets(header,4,binaryIn) == (NULL) ){
                fprintf(stderr,"failed to read header.");
                return NULL;
        }
 
        if( header[0] != 'P' || ! isspace(header[2]) ){
                fprintf(stderr,"invalid header.");
                return NULL;
        }
 
        switch( header[1] ){    
                case '2': reader = (NumReader)numReader_Text;   break;
                case '5': reader = (NumReader)numReader_Binary; break;
                default :
                        fprintf(stderr,"unsupported file.");
                        return NULL;
        }
 
        if( !skip_comment(binaryIn) ){
                fprintf(stderr,"invalid header or unexpected eof detected.");
                return NULL;
        }
 
        out = new_pgm_from_file(binaryIn);
        if( out == NULL ){
                return NULL;
        }
 
        buffer = out->data;
        remain = out->width * out->height;
 
        while( remain > 0 ){
                *buffer = reader(binaryIn);
                if(*buffer > out->max){
                        fprintf(stderr,"value at %d: greater than max (%d)\n",
                                (int)(buffer - out->data),out->max);
                }
                if(*buffer == (-1)){
                        fprintf(stderr,"unexpected eof, or invalid value detected.\n");
                        free(out->data);
                        free(out);
                        return NULL;
                }
                buffer++; remain--;
        }
 
        return out;
}
 
void print_pgm(struct PgmData* p){
        int i,j;
        for( i = 0; i < p->width; i++ ){
                for( j = 0; j < p->height; j++ ){
                        printf("%d ",*(p->data+ (p->width*j)+i));
                }
                putchar('\n');
        }
}
 
int main( int argc, char** argv ){
        int isBinary = 0;
 
        const char *fname_in, *fname_out, *c;
        struct FilterData* filter;
        FILE *fIn,*fOut;
 
        struct PgmData* pgm;
 
        filter = &g_grad;
 
        if( argc < 3 ){ goto show_usage; }
 
        if( argv[1][0] == '-' ){
                if( argc != 4 ){
                        goto show_usage;
                }
                for( c = &(argv[1][1]); *c != '\0'; c++ ){
                        switch(*c){
                        case 'b': isBinary = 1; break;
                        case 't': isBinary = 0; break;
                        case 'g': filter = &g_grad;    break;
                        case 'r': filter = &g_roberts; break;
                        case 's': filter = &g_sobel;   break;
                        case 'l': filter = &g_lapl;    break;
                        default:
                                goto show_usage;
                        }
                }
                fname_in  = argv[2];
                fname_out = argv[3];
        }
        else {
                fname_in  = argv[1];
                fname_out = argv[2];
        }
 
 
        if( ( fIn = fopen(fname_in,"rb") ) == NULL ){
                fprintf(stderr,"cannot open file to read: %s",fname_in);
                return (EXIT_FAILURE);
        }
 
        if( ( pgm = read_pgm(fIn) ) == NULL ){
                fclose(fIn);
                return (EXIT_FAILURE);
        }
 
        fclose(fIn);
 
        if( ( fOut = fopen(fname_out,"wb") ) == NULL ){
                fprintf(stderr,"cannot open file to write: %s",fname_out);
                return (EXIT_FAILURE);
        }
 
        pgm = apply_filter(filter,pgm,1.0);
 
        if( pgm == NULL ){
                fclose(fOut);
                return (EXIT_FAILURE);
        }
 
        write_pgm(fOut,pgm,isBinary);
        fclose(fOut);
 
        return (EXIT_SUCCESS);
 
show_usage:
        printf("usage:\n"
               "  %s [options] <in-text> <out-text>\n"
               "  options: (default: -tg)\n"
               "      t: write data as text.\n"
               "      b: write data as binary.\n"
               "      g: gradient filter\n"
               "      s: sobel filter\n"
               "      r: roberts filter\n"
               "      l: laplacian filter\n",
        argv[0]);
        return (EXIT_FAILURE);
}