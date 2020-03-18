#include "opencv2\opencv.hpp"
using namespace cv;

int main(void)
{
  Mat im = imread("test.png", 0);
  if(im.empty()) return -1;

  Mat im2 = ~im;

  imshow("image1", im);
  imshow("image2", im2);
  waitKey(0);
}
