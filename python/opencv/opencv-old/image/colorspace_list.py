# -*- coding: utf-8 -*-
import cv2

def main():
    flags = [i for i in dir(cv2) if i.startswith('COLOR_')]
    print flags

if __name__ == "__main__":
    main()
