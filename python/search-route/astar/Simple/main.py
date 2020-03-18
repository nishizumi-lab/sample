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
    w = max([len(x) for x in maps])
    h = len(maps)
    Node.start = start
    Node.goal = goal
    # OpenリストとCloseリストを設定
    open_list = NodeList()
    close_list = NodeList()
    start_node = Node(*Node.start)
    start_node.fs = start_node.hs
    open_list.append(start_node)

    while(1):
        # Openリストが空になったら解なし
        if open_list == []:
            print "No route!"
            exit(1);

        # Openリストからf*が最少のノードnを取得
        n = min(open_list, key = lambda x:x.fs)
        open_list.remove(n)     # ノードnをOpenノードから除去
        close_list.append(n)    # ノードnをCloseノードに追加

        # 最小ノードがゴールだったら終了
        if n.isGoal():
            goal_node = n
            break

        n_gs = n.fs - n.hs        # f*() = g*() + h*() -> g*() = f*() - h*()

        # ノードnの移動可能方向のノードを調べる
        for v in ((1,0),(-1,0),(0,1),(0,-1)):
            x = n.pos[0] + v[0]
            y = n.pos[1] + v[1]
            # 移動先ノードがマップ外or障害物(O)の場合はスルー
            if (0 < y < h and 0 < x < w and maps[y][x] == '1'): continue
            m = open_list.find(x,y) # 移動先ノードがOpenリストに格納されているかチェック
            cost = (n.pos[0]-x)**2 + (n.pos[1]-y)**2
            if m: # 移動先ノーがOpenリストに格納されていた場合、より小さいf*ならばノードmのf*を更新し、親を書き換え
                if m.fs > n_gs + m.hs + cost:
                    m.fs = n_gs + m.hs + cost
                    m.parent_node = n
            else:
                m = close_list.find(x,y)
                # 移動先のノードがCloseリストに格納されていた場合、より小さいf*ならばノードmのf*を更新し、親を書き換えかつ、Openリストに移動する
                if (m):
                    if m.fs > n_gs + m.hs + cost:
                        m.fs = n_gs + m.hs + cost
                        m.parent_node = n
                        open_list.append(m)
                        close_list.remove(m)
                # 新規ノードならばOpenリストにノードに追加
                else:
                    m = Node(x,y)
                    m.fs = n_gs + m.hs + cost
                    m.parent_node = n
                    open_list.append(m)

    # ゴールノードから親を辿って経路を求める
    n = goal_node.parent_node
    path = [goal]
    m = [[x for x in line] for line in maps]
    while(1):
        if n.parent_node == None: break
        path.append(n.pos)
        n = n.parent_node
    path.append(start)
    path.reverse()      # 順序反転
    return path

def main():
    im = cv2.imread("map.png")                  # 地図画像の取得
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) # グレースケール変換
    gray[gray < 50] = 1                         # 経路探索用マップに変換(移動可能=0, 不可=1)
    gray[gray > 51] = 0
    path = astar(gray, (1,1), (29,29))
    if len(path)==0:
        print("No route")
        return 0
    for y, x in path[::]:                       # 探索した経路を画像に描く
        cv2.circle(im,(int(x),int(y)), 1, (15,20,215), 1)
    cv2.imwrite("map2.png",im)

if __name__ == "__main__":
    main()
