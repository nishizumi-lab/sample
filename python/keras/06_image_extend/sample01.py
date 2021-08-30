from keras.preprocessing.image import load_img, img_to_array
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

# 1枚あたり20枚の画像を水増し
N_img = 20

# 入力画像の保存先パス
input_path = "C:/github/sample/python/keras/06_image_extend/sample01_data/input/"
files = glob.glob(input_path + '/*.jpg')
 
# 出力画像の保存先パス
output_path = "C:/github/sample/python/keras/06_image_extend/sample01_data/output/"
if os.path.isdir(output_path) == False:
    os.mkdir(output_path)
 
 
for i, file in enumerate(files):
 
    img = load_img(file)
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
 
    # ImageDataGeneratorの生成
    datagen = ImageDataGenerator(
    featurewise_center=False,
    samplewise_center=False,
    featurewise_std_normalization=False,
    samplewise_std_normalization=False,
    zca_whitening=False,
    zca_epsilon=1e-06,
    rotation_range=10.0,
    width_shift_range=0.0,
    height_shift_range=0.0,
    brightness_range=None,
    shear_range=0.0,
    zoom_range=0.0,
    channel_shift_range=0.0,
    fill_mode='nearest',
    cval=0.0,
    horizontal_flip=True,
    vertical_flip=True,
    rescale=None,
    preprocessing_function=None,
    data_format=None,
    validation_split=0.0)
 
    # 1枚あたり20枚の画像を水増し生成
    dg = datagen.flow(x, batch_size=1, save_to_dir=output_path, save_prefix='img', save_format='jpg')
    for i in range(N_img):
        batch = dg.next()