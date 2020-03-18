#include <stdlib.h>
#include <stdio.h>
#include <string.h>
 
#if defined(__GNUC__)
#  include <opencv2/core/core_c.h>
#  include <opencv2/highgui/highgui_c.h> 
#  define  cvSaveImage(x,y) cvSaveImage((x),(y),0)
#else
#  include <opencv/core.h>
#  include <opencv/highgui.h>
#endif
 
#define log_print__(...) printf(__VA_ARGS__)
 
/* Œv‘ª—p */
typedef struct CountableTree_ {
    int value;
    int count;
    struct CountableTree_* node_l;
    struct CountableTree_* node_r;
} CTree_;
 
/* –Ø‚©‚ç•ÏŠ·‚µ‚ÄŽg‚¤‚¾‚¯ */
typedef struct ValList_ {
    int value;
    struct ValList_* n;
} VList_;
 
typedef int (*CtGetter_)(CTree_*);
 
IplImage* createModeImageColor( IplImage**, int );
IplImage* createModeImageGray( IplImage**, int );
IplImage* createMedianImageColor( IplImage**, int );
IplImage* createMedianImageGray( IplImage**, int );
 
static CTree_* ctreeNew__(int initvalue);
static void    ctreeAdd__(CTree_*,int);
static void    ctreeDelete__(CTree_*);
static int     ctreeGetMedian__(CTree_*);
static int     ctreeGetMinMode__(CTree_*);
static void    ctreeGetMinMode_Inner__(CTree_**, CTree_*);
static int     ctreeAsSortedList__(VList_**,CTree_*);
 
static VList_* vlistNew__(int);
static void    vlistDelete__(VList_*);
 
static IplImage*  createImageInner__( IplImage**, int, int, CtGetter_ );
static void       doLoopImage__(IplImage**,  IplImage*, int, int, int, CtGetter_ );
static IplImage** loadImages__( const char*, int, int, int );
static void       releaseImages__( IplImage**, int );
 
static int ctreeGetMedian__(CTree_* ctree){
    VList_ h;
    VList_* res;
    int size, m_index, i, median;
 
    res = &h;
    size = ctreeAsSortedList__(&res,ctree);
 
    if( size < 1 ){ return (-1); }
 
    res = &h;
    m_index = (int)(size/2);
    for( i = 0; i < m_index; i++ ){
        res = res->n;
    }
 
    /* odd */
    if( size & 1 ){
        median = res->value;
    }
    /* even */
    else {
        /* arithmetic mean, floor value. */
        median = (int)( ( res->n->value + res->value ) / 2 );
    }
    vlistDelete__(h.n);
    return median;
}
 
static int ctreeAsSortedList__(VList_** out,CTree_* ctree){
    int size = 0, i = 0;
    if(ctree){
        size = ctreeAsSortedList__(out,ctree->node_l);
 
        for( i = 0; i < ctree->count; i++ ){
            (*out)->n = vlistNew__(ctree->value);
            (*out) = (*out)->n;
        }
        size = size + ctree->count + 
            ctreeAsSortedList__(out,ctree->node_r);
    }
    return size;
}
 
static void vlistDelete__( VList_* v ){
    if(v){ vlistDelete__(v->n); }
    free(v);
}
 
static VList_* vlistNew__(int value){
    VList_* newOne;
    newOne = (VList_*)malloc(sizeof(VList_));
 
    if( newOne ){
        newOne->value = value;
        newOne->n = NULL;
    }
    return newOne;
    
}
 
static CTree_* ctreeNew__(int initvalue){
    CTree_* newOne;
    newOne = (CTree_*)malloc(sizeof(CTree_));
 
    if( newOne ){
        newOne->value = initvalue;
        newOne->count = 1;
        newOne->node_l = newOne->node_r = NULL;
    }
    return newOne;
}
 
static void ctreeAdd__(CTree_* ct,int value){
    CTree_* p, * parent;
 
    if( ! ct ){ return; }
 
    parent = ct;
    p = ct;
 
    while(p){
       parent = p;
       if( p->value == value ){
           p->count++;
           return;
       }
       p = ( value < p->value ) ? p->node_l : p->node_r;
    }
    if( value < parent->value ){
        parent->node_l = ctreeNew__(value);
    }
    else parent->node_r = ctreeNew__(value);
}
 
static void ctreeGetMinMode_Inner__(CTree_** out, CTree_* ct){
    if(ct){
        ctreeGetMinMode_Inner__(out,ct->node_l);
        if( ! (*out) || ct->count > (*out)->count ){
            *out = ct;
        }
        ctreeGetMinMode_Inner__(out,ct->node_r);
    }
}
 
static int ctreeGetMinMode__(CTree_* ct){
    CTree_* out = NULL;
    ctreeGetMinMode_Inner__(&out,ct);
    return ( out ? out->value : (-1) );
}
 
static void ctreeDelete__(CTree_* ct){
    if( ct ){
        ctreeDelete__(ct->node_l);
        ctreeDelete__(ct->node_r);
        free(ct);
    }
}
 
IplImage* createModeImageColor(
    IplImage** srclist, int srcsize )
{
    return createImageInner__(srclist,srcsize,3,ctreeGetMinMode__);
}
 
