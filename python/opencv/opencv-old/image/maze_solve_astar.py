# -*- coding: utf-8 -*-
import cv2,heapq
import numpy as np

def diffs(d1,d2):
    return sum(np.abs(d1-d2))

# 読み取り
def scanning(d, L ,R, n, (w,h), th):
    flag = False
    for i in xrange(n):
        label = n
        if i - w >= 0 and diffs(d[i], d[i-w]) <= th:
            label = min(label, L[i-w])

        if i + w < n and diffs(d[i], d[i+w]) <= th:
            label = min(label, L[i+w])

        if i % w != 0 and diffs(d[i], d[i-1]) <= th:
            label = min(label, L[i-1])

        if (i + 1) % w != 0 and diffs(d[i], d[i+1]) <= th:
            label = min(label, L[i+1])

        if label < L[i]:
            R[L[i]] = label
            flag = True

    return flag, R

# 解析
def analysis(L ,R, n):
    for i in xrange(n):
        label = L[i]
        if label == i:
            ref = label
            label = R[ref]
            while(1):
                ref = label
                label = R[ref]
                if ref == label: break
            R[i] = label

    return R

# 経路の長さを計算
def distance(path, S=0):
    if len(path) == 0: return 0
    S = np.diff(path,axis=0)
    S = np.linalg.norm(S,axis=1)
    return int(np.sum(S))

# 周囲
def neighbor((y,x), L, passage, (h,w)):
    nbs = []
    if y > 0 and L[y-1][x] == passage:
        nbs.append((y-1, x))
    if y < h-1 and L[y+1][x] == passage:
        nbs.append((y+1, x))
    if x > 0 and L[y][x-1] == passage:
        nbs.append((y, x-1))
    if x < w-1 and L[y][x+1] == passage:
        nbs.append((y, x+1))
    if y > 0 and x > 0 and L[y-1][x-1] == passage:
        nbs.append((y-1, x-1))
    if y < h-1 and x > 0 and L[y+1][x-1] == passage:
        nbs.append((y+1, x-1))
    if y > 0 and x < w-1 and L[y-1][x+1] == passage:
        nbs.append((y-1, x+1))
    if y < h-1 and x < w-1 and L[y+1][x+1] == passage:
        nbs.append((y+1, x+1))
    return nbs

# AStarアルゴリズムで最短経路の探索
def astar(L, p1, p2):
    # ラベル領域内に目標点が無ければ経路無し
    if L[p1[0]][p1[1]] != L[p2[0]][p2[1]]: print("No route!")
    (h, w) = len(L),len(L[0])
    path,queue,checked = [],[],[p1]
    p1, p2 = np.array(p1),np.array(p2)
    heapq.heappush(queue, (distance(checked) + np.linalg.norm(p1-p2), checked))

    while len(queue) > 0:
        path = heapq.heappop(queue)[1]
        # 目標点まで経路が到達したら終了
        if path[-1][0] == p2[0] and path[-1][1] == p2[1]:
            return path
        nbs = neighbor(path[-1], L, L[p1[0]][p1[1]], (h, w))
        for nb in nbs:
            if nb in checked: continue
            checked.append(nb)
            newpath = path + [nb]
            heapq.heappush(queue, (distance(newpath) + np.linalg.norm(np.array(nb)-p2), newpath))
    return []

# CCL
def maze_solve(im, (x1,y1), (x2,y2), th, n):
    w0,h0 = im.shape[1],im.shape[0]             # 画像の幅,高さ
    rate = np.sqrt(float(n)/(w0*h0))            # 比率
    w,h = int(w0*rate),int(h0*rate)             # リサイズ画像の幅,高さ
    n = w * h
    im = cv2.resize(im,(w,h))                   # 画像を1/2に縮小
    data = im.reshape((h*w,3)).astype("int32")  # 配列を3次元(unit8)から2次元(int32)へ変換
    R,L = np.arange(n),np.arange(n)             # 配列R,Lの作成
    p1 = (int(y1*rate), int(x1*rate))
    p2 = (int(y2*rate), int(x2*rate))
    while(1):
        flag, R = scanning(data, L ,R, n, (w,h), th)
        if flag:
            R = analysis(L ,R, n)
            L = R[R[L]]
        else:
            L = [L[i:i+w] for i in xrange(0, n, w)] # numpyのLでなくなってる
            path = astar(L, p1 , p2)                # 経路算出
            return path/rate

def main():
    p1,p2 = (45, 13),(95, 13)                         # スタートとゴール座標
    im = cv2.imread("map.jpg")                          # 地図画像の取得
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)         # グレースケール変換
    # 2値化
    cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    im2 = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)        # グレースケール変換
    path = maze_solve(im2, p1, p2, 30, 30000)           # Astarアルゴリズムで経路算出
    # 算出した経路を赤点で地図画像に描画
    for y, x in path[::]:
        cv2.circle(im,(int(x),int(y)), 2, (15,20,215), -1)
    cv2.imwrite("map2.jpg",im)


if __name__ == '__main__':
    main()
