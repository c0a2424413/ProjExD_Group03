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
