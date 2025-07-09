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
        self.width = 30
        self.height = 30
        self.hp = 100
        self.speed = 1
        self.damage = 5
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.x += self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        pg.draw.rect(self.screen, (200, 200, 255), self.rect)
        

class EnemyUnit:
    def __init__(self):
        self.x = WIDTH - 80
        self.y = HEIGHT - 60
        self.width = 30
        self.height = 30
        self.hp = 50
        self.speed = 0.5
        self.damage = 2
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.x -= self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        pg.draw.rect(self.screen, (255, 100, 100), self.rect)


class Castle:
    """
    敵味方の城オブジェクトの設定
    """
    def __init__(self, image, position, hp):
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
        self.hp = hp
        self.destroyed = False

    def draw(self, screen, font):
        screen.blit(self.image, self.rect)
        hp_text1 = font.render(f"{self.hp}", True, (0, 0, 255))
        hp_rect1 = hp_text1.get_rect(center=(self.rect.centerx, self.rect.top - 20))
        screen.blit(hp_text1, hp_rect1)
        # hp_text2 = font.render(f"{self.hp}", True, (255, 0, 0))
        # hp_rect2 = hp_text2.get_rect(center=(self.rect.centerx, self.rect.top - 20))
        # screen.blit(hp_text2, hp_rect2)
        

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.destroyed = True


class EndingManager:
    """
    こうかとん城と反こうかとん城を表示
    どちらかの城の耐久値が０になったときに、爆破エフェクトを出す
    味方の耐久値が０の時はゲームオーバー、敵の耐久値が０の時はゲームクリアを表示
    数秒後、ゲームを終了する
    """
    def __init__(self, screen, explosion_img, font):
        self.screen = screen
        self.explosion_img = explosion_img
        self.font = font
        self.ended = False
        self.end_time = None
        self.message = ""
        self.koka_img = None
        self.explosion_pos = None

    def trigger_ending(self, castle, message, koka_img):
        self.message = message
        self.koka_img = koka_img
        self.explosion_pos = castle.rect.center
        self.end_time = time.time()
        self.ended = True

    def draw_ending(self):
        if not self.ended:
            return

        # 爆破エフェクト
        explosion_rect = self.explosion_img.get_rect(center=self.explosion_pos)
        self.screen.blit(self.explosion_img, explosion_rect)

        # テキスト
        text = self.font.render(self.message, True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)

        # 両脇のこうかとん
        left_koka_rect = self.koka_img.get_rect(midright=(text_rect.left - 20, text_rect.centery))
        right_koka_rect = self.koka_img.get_rect(midleft=(text_rect.right + 20, text_rect.centery))
        self.screen.blit(self.koka_img, left_koka_rect)
        self.screen.blit(self.koka_img, right_koka_rect)

    def check_exit(self):
        if self.ended and time.time() - self.end_time >= 3:
            pg.quit()
            sys.exit()


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

    castle1 = pg.image.load("fig/hachioji.png")
    castle2 = pg.image.load("fig/kamata.png")
    exp = pg.image.load("fig/explosion.gif")
    koka_smile_img = pg.image.load("fig/6.png")
    koka_cry_img = pg.image.load("fig/8.png")
    font = pg.font.Font(None, 80)

    koukaton_castle = Castle(castle1, (0, 270), 10)
    hankoukaton_castle = Castle(castle2, (WIDTH-100, 270), 10)

    ending_manager = EndingManager(screen, exp, font)

    
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

        # 城との衝突判定
        for cat in cats[:]:
            if cat.rect.colliderect(hankoukaton_castle.rect):
                hankoukaton_castle.take_damage(1)
                cats.remove(cat)

        for enemy in enemies[:]:
            if enemy.rect.colliderect(koukaton_castle.rect):
                koukaton_castle.take_damage(1)
                enemies.remove(enemy)


        # エンディング発動
        if koukaton_castle.destroyed and not ending_manager.ended:
            ending_manager.trigger_ending(koukaton_castle, "GAME OVER", koka_smile_img)
        elif hankoukaton_castle.destroyed and not ending_manager.ended:
            ending_manager.trigger_ending(hankoukaton_castle, "GAME CLEAR", koka_cry_img)

        # 城を描画
        koukaton_castle.draw(screen, font)
        hankoukaton_castle.draw(screen, font)

        ending_manager.draw_ending()
        ending_manager.check_exit()

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
