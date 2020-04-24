# -*- coding: utf-8 -*
import glob
import cv2
import numpy as np

# 画像配列の作成
def create_images_array(load_img_paths):
    imgs = []
    # Hog特徴のパラメータ
    win_size = (64, 64)
    block_size = (16, 16)
    block_stride = (4, 4)
    cell_size = (4, 4)
    bins = 9
    # 画像群の配列を生成
    for load_img_path in load_img_paths:
        # 画像をロード, グレースケール変換
        # 色反転, 64*64にリサイズ, 1次元配列に変換
        img = cv2.imread(load_img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, win_size)
        hog = cv2.HOGDescriptor(win_size, block_size, block_stride, cell_size, bins)
        img = hog.compute(gray)
        imgs.append(img)
    return np.array(imgs, np.float32)

def main():
    # 学習用の画像ファイルの格納先（0～2の3種類）
    LOAD_TRAIN_IMG0S_PATH = '/Users/panzer5/github/sample/python/opencv/svm/ex4_data/img0/*'
    LOAD_TRAIN_IMG1S_PATH = '/Users/panzer5/github/sample/python/opencv/svm/ex4_data/img1/*'
    LOAD_TRAIN_IMG2S_PATH = '/Users/panzer5/github/sample/python/opencv/svm/ex4_data/img2/*'

    # 作成した学習モデルの保存先
    SAVE_TRAINED_DATA_PATH = '/Users/panzer5/github/sample/python/opencv/svm/ex4_data/svm_trained_data.xml'
    
    # 検証用の画像ファイルの格納先（0～2の3種類）
    LOAD_TEST_IMG0S_PATH = '/Users/panzer5/github/sample/python/opencv/svm/ex4_data/test_img0/*'
    LOAD_TEST_IMG1S_PATH = '/Users/panzer5/github/sample/python/opencv/svm/ex4_data/test_img1/*'
    LOAD_TEST_IMG2S_PATH = '/Users/panzer5/github/sample/python/opencv/svm/ex4_data/test_img2/*'

    # 学習用の画像ファイルのパスを取得
    load_img0_paths = glob.glob(LOAD_TRAIN_IMG0S_PATH)
    load_img1_paths = glob.glob(LOAD_TRAIN_IMG1S_PATH)
    load_img2_paths = glob.glob(LOAD_TRAIN_IMG2S_PATH)

    # 学習用の画像ファイルをロード
    imgs0 = create_images_array(load_img0_paths)
    imgs1 = create_images_array(load_img1_paths)
    imgs2 = create_images_array(load_img2_paths)
    imgs = np.r_[imgs0, imgs1, imgs2]

    # 正解ラベルを生成
    labels0 = np.full(len(load_img0_paths), 0, np.int32)
    labels1 = np.full(len(load_img1_paths), 1, np.int32)
    labels2 = np.full(len(load_img2_paths), 2, np.int32)
    labels = np.array([np.r_[labels0, labels1, labels2]])

    # SVMで学習モデルの作成（カーネル:LINEAR 線形, gamma:1, C:1）
    svm = cv2.ml.SVM_create()
    svm.setType(cv2.ml.SVM_C_SVC)
    svm.setKernel(cv2.ml.SVM_LINEAR)
    svm.setGamma(1)
    svm.setC(1)
    svm.setTermCriteria((cv2.TERM_CRITERIA_COUNT, 100, 1.e-06))
    svm.train(imgs, cv2.ml.ROW_SAMPLE, labels)

    # 学習結果を保存
    svm.save(SAVE_TRAINED_DATA_PATH)

    # 学習モデルを検証
    # 0～2のテスト用画像を入力し、画像に書かれた数字を予測
    test_img0_paths = glob.glob(LOAD_TEST_IMG0S_PATH)
    test_img1_paths = glob.glob(LOAD_TEST_IMG1S_PATH)
    test_img2_paths = glob.glob(LOAD_TEST_IMG2S_PATH)
    test_imgs0 = create_images_array(test_img0_paths)
    test_imgs1 = create_images_array(test_img1_paths)
    test_imgs2 = create_images_array(test_img2_paths)
    test_imgs = np.r_[test_imgs0, test_imgs1, test_imgs2]

    # 正解ラベルを生成
    test_labels0 = np.full(len(test_img0_paths), 0, np.int32)
    test_labels1 = np.full(len(test_img1_paths), 1, np.int32)
    test_labels2 = np.full(len(test_img2_paths), 2, np.int32)
    test_labels = np.array([np.r_[test_labels0, test_labels1, test_labels2]])

    svm = cv2.ml.SVM_load(SAVE_TRAINED_DATA_PATH)
    predicted = svm.predict(test_imgs)

    # 正解ラベル、予想値、正解率を表示
    print("test labels:", test_labels)
    print("predicted:", predicted[1].T)
    score = np.sum(test_labels == predicted[1].T)/len(test_labels[0])
    print("Score:", score)

    """
    <やかん、土鍋、マグカップ画像を学習した場合>
    test labels: [[0 0 1 1 2 2]]
    predicted: [[0. 0. 1. 1. 2. 2.]]
    Score: 1.0
    """

if __name__ == '__main__':
    main()
