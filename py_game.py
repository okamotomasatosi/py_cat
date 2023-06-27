# -*- coding:utf-8 -*-
import os
import copy
import time
import sys
import random
import pygame
from pygame.locals import *
# 以下コマンドでpygameをインストールすること
# python -m pip install pygame

#スクリーンの大きさを設定
SCREEN_SET = Rect(0, 0, 800, 700)

cat_size = 50

#ゲームの枠部分　0=無  1=壁　　※静的
frame_list = [[1, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 1, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1]]


###################################
#
# 　ここからメイン
#
###################################
def main():
    # 変数の初期化
    x1_pt = 150
    y1_pt = 0
    score = 0

    pygame.init()  # Pygameの初期化
    screen = pygame.display.set_mode((800, 700))  # 画面サイズを指定して画面を生成
    pygame.display.set_caption("GAME")  # タイトルバーに表示する文字
    screen.fill((0, 0, 0))  # 画面を黒色に塗りつぶし
    work_colision_map = copy.deepcopy(frame_list)  # 枠をワーク領域にディープコピー
    screen.fill((0, 0, 0))  # ウィンドウの背景色
    face_img = pygame.image.load("./img/mas_face.jpg")  #プレーヤの顔絵を読み込む
    put_img(screen, face_img, 400, 100)  # 画面に顔を置く

    # 乱数を使用して初期の猫の色を決める
    cat_color = random.randint(2, 7)

    # ココからメインのループ
    while (1):
        # 一番上まで埋まったかチェック
        ret_collision: bool = chek_collision(int(x1_pt / cat_size), int(y1_pt / cat_size), work_colision_map)
        if ret_collision:
            # 一番上まで埋まってたので、暫定的に枠内をクリア
            work_colision_map = copy.deepcopy(frame_list)  # ディープコピー
        put_frame(screen, work_colision_map)  # 画面に枠を置く
        time.sleep(0.2)  # 速度調整のsleep

        # キー入力など、イベント処理
        x1_pt, y1_pt = event_proc(x1_pt, y1_pt)

        y1_pt = y1_pt + cat_size  # ブロック落下

        # ブロック当たりチェック
        ret_collision: bool = chek_collision(int(x1_pt / cat_size), int(y1_pt / cat_size), work_colision_map)
        if ret_collision:
            y1_pt = y1_pt - cat_size  # 落下できなかったので戻す
            # ブロックの固定
            work_colision_map = set_block_list(int(x1_pt / cat_size), int(y1_pt / cat_size), cat_color, work_colision_map)
            # 並びブロックのチェックと削除
            work_colision_map, score = chek_delete_cat(int(x1_pt / cat_size), int(y1_pt / cat_size), work_colision_map, score)
            cat_color = random.randint(2, 7)  # 次の猫色を決める
            y1_pt = 0  # ぶつかったのでy座標をゼロに戻す
            put_frame(screen, work_colision_map)  # 画面に枠を置く

        # 閾値超えたら戻るように
        if y1_pt > 400:
            y1_pt = 0

        # 落ちてくるブロック（猫）を画面に置く
        put_drop_cat(screen, cat_color, x1_pt, y1_pt)

        ##pygame.display.flip()  # display Surface全体を更新して画面に描写します。
        pygame.display.update()  # スクリーンの一部分のみを更新します。この命令はソフトウェア側での表示処理に最適化されています。

        put_score(screen, score)  # スコアの表示


###################################
## スコアの表示
def put_score(screen, score):
    font = pygame.font.Font(None, 40)  # フォントの設定(55px)
    put_img(screen, get_block_img(0), 400, cat_size)  # スコア表示部分に黒ブロックを置いて消す
    put_img(screen, get_block_img(0), 450, cat_size)  # スコア表示部分に黒ブロックを置いて消す
    put_img(screen, get_block_img(0), 500, cat_size)  # スコア表示部分に黒ブロックを置いて消す
    screen.blit(font.render(str(score), True, (255, 255, 0)), [400, 50])  # 文字列の表示位置


###################################
## ブロックの削除対象チェックと削除
## ※この処理でブロックを決すためのルールロジックの処理を行う
## paramerter
##     x:落猫の横軸座標　y:落猫の縦軸座標
##     work_colision_map:当たり判定用の配列　score:点数
def chek_delete_cat(x, y, work_colision_map: list, score):
    if y > 6:
        # 底から2段目以下ならば3個並んでいないので即返る
        return work_colision_map, score
    elif y < 2:
        # 天から2段目以上ならば3個並んでいないので即返る
        return work_colision_map, score
    cat0 = work_colision_map[y][x]
    cat1 = work_colision_map[y + 1][x]
    cat2 = work_colision_map[y + 2][x]
    if (cat0 == cat1) and (cat1 == cat2):
        # 3個並んでる
        work_colision_map[y][x] = 0
        work_colision_map[y + 1][x] = 0
        work_colision_map[y + 2][x] = 0
        score = score + 3
    return work_colision_map, score


