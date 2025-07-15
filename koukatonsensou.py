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


def draw_text(screen, text, size, x, y, color):
    font = pg.font.Font(None, size)
    font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 28)
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(x, y))
    screen.blit(surf, rect)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)
    return text_rect

def title_screen(screen):
    while True:
        screen.fill(((0, 0, 0)))
        draw_text(screen, "こうかとん大戦争", 64, WIDTH / 2, HEIGHT / 4, (255, 255, 255))
        play_button = draw_text(screen, "プレイ", 48, WIDTH / 2, HEIGHT / 2, (255, 255, 255))
        how_to_play_button = draw_text(screen, "あそびかた", 48, WIDTH / 2, HEIGHT / 2 + 60, (255, 255, 255))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "quit"
            if event.type == pg.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return "play"
                if how_to_play_button.collidepoint(event.pos):
                    return "how_to_play"
                
        pg.display.update()

def how_to_play_screen(screen):
    while True:
        screen.fill((0, 0, 0))
        draw_text(screen, "スペースキーを押して、味方を出撃させてね！", 36, WIDTH / 2, HEIGHT / 3, (255, 255, 255))

        back_button = draw_text(screen, "もどる", 48, WIDTH / 2, HEIGHT * 2 / 3, (255, 255, 255))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "quit"
            if event.type == pg.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return "title"
                
        pg.display.update()
        



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
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("こうかとん大戦争")

    game_state = "title"

    while True:
        if game_state == "title":
            result = title_screen(screen)
            if result == "play":
                game_state = "play"
            elif result == "how_to_play":
                game_state = "how_to_play"
            elif result == "quit":
                break

        elif game_state == "how_to_play":
            result = how_to_play_screen(screen)
            if result == "title":
                game_state = "title"
            elif result == "quit":
                break

        elif game_state == "play":
            main()
            break
    pg.quit()
    sys.exit()
