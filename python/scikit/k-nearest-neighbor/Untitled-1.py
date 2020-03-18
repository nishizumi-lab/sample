# -*- coding: utf-8 -*-
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from time import time
from sklearn.utils import shuffle
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin

if len(sys.argv) < 3:
    print('python main.py <image> <nb_couleurs>')

file = sys.argv[1]
nb_colors = int(sys.argv[2])

print('-' * 80)
print 'Image:', file
print 'Nombre de couleurs:', nb_colors
print('-' * 80)


def recreate_image(codebook, labels, w, h):
    d = codebook.shape[1]
    img = np.zeros((w, h, d))
    label_idx = 0
    for i in range(w):
        for j in range(h):
            img[i][j] = codebook[labels[label_idx]]
            label_idx += 1
    return img


image = cv2.imread(file)
image = np.array(image, dtype=np.float64) / 255

w, h, d = tuple(image.shape)
image_array = np.reshape(image, (w * h, d))

print('# Apprentissage par la méthode des K plus proches voisins')
print("Pour apprendre, on prend un échantillon de 1000 couleurs prises au hasard dans l'image de départ.")
image_array_sample = shuffle(image_array, random_state=0)[:1000]
print("On applique l'algorithme des K plus proche voisin sur l'image avec les couleurs sélectionnées et le nombre de couleurs cible.")
kmeans = KMeans(n_clusters=nb_colors, random_state=0).fit(image_array_sample)

print("On prédit les couleurs ensuite l'algorithme des K plus proche voisin sur l'image.")
labels = kmeans.predict(image_array)

print('-' * 80)
print("Pour comparer la méthode d'apprentissage des plus proche voisin et une méthode de sélection aléatoire des couleurs, on sélectionne autant de couleur que de couleurs cible aléatoirement dans l'image.")
codebook_random = shuffle(image_array, random_state=0)[:nb_colors]
print("Pour choisir la couleur à remplacer, on prend la couleur selectionnée qui est la plus proche.")
labels_random = pairwise_distances_argmin(codebook_random, image_array, axis=0)

print('-' * 80)

cv2.imshow('Original image', image)
cv2.imshow('K-Means image', recreate_image(kmeans.cluster_centers_, labels, w, h))
cv2.imshow('Random image', recreate_image(
    codebook_random, labels_random, w, h))
cv2.waitKey(0)
