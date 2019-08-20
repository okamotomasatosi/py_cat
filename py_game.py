# -*- coding:utf-8 -*-
import os
import copy
import time
import sys
import random
import pygame
from pygame.locals import *

SCREEN_SET = Rect(0, 0, 800, 700)
###################################
#
# 　ここからメイン
#
###################################
def main():
    #変数の初期化
    x1_pt = 150
    y1_pt = 0
    list0 = [[]]
    list1 = [[1, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1]]

    pygame.init()    # Pygameの初期化
    screen = pygame.display.set_mode((800, 700))  # 画面サイズを指定して画面を生成
    pygame.display.set_caption("GAME")  # タイトルバーに表示する文字
    font = pygame.font.Font(None, 40)  # フォントの設定(55px)

    face_img = pygame.image.load("./img/mas_face.jpg")
    cat_img = pygame.image.load("./img/cat.png")  # 画像を読み込む(今回追加したとこ)

    screen.fill((0, 0, 0))      # 画面を黒色に塗りつぶし
    list0 = copy.deepcopy(list1)    # ディープコピー
    screen.fill((0, 0, 0))      # ウィンドウの背景色
    put_img(screen, face_img, 400, 100)  # 画面に顔を置く
    #初期の猫の色を決める
    catColor = random.randint(2,7)

    while (1):
        #一番上まで埋まったかチェック
        retCollision: bool = chekCollision(int(x1_pt / 50), int(y1_pt / 50), list0)
        if retCollision:
            # 一番上まで埋まってたので、暫定的に枠内をクリア
            list0 = copy.deepcopy(list1)  # ディープコピー
        put_frame(screen, list0)    # 画面に枠を置く
        time.sleep(0.2)             # 速度調整のsleep

        # キー入力など、イベント処理
        x1_pt,y1_pt = event_proc(x1_pt,y1_pt)

        y1_pt = y1_pt + 50        # ブロック落下

        #ブロック当たりチェック
        retCollision:bool = chekCollision(int(x1_pt/50), int(y1_pt/50), list0)
        if retCollision:
            y1_pt = y1_pt - 50      # 落下できなかったので戻す
            #ブロックの固定
            list0 = setBlockList(int(x1_pt/50), int(y1_pt/50), catColor, list0)
            #並びブロックのチェックと削除
            list0 = chekDeleteCat(int(x1_pt/50), int(y1_pt/50), list0)
            catColor = random.randint(2, 7)     # 次の猫色を決める
            y1_pt = 0                           # ぶつかったのでy座標をゼロに戻す
            put_frame(screen, list0)            # 画面に枠を置く

        # 閾値超えたら戻るように
        if y1_pt > 400:
            y1_pt = 0

        putDropCat(screen, catColor, x1_pt, y1_pt)

        # screen.blit(font.render("AAA", True, (255,255,0)), [40, 40])# 文字列の表示位置

        ##pygame.display.flip()  # display Surface全体を更新して画面に描写します。
        pygame.display.update()     # スクリーンの一部分のみを更新します。この命令はソフトウェア側での表示処理に最適化されています。

## ブロックの削除対象チェックと削除
def chekDeleteCat(x, y, list0: list) -> list:
    if y>6:
        # 底から2段目以下ならば3個並んでいないので即返る
        return list0
    elif y<2:
        # 天から2段目以上ならば3個並んでいないので即返る
        return list0

    cat0 = list0[y][x]
    cat1 = list0[y+1][x]
    cat2 = list0[y+2][x]
    if (cat0 == cat1) and (cat1 == cat2):
        # 3個並んでる
        list0[y][x]=0
        list0[y + 1][x]=0
        list0[y + 2][x]=0
    return list0

## ブロックの当たり判定　※簡易なので下しか見ていない。本来は横も見る
def chekCollision(x, y, list0:list) -> bool:
    block = list0[y][x]
    print('block=', block)
    if block == 0:
        return False
    else:
        return True

## 着地したブロックを変数に書き込む
def setBlockList(x, y, cat_col,list0: list)-> list:
    list0[y][x] = cat_col
    return list0


