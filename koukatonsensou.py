import os
import random
import sys
import time
import pygame as pg


os.chdir(os.path.dirname(os.path.abspath(__file__)))
WIDTH, HEIGHT = 800, 400
# ユニットの設定


class BaseCatUnit:
    def __init__(self, x, y, hp, damage, speed, image_path):
        self.x = x
        self.y = y
        self.hp = hp
        self.damage = damage
        self.speed = speed
        self.img = pg.image.load(image_path)
        self.img = pg.transform.flip(self.img, True, False)
        self.rct = self.img.get_rect()
        self.rct.center = (self.x, self.y)

    def move(self):
        self.x += self.speed
        self.rct.centerx = self.x

    def draw(self, screen: pg.Surface):
        screen.blit(self.img, self.rct)

# 各キャラの定義
class NormalCat(BaseCatUnit):
    def __init__(self):
        super().__init__(50, HEIGHT - 60, 100, 5, 1, "fig/5.png")

class TankCat(BaseCatUnit):
    def __init__(self):
        super().__init__(50, HEIGHT - 60, 300, 2, 0.5, "fig/9.png")

class SpeedCat(BaseCatUnit):
    def __init__(self):
        super().__init__(50, HEIGHT - 60, 50, 8, 2, "fig/3.png")

class BaseEnemyUnit:
    def __init__(self, x, y, hp, damage, speed, image_path):
        self.x = x
        self.y = y
        self.hp = hp
        self.damage = damage
        self.speed = speed
        self.img = pg.image.load(image_path)
        self.img =  pg.transform.flip(self.img, True, False)
        self.img = pg.transform.scale(self.img, (100,100))
        self.rct = self.img.get_rect()
        self.rct.center = self.x , self.y
        

    def move(self):
        self.x -= self.speed
        self.rct.centerx = self.x 

    def draw(self, screen: pg.Surface):
        screen.blit(self.img, self.rct)

class NormalEnemy(BaseEnemyUnit):
    def __init__(self):
        super().__init__(WIDTH - 80, HEIGHT - 60, 50, 2, 0.5, "fig/tekikyara.png")

class HeavyEnemy(BaseEnemyUnit):
    def __init__(self):
        super().__init__(WIDTH - 80, HEIGHT - 60, 150, 4, 0.3, "fig/tekikuma.png")

class FastEnemy(BaseEnemyUnit):
    def __init__(self):
        super().__init__(WIDTH - 80, HEIGHT - 60, 30, 1, 1.2, "fig/tekitaka.png")

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

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    cats.append(NormalCat())
                elif event.key == pg.K_a:
                    cats.append(TankCat())
                elif event.key == pg.K_s:
                    cats.append(SpeedCat())

        screen.blit(bg_img, [0, 0])

        # 敵を定期的に出す
        enemy_spawn_timer += 1
        if enemy_spawn_timer > 120:
    # ランダムに敵を選ぶ
            rand = random.randint(0, 9)
            if rand < 6:
                enemies.append(NormalEnemy())
            elif rand < 9:
                enemies.append(HeavyEnemy())
            else:
                enemies.append(FastEnemy())

            enemy_spawn_timer = 0

        # ユニットの動き・描画
        for cat in cats:
            cat.move()
            cat.draw(screen)

        for enemy in enemies:
            enemy.move()
            enemy.draw(screen)

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
