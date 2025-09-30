import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect or ばくだんRect
    戻り値：判定結果タプル（横方向，縦方向）
    画面内ならTrue/画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right: #横方向にはみ出ていたら
        yoko = False
    if rct.top <0 or HEIGHT < rct.bottom: #縦方向にはみ出ていたら
        tate = False
    return yoko, tate

def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    kk_imgs = {}
    kk_img_normal = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 1.0)  # 元画像_左
    kk_img_hanten = pg.transform.flip(kk_img_normal, True, False)  # 反転画像_右
    
    kk_imgs[(0, 0)] = kk_img_normal  # 通常
    kk_imgs[(-5, -5)] = pg.transform.rotozoom(kk_img_normal, -45, 1.0) # 左上
    kk_imgs[(0, -5)] = pg.transform.rotozoom(kk_img_hanten, 90, 1.0) # 上
    kk_imgs[(+5, -5)] = pg.transform.rotozoom(kk_img_hanten, 45, 1.0) # 右上
    kk_imgs[(+5, 0)] = kk_img_hanten # 右
    kk_imgs[(+5, +5)] = pg.transform.rotozoom(kk_img_hanten, -45, 1.0) # 右下
    kk_imgs[(0, +5)] = pg.transform.rotozoom(kk_img_hanten, -90, 1.0) # 下
    kk_imgs[(-5, +5)] = pg.transform.rotozoom(kk_img_normal, +45, 1.0) # 左下
    
    return kk_imgs

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
        bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    kk_imgs = get_kk_imgs()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 爆弾用の空Surface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤い爆弾円
    bb_img.set_colorkey((0, 0, 0))  # 四隅の黒い部分を透過
    bb_rct = bb_img.get_rect()  # 爆弾Rect
    bb_rct.centerx = random.randint(0, WIDTH)  # 爆弾横座標
    bb_rct.centery = random.randint(0, HEIGHT)  # 爆弾縦座標
    vx, vy = +5, +5  # 爆弾の速度
    bb_imgs, bb_accs = init_bb_imgs()
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾の衝突判定
            return  # ゲームオーバー

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  # 横方向の移動量を加算
                sum_mv[1] += mv[1]  # 縦方向の移動量を加算
        # if key_lst[pg.K_w]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        kk_img = kk_imgs.get(tuple(sum_mv), kk_img)
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)  # 爆弾移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            vx *= -1  # 横方向速度を反転
        if not tate:  # 縦方向にはみ出ていたら
            vy *= -1  # 縦方向速度を反転
        screen.blit(bb_img, bb_rct)  # 爆弾描画
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_rct.move_ip(avx, avy)  # 爆弾移動
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()