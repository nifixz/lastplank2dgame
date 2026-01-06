import pygame
import sys
import os
import subprocess
import math
import random

# ---------- INIT ----------
pygame.init()
pygame.mixer.init()

# ---------- PATH ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def path(file):
    return os.path.join(BASE_DIR, file)

# ---------- SCREEN ----------
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Last Plank")

clock = pygame.time.Clock()

# ---------- FONTS ----------
TEXT_FONT = pygame.font.SysFont(None, 34)

# ---------- COLORS ----------
WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
ORANGE = (255, 120, 40)
BLACK = (0, 0, 0)

# ---------- MUSIC ----------
pygame.mixer.music.load(path("homebg.mp3"))
pygame.mixer.music.play(-1)

# ---------- BACKGROUND ----------
bg_img = pygame.image.load(path("logo.png")).convert()
def scale_bg(img):
    iw, ih = img.get_size()
    scale = max(WIDTH / iw, HEIGHT / ih)
    return pygame.transform.smoothscale(img, (int(iw*scale), int(ih*scale)))
bg = scale_bg(bg_img)

# ---------- STATES ----------
HOME = 0
LOADING = 1
state = HOME

# ---------- LOADING DATA ----------
angle = 0
pulse = 0
progress = 0

fire_particles = []
smoke_particles = []

# ---------- PARTICLES ----------
def spawn_fire(cx, cy):
    fire_particles.append([
        cx + random.randint(-20, 20),
        cy + random.randint(-20, 20),
        random.randint(4, 7),
        random.randint(2, 4)
    ])

def spawn_smoke(cx, cy):
    smoke_particles.append([
        cx + random.randint(-30, 30),
        cy + random.randint(-10, 10),
        random.randint(20, 30),
        random.uniform(0.3, 0.6)
    ])

# ---------- DRAW LOADING ----------
def draw_loading(cx, cy):
    global angle, pulse, progress

    angle = (angle + 4) % 360
    pulse = (pulse + 1) % 60
    progress = min(progress + 0.6, 100)

    # beat sync pulse
    beat = 1 + 0.08 * math.sin(pulse / 6)

    # fire + smoke
    for _ in range(2):
        spawn_fire(cx, cy)
    if pulse % 8 == 0:
        spawn_smoke(cx, cy)

    for f in fire_particles[:]:
        f[1] -= f[3]
        f[2] -= 0.15
        if f[2] <= 0:
            fire_particles.remove(f)
        else:
            pygame.draw.circle(screen, ORANGE, (int(f[0]), int(f[1])), int(f[2]))

    for s in smoke_particles[:]:
        s[2] += 0.3
        s[3] -= 0.01
        if s[3] <= 0:
            smoke_particles.remove(s)
        else:
            surf = pygame.Surface((s[2]*2, s[2]*2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (200, 200, 200, int(80*s[3])), (s[2], s[2]), s[2])
            screen.blit(surf, (s[0]-s[2], s[1]-s[2]))

    # rotating arcs
    r1, r2 = int(26*beat), int(38*beat)
    pygame.draw.arc(screen, WHITE, (cx-r2, cy-r2, r2*2, r2*2),
                    math.radians(angle), math.radians(angle+200), 4)
    pygame.draw.arc(screen, GRAY, (cx-r1, cy-r1, r1*2, r1*2),
                    math.radians(-angle), math.radians(-angle+240), 3)

    # progress bar
    bar_w, bar_h = 300, 10
    bx, by = cx - bar_w//2, cy + 70
    pygame.draw.rect(screen, GRAY, (bx, by, bar_w, bar_h), 1)
    pygame.draw.rect(screen, ORANGE, (bx, by, int(bar_w*(progress/100)), bar_h))

    txt = TEXT_FONT.render(f"Loading {int(progress)}%", True, WHITE)
    screen.blit(txt, (cx - txt.get_width()//2, by + 18))

# ---------- START GAME ----------
def launch_game():
    pygame.mixer.music.stop()
    subprocess.call([sys.executable, path("main.py")])
    pygame.quit()
    sys.exit()

# ---------- MAIN LOOP ----------
while True:
    clock.tick(60)

    # background
    screen.blit(bg, ((WIDTH-bg.get_width())//2, (HEIGHT-bg.get_height())//2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()

            if event.key == pygame.K_RETURN and state == HOME:
                state = LOADING
                progress = 0

    if state == HOME:
        hint = TEXT_FONT.render("Press ENTER to Start", True, WHITE)
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 140))

    if state == LOADING:
        draw_loading(WIDTH//2, HEIGHT - 200)
        if progress >= 100:
            launch_game()

    pygame.display.update()