## キー入力など、イベント処理
##　矢印キーでブロックの座標他仕込みも行う
def event_proc(x1_pt,y1_pt):
        """
        :type x1_pt: int
        :type y1_pt: int
        """
        # イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:  # 閉じるボタンが押されたら終了
                pygame.quit()  # Pygameの終了(画面閉じられる)
                sys.exit()
            # キー操作(追加したとこ)
            elif event.type == KEYDOWN:
                print("event.type=" + str(event.type))
                print("event.key=" + str(event.key))
                if event.key == K_LEFT:
                    print("←")
                    x1_pt -= 50
                elif event.key == K_RIGHT:
                    print("→")
                    x1_pt += 50
                #elif event.key == K_UP:
                    #print("↑")
                    #y1_pt -= 50
                #elif event.key == K_DOWN:
                    #print("↓")
                    #y1_pt += 50
        if x1_pt < 50:
            x1_pt = 50
        if x1_pt > 250:
            x1_pt = 250
        #　座標のみ返す
        return x1_pt,y1_pt

##　指定のブロック絵柄（猫）をイメージオブジェクトに入れて返す
def getCatImg(catColor:int):
    if catColor == 2:
        dropCatimg = pygame.image.load("./img/neko0.png")  # 画像を読み込む(今回追加したとこ)
    elif catColor == 3:
        dropCatimg = pygame.image.load("./img/neko1.png")  # 画像を読み込む(今回追加したとこ)
    elif catColor == 4:
        dropCatimg = pygame.image.load("./img/neko2.png")  # 画像を読み込む(今回追加したとこ)
    elif catColor == 5:
        dropCatimg = pygame.image.load("./img/neko3.png")  # 画像を読み込む(今回追加したとこ)
    elif catColor == 6:
        dropCatimg = pygame.image.load("./img/neko4.png")  # 画像を読み込む(今回追加したとこ)
    elif catColor == 7:
        dropCatimg = pygame.image.load("./img/neko5.png")  # 画像を読み込む(今回追加したとこ)
    return dropCatimg

##　落ちてくるブロック（猫）を画面に置く
def putDropCat(screen, catColor, x1_pt, y1_pt):
    dropCatImg = getCatImg(catColor)
    screen.blit(dropCatImg, (x1_pt, y1_pt))


##フレーム内を描き直す
def put_frame(screen, list):
    block_img = pygame.image.load("./img/block.png")  # 画像を読み込む(今回追加したとこ)
    blank_img = pygame.image.load("./img/blank.png")  # 画像を読み込む(今回追加したとこ)
    neko0_img = pygame.image.load("./img/neko0.png")  # 画像を読み込む(今回追加したとこ)
    neko1_img = pygame.image.load("./img/neko1.png")  # 画像を読み込む(今回追加したとこ)
    neko2_img = pygame.image.load("./img/neko2.png")  # 画像を読み込む(今回追加したとこ)
    neko3_img = pygame.image.load("./img/neko3.png")  # 画像を読み込む(今回追加したとこ)
    neko4_img = pygame.image.load("./img/neko4.png")  # 画像を読み込む(今回追加したとこ)
    neko5_img = pygame.image.load("./img/neko5.png")  # 画像を読み込む(今回追加したとこ)

    # 枠のブロックを表示する。
    y_idx = 0
    for val1 in list:
        x_idx = 0
        for val2 in val1:
            # text = list2[0][index2]
            text = str(val2)
            if text == '0':
                put_block(screen, blank_img, x_idx, y_idx)
            elif text == '2':
                put_block(screen, neko0_img, x_idx, y_idx)
            elif text == '3':
                put_block(screen, neko1_img, x_idx, y_idx)
            elif text == '4':
                put_block(screen, neko2_img, x_idx, y_idx)
            elif text == '5':
                put_block(screen, neko3_img, x_idx, y_idx)
            elif text == '6':
                put_block(screen, neko4_img, x_idx, y_idx)
            elif text == '7':
                put_block(screen, neko5_img, x_idx, y_idx)
            else:
                put_block(screen, block_img, x_idx, y_idx)
            x_idx += 1
        y_idx += 1


## 絵を表示する
def put_img(screen, img_obj, x, y):
    screen.blit(img_obj, (50 * x, 50 * y, 50, 50))  # 絵を画面に貼り付ける


## ブロックを画面に置く
def put_block(screen, img_obj, x, y):
    screen.blit(img_obj, ((50 * x), (50 * y), 50, 50))  # 絵を画面に貼り付ける

##画面に資格を書く
def put_rect(screen, x, y):
    RED = (255, 0, 0)
    rect = ((50 * x), (50 * y), 50, 50)
    pygame.draw.rect(screen, RED, rect)
    # screen.blit(font.render( in_chr, True, (255, 255, 0)), [(50 * x_idx), (40 * y_idx)])  # 文字列の表示位置

##　既定　これが無いと動かない
if __name__ == "__main__":
    main()
