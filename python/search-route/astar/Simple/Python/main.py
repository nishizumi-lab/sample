# -*- coding: utf-8 -*-
import numpy as np
import cv2

class Node(object):
    def __init__(self,x,y):
        self.pos = (x,y)
        self.hs = (x-self.goal[0])**2 + (y-self.goal[1])**2
        self.fs = 0
        self.owner_list = None
        self.parent_node = None

    def isGoal(self):
        return self.goal == self.pos

class NodeList(list):
    def find(self, x,y):
        l = [t for t in self if t.pos==(x,y)]
        return l[0] if l != [] else None
    def remove(self,node):
        del self[self.index(node)]

def astar(maps, start, goal):
    (h, w) = maps.shape             # マップのサイズ
    Node.start = start              # スタート座標の定義
    Node.goal = goal                # ゴール座標の定義
    open_list = NodeList()          # Openリストの作成
    close_list = NodeList()         # Closeリストの作成
    start_node = Node(*Node.start)  # スタートノードの作成
    start_node.fs = start_node.hs   # f*(S)=h*(S)
    open_list.append(start_node)    # スタートノードをOpenリストに追加

    while(1):
        # Openリストが空になったら経路無し
        if open_list == []:exit(1);
        # Openリストからf*が最少のノードnを取得
        n = min(open_list, key = lambda x:x.fs)
        open_list.remove(n)     # nをOpenリストから削除
        close_list.append(n)    # nをCloseリストに追加
        # 最小ノードがゴールだったら終了
        if n.isGoal():
            goal_node = n
            break

        n_gs = n.fs - n.hs        # g*(n)=f*(n)-h*(n)
        # ノードnの移動可能方向のノードを調べる
        for v in ((1,0),(-1,0),(0,1),(0,-1)):
            x = n.pos[0] + v[0]
            y = n.pos[1] + v[1]
            # 移動先ノードがマップ外or障害物(O)の場合はスルー
            if (0 < y < h and 0 < x < w and maps[y][x] == 1): continue
            # 移動先ノードがOpenリストにあるか確認
            m = open_list.find(x,y)
            cost = (n.pos[0]-x)**2 + (n.pos[1]-y)**2    # 移動コスト:cost(n)
            # mがOpenリストにある時
            if m:
                # より小さいf*(m)ならばf*(m)を更新して親を書き換え
                if m.fs > n_gs + m.hs + cost:
                    m.fs = n_gs + m.hs + cost   # f*(m)=g*(n)+h*(m)+cost(n)
                    m.parent_node = n           # nをmの親ノードに追加
            else:
                # 移動先ノードがCloseリストにあるか確認
                m = close_list.find(x,y)
                # mがCloseリストにある時、より小さいf*ならばf*(m)を更新して親を書き換え、Openリストに移動
                if (m):
                    if m.fs > n_gs + m.hs + cost:
                        m.fs = n_gs + m.hs + cost   # f*(m)=g*(n)+h*(m)+cost(n)
                        m.parent_node = n           # nをmの親ノードに追加
                        open_list.append(m)         # mをOpenリストに追加
                        close_list.remove(m)        # mをCloseリストから削除
                # OpenリストにもCloseリストにもない新規ノードならばOpenリストにノードに追加
                else:
                    m = Node(x,y)
                    m.fs = n_gs + m.hs + cost   # f*(m)=g*(n)+h*(m)+cost(n)
                    m.parent_node = n           # nをmの親ノードに追加
                    open_list.append(m)         # mをOpenリストに追加

    n = goal_node.parent_node
    path = [goal]                           # ゴール座標を経路に追加
    m = [[x for x in line] for line in maps]
    # ゴールノードから親ノードを辿って経路を求める
    n = goal_node.parent_node
    m = [[x for x in line] for line in maps]
    while(1):
        if n.parent_node == None: break
        path.append((n.pos[1], n.pos[0]))   # ノードnを経路に追加
        n = n.parent_node
    path.append(start)                      # スタート座標を経路に追加
    path.reverse()                          # 順序反転
    return path

def main():
    maps = [
    [0,0,0,0,0],
    [0,0,1,0,1],
    [0,1,0,0,0],
    [0,1,1,0,0],
    [0,0,0,0,0]
    ]
    path = astar(maps, (1,1), (3,4))
    print path

if __name__ == "__main__":
    main()