IplImage* createModeImageGray(
    IplImage** srclist, int srcsize )
{
    return createImageInner__(srclist,srcsize,1,ctreeGetMinMode__);
}
 
 
IplImage* createMedianImageColor(
    IplImage** srclist, int srcsize )
{
    return createImageInner__(srclist,srcsize,3,ctreeGetMedian__);
}
 
IplImage* createMedianImageGray(
    IplImage** srclist, int srcsize )
{
    return createImageInner__(srclist,srcsize,1,ctreeGetMedian__);
}
 
static IplImage* createImageInner__(
    IplImage** srclist, int srcsize, int ch, CtGetter_ getter )
{
    IplImage* dst;
    int i;
    CvSize imgsize;
    if( srcsize < 0 || !srclist ){ return NULL; }
 
    imgsize.width = srclist[0]->width;
    imgsize.height = srclist[0]->height;
 
    dst = cvCreateImage(imgsize,IPL_DEPTH_8U,ch);
    for(i=0;i<ch;i++){
        doLoopImage__(srclist,dst,srcsize,ch,i,getter);
    }
    return dst;
}
 
static void doLoopImage__(
    IplImage** srclist, IplImage* dst, int srcsize, int bytes, int ch,
    CtGetter_ getter )
{
    int w, h, step, x, y, i;
    CTree_* p;
 
    if( srcsize < 1 ){ return; }
 
    w  = srclist[0]->width;
    h = srclist[0]->height;
    step = srclist[0]->widthStep;
 
    log_print__("width = %d, height = %d, channel = %d\n",w,h,ch);
    for( y = 0; y < h; y++ ){
      for( x = 0; x < w; x++ ){
        p = ctreeNew__(
          CV_IMAGE_ELEM(srclist[0],uchar,y,x*bytes + ch)
        );
        if(!p){ continue; }
 
        for(i=1;i<srcsize;i++){
            ctreeAdd__(p,
              CV_IMAGE_ELEM(srclist[i],uchar,y,x*bytes + ch) );
        }
        dst->imageData[step*y + x*bytes + ch] = getter(p);
        ctreeDelete__(p);
      }
    }
}
 
static IplImage** loadImages__(
    const char* format, int start, int count, int flag )
{
    int i;
    char* buffer;
    IplImage** images;
 
    buffer = (char*)malloc(sizeof(char)*( strlen(format) + 16 ));
    if( !buffer ){
        fprintf(stderr,"failed to  allocate memory "
                       "for in-filename buffer\n");
        return NULL;
    }
 
    images = (IplImage**)malloc(sizeof(IplImage*)*(count+1));
    if( !images ){
        fprintf(stderr,"failed to  allocate memory"
                       " for image pointers.\n");
        return NULL;
    }
 
    for( i = 0; i < count; i++ ){
        sprintf(buffer,format,start+i);
        log_print__("loading: %s\n",buffer);
        images[i] = cvLoadImage(buffer,flag);
    }
    return images;
}
 
static void releaseImages__( IplImage** images, int count ){
    int i;
    for( i = 0; i < count; i++ ){
        cvReleaseImage(&(images[i]));
    }
}
 
int main( int argc, char** argv ){
    int start, end, count;
    IplImage** images;
    IplImage* temp;
    char* buffer;
 
    if( argc != 5 ||
        sscanf(argv[2],"%d",&start) != 1 || start < 0 ||
        sscanf(argv[3],"%d",&end)   != 1 || end   < 0 ||
        end < start){
        printf(
            "usage: \n"
            "  %s [options] <input (printf-format)>"
            "  <startnum> <endnum> <output (printf-format)\n\n"
            "e.g. %s s%%04d.png 0 3 %%s.png\n"
            "  -> load s0000.png s0001.png s0002.png s0003.png,\n"
            "     and store filtered to ColorMedian.png, ColorMode.png,\n"
            "     GrayMedian.png, GrayMode.png\n",
            argv[0],argv[0]
        );
        return 0;
    }
 
    buffer = (char*)malloc(sizeof(char)*( strlen(argv[4]) + 32 ));
    if( !buffer ){
        fprintf(stderr,"failed to allocate out-filename buffer.\n");
        return (-1);
    }
 
    count = ( end - start ) + 1;
 
#   define doFilterMacro__( \
        outname, chn, functype, im, ct, buf, tmp ) \
            \
            log_print__("processing: type = "\
                    #chn ", filter = " #functype "\n");\
            \
            tmp = create##functype##Image##chn ( im, ct );\
            if( tmp != NULL ){\
                sprintf(buf,outname,#chn #functype);\
                log_print__("-> %s\n",buf);\
                cvSaveImage(buf,tmp);\
            }\
            cvReleaseImage(&tmp)\
        \
    \
 
    /* end def*/
 
    images = loadImages__(argv[1],start,count,CV_LOAD_IMAGE_COLOR);
    doFilterMacro__(argv[4],Color,Mode,images,count,buffer,temp);
    doFilterMacro__(argv[4],Color,Median,images,count,buffer,temp);
 
    log_print__("release loaded images.\n");
    releaseImages__(images,count);
 
    images = loadImages__(argv[1],start,count,CV_LOAD_IMAGE_GRAYSCALE);
    doFilterMacro__(argv[4],Gray,Mode,images,count,buffer,temp);
    doFilterMacro__(argv[4],Gray,Median,images,count,buffer,temp);
 
    log_print__("complete.\n");
 
    return 0;
}
 