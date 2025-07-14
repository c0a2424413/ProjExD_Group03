import os
import random
import sys
import time
import pygame as pg


os.chdir(os.path.dirname(os.path.abspath(__file__)))
WIDTH, HEIGHT = 800, 400

# ユニットの設定
class CatUnit:
    """
    味方ユニットの設定
    """
    def __init__(self):
        self.x = 50  # 初期x座標
        self.y = HEIGHT - 60  # 初期y座標
        self.width = 30  # 幅
        self.height = 30  # 高さ
        self.hp = 100  # HP(体力)
        self.speed = 1  # 移動速度
        self.damage = 5  # 攻撃力
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)  # 当たり判定の設定

    def move(self):
        self.x += self.speed  # 右への移動
        self.rect.topleft = (self.x, self.y)  # Rectを更新

    def draw(self):
        pg.draw.rect(self.screen, (200, 200, 255), self.rect)  # 味方ユニットの見た目　青四角
        

class EnemyUnit:
    """
    敵ユニットの設定
    """
    def __init__(self):
        self.x = WIDTH - 80  # 初期x座標
        self.y = HEIGHT - 60  # 初期y座標
        self.width = 30  # 幅
        self.height = 30  # 高さ
        self.hp = 50  # HP(体力)
        self.speed = 0.5  # 移動速度
        self.damage = 2  # 攻撃力
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)  # 当たり判定の設定　赤四角

    def move(self):
        self.x -= self.speed  # 左への移動
        self.rect.topleft = (self.x, self.y)  # Rectの更新

    def draw(self):
        pg.draw.rect(self.screen, (255, 100, 100), self.rect)  # 敵ユニットの見た目


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
    bg_img = pg.image.load("fig/umi.png") # 背景画像のサーフェイス

    castle1 = pg.image.load("fig/hachioji.png")  # 味方城
    castle2 = pg.image.load("fig/kamata.png")  # 敵城
    exp = pg.image.load("fig/explosion.gif")  # 爆発画像
    koka_smile_img = pg.image.load("fig/8.png")  # 喜んでいるこうかとん画像
    koka_cry_img = pg.image.load("fig/6.png")  # 泣いているこうかとん画像
    font = pg.font.Font(None, 80)  # フォント設定

    # 味方と敵城の初期設定
    koukaton_castle = Castle(castle1, (0, 270), 10, (0, 0 ,255))  # 味方城の設定
    hankoukaton_castle = Castle(castle2, (WIDTH-100, 270), 10, (255, 0, 0))  # 敵城の設定

    ending_manager = EndingManager(screen, exp, font)  # エンディングの管理

    
    while True:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

            # スペースキーでにゃんこ出撃
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

        # 城との衝突判定　味方→敵城、敵→味方城の衝突時にユニットが消える
        for cat in cats[:]:
            if cat.rect.colliderect(hankoukaton_castle.rect):
                hankoukaton_castle.take_damage(1)
                cats.remove(cat)

        for enemy in enemies[:]:
            if enemy.rect.colliderect(koukaton_castle.rect):
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

        pg.display.update()
        clock.tick(60)
        screen.blit(bg_img,[0,0])

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
