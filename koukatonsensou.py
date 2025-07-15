import os
import random
import sys
import time
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))
WIDTH, HEIGHT = 800, 400


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


class DefenseCannon:
    """こうかとん砲に関するクラス"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 80
        self.height = 30
        self.cooldown = 0
        self.max_cooldown = 300  # 5秒
        self.fire_text_timer = 0
        self.image = pg.image.load("fig/beam.png")
        self.image = pg.transform.scale(self.image, (self.width, self.height))

    def draw(self, screen: pg.Surface):
        screen.blit(self.image, (self.x, self.y))
        if self.fire_text_timer > 0:
            font = pg.font.SysFont(None, 36)
            fire_text = font.render("FIRE", True, (255, 150, 50))
            fire_rect = fire_text.get_rect(center=(self.x + self.width // 2, self.y - 30))
            screen.blit(fire_text, fire_rect)
            self.fire_text_timer -= 1

        if self.cooldown > 0:
            font = pg.font.SysFont(None, 20)
            cd_text = font.render(f"{self.cooldown // 60}s", True, (255, 255, 255))
            screen.blit(cd_text, (self.x + (self.width - cd_text.get_width()) // 2, self.y - 20))
            pg.draw.rect(screen, (50, 50, 50), (self.x, self.y - 15, self.width, 5))
            pg.draw.rect(screen, (0, 200, 0), (self.x, self.y - 15,
                            self.width * (1 - self.cooldown / self.max_cooldown), 5))


class Castle:
    """
    敵味方の城オブジェクトの設定
    """
    def __init__(self, image, position, hp, color):
        self.image = image  # 城画像
        self.rect = self.image.get_rect(topleft=position)  # 配置場所
        self.hp = hp  # 耐久値
        self.color = color  # hpの色
        self.destroyed = False  # 破壊判定

    def draw(self, screen, font):
        screen.blit(self.image, self.rect)  # 城画像の描画
        hp_text = font.render(f"{self.hp}", True, self.color)  # HPテキスト
        hp_rect = hp_text.get_rect(center=(self.rect.centerx, self.rect.top - 20))
        screen.blit(hp_text, hp_rect)  # HPを城の上に表示

    def take_damage(self, amount):
        self.hp -= amount  # ダメージを受ける
        if self.hp <= 0:  # HPが0以下の時、耐久値を0にして城陥落
            self.hp = 0
            self.destroyed = True


class EndingManager:
    """
    エンディング時に起こるイベントの設定
    """
    def __init__(self, screen, explosion_img, font):
        self.screen = screen
        self.explosion_img = explosion_img  # 爆破画像
        self.font = font
        self.ended = False  # エンディング状態
        self.end_time = None  # 終了タイム
        self.message = ""  # エンディングメッセージ
        self.koka_img = None  # こうかとんの画像

    def trigger_ending(self, castle, message, koka_img):
        self.message = message  # エンディングメッセージ
        self.koka_img = koka_img  # こうかとんの画像
        self.explosion_pos = castle.rect.center  # 爆発の位置
        self.end_time = time.time()  # エンディング開始時間
        self.ended = True  # エンディング状態にする

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

        # 両端のこうかとん
        left_koka_rect = self.koka_img.get_rect(midright=(text_rect.left - 20, text_rect.centery))
        right_koka_rect = self.koka_img.get_rect(midleft=(text_rect.right + 20, text_rect.centery))
        self.screen.blit(self.koka_img, left_koka_rect)
        self.screen.blit(self.koka_img, right_koka_rect)

    def check_exit(self):
        # エンディング後、3秒後にゲーム終了
        if self.ended and time.time() - self.end_time >= 3:
            pg.quit()
            sys.exit()


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
        if buff_st == "yes":   # バフをかけられるか判定
            buff_ok_font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体",30)   # fontでバフをかけられるかどうか示す(文字の描画)
            txt2 = buff_ok_font.render("bキーでバフ!",True, (0, 0, 0))
            buff_ok_rct = txt2.get_rect()
            buff_ok_rct.center = (105,40)
            screen.blit(txt2,buff_ok_rct)
        if buff_st == "no":    # バフをかけられるようになるまでの時間
            buff_no_font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体",20)   # fontでバフをかけられるかどうか示す(文字の描画)
            txt1 = buff_no_font.render(f"バフOKまで:{1200 - buff_timer}",True, (0, 0, 0))
            buff_no_rct = txt1.get_rect()
            buff_no_rct.center = (80,40)
            screen.blit(txt1,buff_no_rct)

def draw_text(screen, text, size, x, y, color):
    font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 28)
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(x, y))
    screen.blit(surf, rect)
    return rect

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


def main():
    cats = []
    enemies = []
    enemy_spawn_timer = 0
    buff_timer = 0
    buff_st = "no"
    fail_image_timer = 0

    castle1 = pg.image.load("fig/hachioji.png")  # 味方城
    castle2 = pg.image.load("fig/kamata.png")  # 敵城
    exp = pg.image.load("fig/explosion.gif")  # 爆発画像
    koka_smile_img = pg.image.load("fig/8.png")  # 喜んでいるこうかとん画像
    koka_cry_img = pg.image.load("fig/6.png")  # 泣いているこうかとん画像
    font = pg.font.Font(None, 80)  # フォント設定

    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("こうかとん大戦争")
    clock = pg.time.Clock()
    bg_img = pg.image.load("fig/umi.png")    #背景画像のサーフェイス
    fail_image = pg.image.load("fig/8.png")  # ← 加载失败图像
    fail_image = pg.transform.scale(fail_image, (100, 100))

    # 味方と敵城の初期設定
    koukaton_castle = Castle(castle1, (0, 270), 10, (0, 0 ,255))  # 味方城の設定
    hankoukaton_castle = Castle(castle2, (WIDTH-100, 270), 10, (255, 0, 0))  # 敵城の設定

    ending_manager = EndingManager(screen, exp, font)  # エンディングの管理

    cannon = DefenseCannon(10 + 40 - 40, HEIGHT - 90 - 65)       # 防御砲初期化

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            # スペースキーでにゃんこ出撃
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    cats.append(NormalCat())
                elif event.key == pg.K_a:
                    cats.append(TankCat())
                elif event.key == pg.K_s:
                    cats.append(SpeedCat())


                elif event.key == pg.K_b:    # bキーを押したらバフ
                    if buff_st == "yes":
                        Buff(screen, cats)
                        buff_st = "no"
                elif event.key == pg.K_LSHIFT and cannon.cooldown <= 0:
                    if random.random() < 0.1:
                        fail_image_timer = 60
                    else:
                        for _ in range(min(3, len(enemies))):
                            enemies.pop(0)
                        cannon.fire_text_timer = 60
                    cannon.cooldown = cannon.max_cooldown

        screen.blit(bg_img, [0, 0])

        buff_timer += 1
        if buff_timer > 1200:
            buff_st = "yes"
            buff_timer = 0
        BuffFont(screen, buff_timer, buff_st)

        enemy_spawn_timer += 1
        if enemy_spawn_timer > 120:
            rand = random.randint(0, 9)
            if rand < 6:
                enemies.append(NormalEnemy())
            elif rand < 9:
                enemies.append(HeavyEnemy())
            else:
                enemies.append(FastEnemy())
            enemy_spawn_timer = 0

        for cat in cats:
            cat.move()
            cat.draw(screen)

        for enemy in enemies:
            enemy.move()
            enemy.draw(screen)

        for cat in cats:
            for enemy in enemies:
                if abs(cat.x - enemy.x) < 30:
                    enemy.hp -= cat.damage
                    cat.hp -= enemy.damage

        # 城との衝突判定　味方→敵城、敵→味方城の衝突時にユニットが消える
        for cat in cats[:]:
            if cat.rct.colliderect(hankoukaton_castle.rect):
                hankoukaton_castle.take_damage(1)
                cats.remove(cat)

        for enemy in enemies[:]:
            if enemy.rct.colliderect(koukaton_castle.rect):
                koukaton_castle.take_damage(1)
                enemies.remove(enemy)


        # エンディング発動　味方城陥落→ゲームオーバー、敵城陥落→ゲームクリア
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

        if cannon.cooldown > 0:
            cannon.cooldown -= 1

        cannon.draw(screen) 

        if fail_image_timer > 0:
            screen.blit(fail_image, (WIDTH//2 - fail_image.get_width()//2, HEIGHT//2 - fail_image.get_height()//2))
            fail_image_timer -= 1

        pg.display.update()
        clock.tick(60)


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