###################################
## ブロックの当たり判定　※簡易なので下しか見ていない。本来は横も見る
## paramerter
##     x:落猫の横軸座標　y:落猫の縦軸座標
##     work_colision_map:当たり判定用の配列
## ret    true:当たり  false:無し
def chek_collision(x, y, work_colision_map: list) -> bool:
    block = work_colision_map[y][x]
    print('block=', block)
    if block == 0:
        return False
    else:
        return True


###################################
## 着地したブロックを変数に書き込む
def set_block_list(x, y, cat_col, work_colision_map: list) -> list:
    work_colision_map[y][x] = cat_col
    return work_colision_map


###################################
## キー入力など、イベント処理
## 矢印キーでブロックの座標他仕込みも行う
def event_proc(x1_pt: int, y1_pt: int) -> object:
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
                x1_pt -= cat_size
            elif event.key == K_RIGHT:
                print("→")
                x1_pt += cat_size
            # elif event.key == K_UP:
            # print("↑")
            # y1_pt -= CatSize
            # elif event.key == K_DOWN:
            # print("↓")
            # y1_pt += CatSize
    #
    if x1_pt < 50:
        x1_pt = 50
    if x1_pt > 250:
        x1_pt = 250
    # 　座標のみ返す
    return x1_pt, y1_pt


###################################
##　指定のブロック絵柄（猫など）をイメージオブジェクトに入れて返す
def get_block_img(cat_color: int):
    if cat_color == 0:
        ret_img = pygame.image.load("./img/blank.png")  # 画像を読み込む(今回追加したとこ)
    elif cat_color == 1:
        ret_img = pygame.image.load("./img/block.png")  # 画像を読み込む(今回追加したとこ)
    elif cat_color == 2:
        ret_img = pygame.image.load("./img/neko0.png")  # 画像を読み込む(今回追加したとこ)
    elif cat_color == 3:
        ret_img = pygame.image.load("./img/neko1.png")  # 画像を読み込む(今回追加したとこ)
    elif cat_color == 4:
        ret_img = pygame.image.load("./img/neko2.png")  # 画像を読み込む(今回追加したとこ)
    elif cat_color == 5:
        ret_img = pygame.image.load("./img/neko3.png")  # 画像を読み込む(今回追加したとこ)
    elif cat_color == 6:
        ret_img = pygame.image.load("./img/neko4.png")  # 画像を読み込む(今回追加したとこ)
    elif cat_color == 7:
        ret_img = pygame.image.load("./img/neko5.png")  # 画像を読み込む(今回追加したとこ)
    else:
        ret_img = pygame.image.load("./img/block.png")  # 画像を読み込む(今回追加したとこ)
    return ret_img


###################################
##　落ちてくるブロック（猫）を画面に置く
def put_drop_cat(screen, cat_color: int, x1_pt, y1_pt):
    drop_cat_img = get_block_img(cat_color)
    screen.blit(drop_cat_img, (x1_pt, y1_pt))


###################################
##フレーム内を描き直す
def put_frame(screen, work_colision_map):
    # 枠のブロックを表示する。
    y_idx = 0
    for val1 in work_colision_map:
        x_idx = 0
        for val2 in val1:
            # idBlokck = list2[0][index2]
            id_blokck = int(val2)
            put_block(screen, get_block_img(id_blokck), x_idx, y_idx)
            x_idx += 1
        y_idx += 1


###################################
## 絵を表示する
def put_img(screen, img_obj, x, y):
    screen.blit(img_obj, (x, y, cat_size, cat_size))  # 絵を画面に貼り付ける


###################################
## ブロックを画面に置く ※50ドット単位(cat_size)
def put_block(screen, img_obj, x, y):
    screen.blit(img_obj, (cat_size * x, cat_size * y, cat_size, cat_size))  # 絵を画面に貼り付ける


###################################
## 画面に四角を書く
def put_rect(screen, x, y):
    RED = (255, 0, 0)
    rect = ((50 * x), (50 * y), 50, 50)
    pygame.draw.rect(screen, RED, rect)
    # screen.blit(font.render( in_chr, True, (255, 255, 0)), [(50 * x_idx), (40 * y_idx)])  # 文字列の表示位置


###################################
##　既定　これが無いと動かない    #############################
if __name__ == "__main__":
    main()
