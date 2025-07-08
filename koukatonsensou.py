import os
import random
import sys
import time
import pygame as pg


os.chdir(os.path.dirname(os.path.abspath(__file__)))
WIDTH, HEIGHT = 800, 400
# ユニットの設定
class CatUnit:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT - 60
        self.hp = 100
        self.speed = 1
        self.damage = 5
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))

    def move(self):
        self.x += self.speed

    def draw(self):
        pg.draw.rect(self.screen, (200, 200, 255), (self.x, self.y, 30, 30))

class EnemyUnit:
    def __init__(self):
        self.x = WIDTH - 80
        self.y = HEIGHT - 60
        self.hp = 50
        self.speed = 0.5
        self.damage = 2
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))

    def move(self):
        self.x -= self.speed

    def draw(self):
        pg.draw.rect(self.screen, (255, 100, 100), (self.x, self.y, 30, 30))


class Balse:
    """
    こうかとん城と反こうかとん城を表示
    どちらかの城の耐久値が０になったときに、爆破エフェクトを出す
    味方の耐久値が０の時はゲームオーバー、敵の耐久値が０の時はゲームクリアを表示
    数秒後、ゲームを終了する
    """
    def __init__(self, obj: "CatUnit|EnemyUnit", life: int):
        self.x = 10
        self.y = HEIGHT - 20
        self.image = self.imgs1[0]
        self.image = self.imgs2[0]
        self.rect = self.image.get_rect(center=obj.rect.center)
        self.life = life

    def gameover(screen: pg.Surface) -> None: 
        # ブラックアウト
        img = pg.Surface((WIDTH, HEIGHT))
        pg.draw.rect(img,(0,0,0),pg.Rect(0,0,WIDTH,HEIGHT))
        img.set_alpha(200)
        screen.blit(img,[0,0])
        # 泣いているこうかとん一枚目
        img = pg.image.load("fig/8.png")
        bg_rct1 = img.get_rect()
        bg_rct1.center = 800,320
        # 泣いているこうかとん二枚目
        img = pg.image.load("fig/8.png")
        bg_rct2 = img.get_rect()
        bg_rct2.center = 300,320
        # GameOverのサイズと色 
        fonto = pg.font.Font(None,80)
        txt = fonto.render("Game Over",True,(255,255,255))
        # 上記表示
        screen.blit(img,bg_rct1)
        screen.blit(img,bg_rct2)
        screen.blit(txt,[400,300])
        pg.display.update()  # 更新
        time.sleep(5)  # 5秒間
        return



# メインループ
def main():
    # リスト
    cats = []
    enemies = []

    # タイマー
    enemy_spawn_timer = 0
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("こうかとん大戦争")
    clock = pg.time.Clock()
    bg_img = pg.image.load("fig/umi.png") #背景画像のサーフェイス

    img1 = pg.image.load("fig/八王子キャンパス.png")
    img2 = pg.image.load("fig/蒲田キャンパス.png")



    
    while True:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

            # にゃんこ出撃
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    cats.append(CatUnit())

        screen.blit(bg_img, [0, 0])

        # 敵を定期的に出す
        enemy_spawn_timer += 1
        if enemy_spawn_timer > 120:  # 2秒ごとに敵を出す
            enemies.append(EnemyUnit())
            enemy_spawn_timer = 0

        # ユニットの動き・描画
        for cat in cats:
            cat.move()
            cat.draw()

        for enemy in enemies:
            enemy.move()
            enemy.draw()

        # 簡易バトル処理
        for cat in cats:
            for enemy in enemies:
                if abs(cat.x - enemy.x) < 30:
                    enemy.hp -= cat.damage
                    cat.hp -= enemy.damage
                
        if catcassle >= 0:
            gameover(screen)
            return
        
        if enemycassle >= 0:
            gameclear(screen)
            return

        # 死亡処理
        cats = [c for c in cats if c.hp > 0]
        enemies = [e for e in enemies if e.hp > 0]

        pg.display.update()
        clock.tick(60)
        screen.blit(bg_img,[0,0])

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
