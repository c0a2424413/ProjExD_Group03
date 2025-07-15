import os                  
import pygame              
import random              
import sys                 

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --- ゲーム初期化と画面設定 ---
pygame.init()                                      # Pygameの初期化
WIDTH, HEIGHT = 800, 400                           # 画面サイズを定義
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 画面を生成
pygame.display.set_caption("こうかとん大戦争")      # タイトルを設定
clock = pygame.time.Clock()                        # フレームレート管理

# --- 色の定義  ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 100, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 150, 50)

# --- 画像読み込み関数 ---
def load_image(name, scale=1.0):
    path = os.path.join("fig", name)                  # figフォルダ内の画像パスを構築
    image = pygame.image.load(path)                   # 画像読み込み
    if scale != 1.0:                                  # スケール指定がある場合
        new_size = (int(image.get_width() * scale), 
                    int(image.get_height() * scale))  # 新しいサイズを計算
        image = pygame.transform.scale(image, new_size)  # 画像をリサイズ
    return image


class CatUnit:
    """プレイヤーのユニットクラス"""
    def __init__(self):
        self.x = 50                                   # 初期位置X
        self.y = HEIGHT - 80                          # 地面のY座標に配置
        self.hp = 100                                 # 体力
        self.max_hp = 100
        self.speed = 1                                # 移動速度
        self.damage = 5                               # ダメージ
        self.image = load_image("2.png", 0.7)         # 画像読み込み

    def move(self):
        self.x += self.speed                          # 毎フレーム右へ移動

    def draw(self):
        screen.blit(self.image, (self.x, self.y))     # ユニット画像を描画
        pygame.draw.rect(screen, (200, 0, 0), (self.x, self.y - 10, 30, 5))  # HPバー背景
        pygame.draw.rect(screen, (0, 200, 0), (self.x, self.y - 10, 30 * (self.hp / self.max_hp), 5))  # 残HP


class EnemyUnit:
    """敵ユニットクラス"""
    def __init__(self):
        self.x = WIDTH - 80                           
        self.y = HEIGHT - 80
        self.hp = 50
        self.max_hp = 50
        self.speed = 1
        self.damage = 2
        self.image = load_image("alien1.png", 0.7)

    def move(self):
        self.x -= self.speed                          # 左に移動

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        pygame.draw.rect(screen, (200, 0, 0), (self.x, self.y - 10, 30, 5))
        pygame.draw.rect(screen, (0, 200, 0), (self.x, self.y - 10, 30 * (self.hp / self.max_hp), 5))


