from pygame import *
import socket
import json
from threading import Thread




# ---ПУГАМЕ НАЛАШТУВАННЯ ---
WIDTH, HEIGHT = 800, 600
init()
screen = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
display.set_caption("Пінг-Понг")

CURRENT_SCORE = 0
# ---СЕРВЕР ---
def connect_to_server():
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('localhost', 8080)) # ---- Підключення до сервера
            buffer = ""
            game_state = {}
            my_id = int(client.recv(24).decode())
            return my_id, game_state, buffer, client
        except:
            pass


def receive():
    global buffer, game_state, game_over
    while not game_over:
        try:
            data = client.recv(1024).decode()
            buffer += data
            while "\n" in buffer:
                packet, buffer = buffer.split("\n", 1)
                if packet.strip():
                    game_state = json.loads(packet)
        except:
            game_state["winner"] = -1
            break

# --- ШРИФТИ ---
font_win = font.Font(None, 72)
font_main = font.Font(None, 36)
# --- ЗОБРАЖЕННЯ ----
loading_bg = image.load("images/waiting.png")
loading_bg = transform.scale(loading_bg, (WIDTH, HEIGHT))

game_bg = image.load("images/bg.png")
game_bg = transform.scale(game_bg, (WIDTH, HEIGHT))

win_bg = image.load("images/win.png")
win_bg = transform.scale(win_bg, (WIDTH, HEIGHT))

lose_bg = image.load("images/lose.png")
lose_bg = transform.scale(lose_bg, (WIDTH, HEIGHT))

# --- ЗВУКИ ---
mixer.init()
mixer.music.load("sounds/in_the_lobby.wav")
mixer.music.play(-1)

ball_platform_sound = mixer.Sound("sounds/Pop.ogg")
ball_platform_sound.set_volume(1)

ball_wall_sound = mixer.Sound("sounds/wall.ogg")
ball_wall_sound.set_volume(1)

lose_sound = mixer.Sound("sounds/lose.ogg")
lose_sound.set_volume(1)

win_sound = mixer.Sound("sounds/win.wav")
win_sound.set_volume(1)

Score_sound = mixer.Sound("sounds/Score.ogg")
Score_sound.set_volume(1)

# --- ГРА ---
game_over = False
winner = None
you_winner = None
my_id, game_state, buffer, client = connect_to_server()
Thread(target=receive, daemon=True).start()
while True:
    for e in event.get():
        if e.type == QUIT:
            exit()

    if "countdown" in game_state and game_state["countdown"] > 0:
        screen.fill((0, 0, 0))
        countdown_text = font.Font(None, 72).render(str(game_state["countdown"]), True, (255, 255, 255))
        screen.blit(countdown_text, (WIDTH // 2 - 20, HEIGHT // 2 - 30))
        display.update()
        continue  # Не малюємо гру до завершення відліку

    if "winner" in game_state and game_state["winner"] is not None:
        screen.fill((20, 20, 20))

        if you_winner is None:  # Встановлюємо тільки один раз
            if game_state["winner"] == my_id:
                you_winner = True
            else:
                you_winner = False
