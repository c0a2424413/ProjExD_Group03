import os
import pygame
import random
import time


os.path.dirname(os.path.abspath(__file__))
# 初期化
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("にゃんこ大戦争風ゲーム")
clock = pygame.time.Clock()

# 色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ユニットの設定
class CatUnit:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT - 60
        self.hp = 100
        self.speed = 1
        self.damage = 5

    def move(self):
        self.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, (200, 200, 255), (self.x, self.y, 30, 30))

class EnemyUnit:
    def __init__(self):
        self.x = WIDTH - 80
        self.y = HEIGHT - 60
        self.hp = 50
        self.speed = 0.5
        self.damage = 2

    def move(self):
        self.x -= self.speed

    def draw(self):
        pygame.draw.rect(screen, (255, 100, 100), (self.x, self.y, 30, 30))


class Buff:
    """
    味方ユニットにバフを掛ける機能に関するクラス
    """
    def __init__(self,cats,screen):
        """
        画面内にいる味方ユニットの速度と与えるダメージを増加させる。また画面を緑に光らせる。
        引数 screen : 画面Surface
        引数2 cats : catsリスト
        """
        for cat in cats:
            cat.speed = 3  # スピードを3に変更
            cat.damege = 10  # 与えるダメージを10に変更
        buff_img = pygame.Surface((WIDTH, HEIGHT)) 
        for i in range(20):
            pygame.draw.rect(buff_img,(0,255,100),(0,0,WIDTH,HEIGHT))  # 画面全体が緑色に光る
            buff_img.set_alpha(8*(i+1))
            screen.blit(buff_img,[0,0])
            buff_timer = 0
            pygame.display.update()
            time.sleep(0.01)


class BuffFont:
    """
    バフについて示す文字を表示するクラス
    """
    def __init__(self):
        """
        buff_stに代入されている文字列によってそれぞれ文字を画面に表示させる。
        """
        if buff_st == "yes":  # バフをかけられるか判定 
            buff_ok_font = pygame.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体",30)  # fontでバフをかけられるかどうか示す(文字の描画)
            txt2 = buff_ok_font.render("bキーでバフ!",True, (0, 0, 0))
            buff_ok_rct = txt2.get_rect()
            buff_ok_rct.center = (105,40)
            screen.blit(txt2,buff_ok_rct)

        if buff_st == "no":  # バフをかけられるようになるまでの時間
            buff_no_font = pygame.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体",20)  # fontでバフをかけられるかどうか示す(文字の描画)
            txt1 = buff_no_font.render(f"バフOKまで:{1200 - buff_timer}",True, (0, 0, 0))
            buff_no_rct = txt1.get_rect()
            buff_no_rct.center = (80,40)
            screen.blit(txt1,buff_no_rct)


# リスト
cats = []  # buffクラスで使用(catsを)
enemies = []

# タイマー
enemy_spawn_timer = 0

# バフをかけられるようになるまでのタイマー
buff_timer = 1000  # テストのため今は1000で設定
buff_st = "no"

# メインループ
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 味方ユニット出撃
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                cats.append(CatUnit())

        if event.type == pygame.KEYDOWN:
                if buff_st == "yes":                 
                    if event.key == pygame.K_b:  # bキーを押したらバフ
                        Buff(cats,screen)
                        buff_st = "no"

    # 敵を定期的に出す
    enemy_spawn_timer += 1
    if enemy_spawn_timer > 120:  # 2秒ごとに敵を出す
        enemies.append(EnemyUnit())
        enemy_spawn_timer = 0

    buff_timer += 1  # 1/60秒に1増加
    if buff_timer > 1200:  # 20秒ごとにバフをかけられるようにする。
        buff_st = "yes"
        buff_timer = 0  # タイマーリセット
    BuffFont()

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

    pygame.display.update()
    clock.tick(60)

pygame.quit()