class BaseCamp:
    """大本営クラス"""
    def __init__(self, x, y, is_player):
        self.x = x
        self.y = y
        self.hp = 1000      #大本営hp
        self.max_hp = 1000
        self.is_player = is_player
        self.image = load_image("my.png") if is_player else load_image("you.png")
        self.width = 80
        self.height = 80

    def draw(self):
        screen.blit(self.image, (self.x, self.y))                      # 大本営画像
        bar_width = 100
        bar_x = self.x + (self.width - bar_width) // 2
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, self.y - 20, bar_width, 10))  # 背景バー
        color = (0, 200, 0) if self.hp > 500 else (200, 200, 0) if self.hp > 200 else (200, 0, 0)
        pygame.draw.rect(screen, color, (bar_x, self.y - 20, bar_width * (self.hp / self.max_hp), 10))  # HPバー

        font = pygame.font.SysFont(None, 24)
        label = font.render("Player Base" if self.is_player else "Enemy Base", True, BLUE if self.is_player else RED)
        screen.blit(label, (self.x + (self.width - label.get_width()) // 2, self.y - 40))


class DefenseCannon:
    """こうかとん砲クラス"""
    def __init__(self, base):
        self.base = base
        self.cooldown = 0
        self.max_cooldown = 300                            # 5秒クールダウン
        self.image = load_image("beam.png", 0.9)
        self.width = 80
        self.height = 30
        self.fire_text_timer = 0

    def draw(self):
        cannon_x = self.base.x + (self.base.width - self.width) // 2
        cannon_y = self.base.y - 65
        screen.blit(self.image, (cannon_x, cannon_y))      # 砲台画像表示

        if self.fire_text_timer > 0:
            font = pygame.font.SysFont(None, 36)
            fire_text = font.render("FIRE", True, ORANGE)
            text_rect = fire_text.get_rect(center=(self.base.x + self.base.width//2, self.base.y - 70))
            screen.blit(fire_text, text_rect)
            self.fire_text_timer -= 1

        if self.cooldown > 0:
            font = pygame.font.SysFont(None, 20)
            cooldown_text = font.render(f"{self.cooldown//60}s", True, WHITE)
            screen.blit(cooldown_text, (cannon_x + (self.width - cooldown_text.get_width()) // 2, cannon_y - 20))
            pygame.draw.rect(screen, (50, 50, 50), (cannon_x, cannon_y - 15, self.width, 5))
            pygame.draw.rect(screen, (0, 200, 0), (cannon_x, cannon_y - 15,
                                                   self.width * (1 - self.cooldown/self.max_cooldown), 5))


class GameState:
    """ゲーム状態定義"""
    RUNNING = 0
    PLAYER_WIN = 1
    PLAYER_LOSE = 2

Koukatons = []                           # 味方ユニットリスト
enemies = []                        # 敵ユニットリスト

try:
    background_img = load_image("umi.png")                         # 背景画像
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
except:
    background_img = pygame.Surface((WIDTH, HEIGHT))               # 単色背景
    background_img.fill((100, 150, 255))


player_base = BaseCamp(10, HEIGHT - 90, True)
enemy_base = BaseCamp(WIDTH - 90, HEIGHT - 90, False)
cannon = DefenseCannon(player_base)        #大本営と防御砲の生成


enemy_spawn_timer = 0
fail_image_timer = 0
fail_image = load_image("8.png")
game_state = GameState.RUNNING    #タイマーなどの初期化


running = True    #メインループ開始
frame_count = 0
while running:
    screen.blit(background_img, (0, 0))                         # 背景描画
    pygame.draw.rect(screen, (100, 200, 100), (0, HEIGHT - 20, WIDTH, 20))  # 地面

    # タイトルと説明
    font_title = pygame.font.SysFont(None, 48)
    title = font_title.render("Koukaton War", True, (50, 50, 150))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 10))
    
    font_help = pygame.font.SysFont(None, 24)
    help_text = [
        "SPACE: Koukaton sortie",
        "L-SHIFT: Defensive Cannon Fire (5 second cooldown)",
        "ESC: game over"
    ]
    for i, text in enumerate(help_text):
        screen.blit(font_help.render(text, True, BLACK), (10, 60 + i * 25))

    # 終了画面
    if game_state != GameState.RUNNING:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        font_large = pygame.font.SysFont(None, 72)
        font_small = pygame.font.SysFont(None, 36)
        if game_state == GameState.PLAYER_WIN:
            result_text = font_large.render("VICTORY!", True, YELLOW)
            message = font_small.render("Congratulations! You destroyed the enemy base!", True, WHITE)
        else:
            result_text = font_large.render("DEFEAT!", True, RED)
            message = font_small.render("Your base has been destroyed...", True, WHITE)
        screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, HEIGHT//2 - 60))
        screen.blit(message, (WIDTH//2 - message.get_width()//2, HEIGHT//2 + 20))
        screen.blit(font_small.render("Press R to restart or ESC to quit", True, GREEN),
                    (WIDTH//2 - 160, HEIGHT//2 + 80))

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_state != GameState.RUNNING:
                if event.key == pygame.K_r:
                    # 再スタート処理
                    Koukatons = []
                    enemies = []
                    player_base.hp = 1000
                    enemy_base.hp = 1000
                    cannon.cooldown = 0
                    game_state = GameState.RUNNING
                    frame_count = 0
                elif event.key == pygame.K_ESCAPE:
                    running = False
            else:
                if event.key == pygame.K_SPACE:
                    Koukatons.append(CatUnit())                    # こうかとんを追加
                if event.key == pygame.K_LSHIFT and cannon.cooldown <= 0:
                    if random.random() < 0.1:
                        fail_image_timer = 60                 # 失敗表示
                    else:
                        for _ in range(min(3, len(enemies))):  # 敵最大3体を削除
                            if enemies:
                                enemies.pop(0)
                        cannon.fire_text_timer = 60
                    cannon.cooldown = cannon.max_cooldown

    # ゲーム進行中のみ処理
    if game_state == GameState.RUNNING:
        frame_count += 1
        enemy_spawn_timer += 1
        if enemy_spawn_timer > 120:
            enemies.append(EnemyUnit())
            enemy_spawn_timer = 0

        for Koukaton in Koukatons:
            Koukaton.move()
            Koukaton.draw()
            if Koukaton.x >= enemy_base.x:
                enemy_base.hp -= Koukaton.damage
                Koukaton.hp = 0

        for enemy in enemies:
            enemy.move()
            enemy.draw()
            if enemy.x <= player_base.x + player_base.width:
                player_base.hp -= enemy.damage
                enemy.hp = 0

        # 衝突処理
        for enemy in enemies:
            if enemy.hp <= 0:
                continue
            for Koukaton in Koukatons:
                if Koukaton.hp <= 0:
                    continue
                if abs(Koukaton.x - enemy.x) < 30 and abs(Koukaton.y - enemy.y) < 30:
                    enemy.hp = 0
                    Koukaton.hp = 0
                    break

        Koukatons = [c for c in Koukatons if c.hp > 0]
        enemies = [e for e in enemies if e.hp > 0]

        if cannon.cooldown > 0:
            cannon.cooldown -= 1

        if player_base.hp <= 0:
            player_base.hp = 0
            game_state = GameState.PLAYER_LOSE
        if enemy_base.hp <= 0:
            enemy_base.hp = 0
            game_state = GameState.PLAYER_WIN

    # 描画処理
    player_base.draw()
    enemy_base.draw()
    cannon.draw()

    if fail_image_timer > 0:
        screen.blit(fail_image, (WIDTH//2 - fail_image.get_width()//2, HEIGHT//2 - 50))
        fail_image_timer -= 1

    font = pygame.font.SysFont(None, 28)
    screen.blit(font.render(f"Koukaton: {len(Koukatons)}", True, BLUE), (20, HEIGHT - 120))
    enemies_count = font.render(f"enemy: {len(enemies)}", True, RED)
    screen.blit(enemies_count, (WIDTH - enemies_count.get_width() - 20, HEIGHT - 120))

    pygame.display.update()           # 画面更新
    clock.tick(60)                    # 60FPS

pygame.quit()                         # Pygame終了
sys.exit()                            # プログラム終了
