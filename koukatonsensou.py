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

class Buff:
    """
    味方ユニットにバフを掛ける機能に関するクラス
    """
    def __init__(self,screen,cats):
        """
        画面内にいる味方ユニットの速度と与えるダメージを増加させる。また画面を緑に光らせる。
        引数 screen : 画面Surface
        引数2 cats : catsリスト
        """
        for cat in cats:
            cat.speed = 3  # スピードを3に変更
            cat.damege = 10  # 与えるダメージを10に変更
        buff_img = pg.Surface((WIDTH, HEIGHT)) 
        for i in range(20):
            pg.draw.rect(buff_img,(0,255,100),(0,0,WIDTH,HEIGHT))  # 画面全体が緑色に光る
            buff_img.set_alpha(8*(i+1))
            screen.blit(buff_img,[0,0])
            buff_timer = 0
            pg.display.update()
            time.sleep(0.01)


class BuffFont:
    """
    バフについて示す文字を表示するクラス
    """
    def __init__(self,screen,buff_timer,buff_st):
        """
        buff_stに代入されている文字列によってそれぞれ文字を画面に表示させる。
        """
        if buff_st == "yes":  # バフをかけられるか判定 
            buff_ok_font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体",30)  # fontでバフをかけられるかどうか示す(文字の描画)
            txt2 = buff_ok_font.render("bキーでバフ!",True, (0, 0, 0))
            buff_ok_rct = txt2.get_rect()
            buff_ok_rct.center = (105,40)
            screen.blit(txt2,buff_ok_rct)

        if buff_st == "no":  # バフをかけられるようになるまでの時間
            buff_no_font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体",20)  # fontでバフをかけられるかどうか示す(文字の描画)
            txt1 = buff_no_font.render(f"バフOKまで:{1200 - buff_timer}",True, (0, 0, 0))
            buff_no_rct = txt1.get_rect()
            buff_no_rct.center = (80,40)
            screen.blit(txt1,buff_no_rct)


class HeavyEnemy(BaseEnemyUnit):
    def __init__(self):
        super().__init__(WIDTH - 80, HEIGHT - 60, 150, 4, 0.3, "fig/tekikuma.png")

class FastEnemy(BaseEnemyUnit):
    def __init__(self):
        super().__init__(WIDTH - 80, HEIGHT - 60, 30, 1, 1.2, "fig/tekitaka.png")
buff_st = "no"


# メインループ
def main():
    # リスト
    cats = []
    enemies = []

    # タイマー
    enemy_spawn_timer = 0
    # バフをかけられるようになるまでのタイマー
    buff_timer = 0  # テストのため今は1000で設定
    buff_st = "no"

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


                if event.key == pg.K_b:  # bキーを押したらバフ
                    if buff_st == "yes":   
                        Buff(screen,cats)
                        buff_st = "no"
        screen.blit(bg_img, [0, 0])

        buff_timer += 1  # 1/60秒に1増加
        if buff_timer > 1200:  # 20秒ごとにバフをかけられるようにする。
            buff_st = "yes"
            print("テストテストテスト")
            buff_timer = 0  # タイマーリセット
        BuffFont(screen,buff_timer,buff_st)


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
