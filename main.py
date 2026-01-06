import pygame
import random
import sys
import os

# ---------- RESOURCE PATH ----------
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()
pygame.mixer.init()

# ---------- SCREEN ----------
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Last Plank by NTSgrow")

clock = pygame.time.Clock()

FONT = pygame.font.SysFont("comicsansms", 52, bold=True)
SMALL_FONT = pygame.font.SysFont(None, 28)

# ---------- COLORS ----------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# ---------- BACKGROUNDS ----------
bg_files = ["bg.png", "bg1.png", "bg3.png"]
bg = None

def load_random_bg():
    global bg
    img = pygame.image.load(resource_path(random.choice(bg_files))).convert()
    bg = pygame.transform.scale(img, (WIDTH, HEIGHT))

load_random_bg()

# ---------- MUSIC ----------
pygame.mixer.music.load(resource_path("b.mp3"))
game_over_sound = pygame.mixer.Sound(resource_path("over.mp3"))

# ---------- BALL ----------
ball_radius = 15
ball_speed_x = 6
gravity = 4

# ---------- HERO ----------
hero_img = pygame.image.load(resource_path("hero.png")).convert_alpha()
HERO_SIZE = int(ball_radius * 2 * 2)
hero_img = pygame.transform.scale(hero_img, (HERO_SIZE, HERO_SIZE))
hero_right = hero_img
hero_left = pygame.transform.flip(hero_img, True, False)
current_hero = hero_right

# ---------- PLANK ----------
plank_height = 15
plank_speed = 3
PLANK_COUNT = 3
MAX_PLANK_WIDTH = 130
MIN_PLANK_WIDTH = 70

# ---------- BUTTON ----------
retry_button = pygame.Rect(WIDTH//2 - 80, HEIGHT//2 + 50, 160, 45)

# ---------- GAME STATES ----------
START = 0
PLAYING = 1
GAME_OVER = 2
game_state = START

# ---------- MOTIVATIONAL TEXT SYSTEM ----------
quotes = [

# --- 1–50 ---
"KEEP GOING 💪","NEVER GIVE UP 🔥","YOU ARE STRONGER 💥","ONE MORE TRY 🚀","BELIEVE IN YOU ❤️",
"FOCUS IS POWER 🎯","STAY HARD 😤","NO EXCUSES ⚡","WIN OR LEARN 🧠","LEVEL UP 🔝",
"GAME ON 🎮","PLAY LIKE A PRO 👑","DON'T PANIC 😎","SKILL > LUCK 🧠","CLUTCH TIME ⏱️",
"EYES ON TARGET 🎯","STAY SHARP 🔪","NO FEAR 😈","FULL POWER 🔋","GO BEAST MODE 🦁",
"AARAM MAT KAR 😤","HIMMAT MAT HAR 🔥","TU KAR SAKTA HAI 💪","BAS EK AUR TRY 🚀",
"DIMAAG THANDA RAKH 🧠","CONTROL = SUCCESS 🎯","NAZAR BALL PE 👀",
"AAJ NAHI TO KABHI NAHI ⚡","KHUD PE BHAROSA RAKH ❤️","MAT RUK 😎",
"FAILURE = PRACTICE 📈","LOSING MAKES YOU STRONG 💥","FOCUS BRO FOCUS 🎯",
"NO PAIN NO GAIN 🔥","STAY CONSISTENT 🧠","WORK SILENT WIN LOUD 🏆",
"PRESS ON 💪","YOU GOT THIS 🚀","HARD WORK PAYS 💸","KEEP THE FLOW 🌊",
"CALM MIND WINS 🧘","REACTION TIME ⚡","BALANCE IS KEY 🔑","DON'T RUSH 😌",
"SMART PLAY 🧠","SMALL MOVES BIG WINS 📈","DISCIPLINE = POWER 💥",
"LOCK IN 🔒","EYES FORWARD 👁️","STAY IN ZONE 🎧",

# --- 51–100 ---
"MAIN CHARACTER ENERGY 😎","BUILT DIFFERENT 🧬","GRIND MODE ON 🔥","NO LIMITS 🚫",
"CHASE GREATNESS 👑","UNSTOPPABLE 💣","NEXT LEVEL 🧠","HUSTLE HARD 💪",
"DO OR DIE ⚔️","WINNING HABIT 🏆","FOCUS MAT TOD ❌","GALTI SE SEEKH 📚",
"CONTROL YOUR MOVE 🎯","KHEL KHATARNAAK 🔥","DARR KO HARA 😈",
"SABAR KA PHAL SWEET 🍯","BAS JAME RAHO 💪","GAME TERA HAI 🎮",
"TENSION MAT LE 😌","AAGE BADH 🚀","EFFORT NEVER LIES 📈",
"STRONG MIND STRONG PLAY 🧠","STAY HUNGRY 🐺","PUSH YOUR LIMIT 💥",
"TRAINED TO WIN 🏆","NO DISTRACTIONS 🔕","KEEP BALANCE ⚖️",
"OWN THE MOMENT ⏳","JUST BREATHE 😮‍💨","EXECUTE PERFECTLY 🎯",
"TU HERO HAI 👑","AAPKA TIME AAYEGA ⏰","FINAL TRY 🔥",
"HARD MODE ON ⚙️","TU LEGEND BANEGA 🏆","CONTROL HI KING 👑",
"AANKH MAT JHAPAK 👀","END TAK KHEL 🎮","REACTION FAST ⚡",
"TU BOSS HAI 👑","MIND OVER MOVES 🧠","FOCUS LOCK 🔒",
"TILT MAT HO 😤","KEEP TRYING 🔁",

# --- 101–200 ---
"YOU ARE READY 💪","STAY COOL ❄️","PERFECT TIMING ⏱️","ONE MOVE MATTERS 🎯",
"SMART NOT FAST 🧠","CONTROL YOUR SPEED ⚖️","DON'T BLINK 👀",
"HOLD THE LINE 🛡️","CONFIDENCE BOOST 🔋","GAME SENSE ON 🧠",
"NO PRESSURE 😌","DOMINATE 🎮","EVERY TRY COUNTS 📈",
"YOU ARE IMPROVING 🔝","GAME IS TESTING YOU 🔥",
"PASS THIS LEVEL 🚀","EYES OPEN 👁️","WIN COMES LATE 🏆",
"STAY PRESENT ⏳","END GAME ENERGY 😤","FINAL MOMENT 👑",
"NO FEAR LEFT 😈","THIS IS IT 🔥","LEVEL MASTER 🎮",
"CALM HANDS ✋","PERFECT CONTROL 🎯","WIN IT 🏆",
"LEGEND MOVE 👑","GAME WON 💥","STAY ALIVE 🕹️",
"SAFE PLAY 🎯","SMART GAMER 🧠","PURE SKILL 💥",
"CALCULATED MOVES 📐","STAY CENTERED ⚖️","READY FOR MORE 🚀",
"NO MERCY MODE 😈","JUST PLAY 😎","NO DISTRACTION 🔕",
"DOMINATE AGAIN 👑","ONE LIFE ONE GAME 🎮",
"PLAY TO WIN 🏆","YOU CAN DO IT 💪",
"NEVER BACK DOWN 🔥","LOCKED IN 🔒",

# --- 201–300 ---
"FOCUS = POWER 🎯","STAY HARD 😤","NO SHORTCUTS ⚡",
"BUILD YOUR SKILL 🧠","PLAY WITH BRAIN 🧠",
"CONTROL THE CHAOS 🔥","DON'T TILT 😎",
"SMART RISK 📐","WIN THE MOMENT ⏳",
"YOU ARE SHARP 🔪","LEVEL AFTER LEVEL 🔝",
"KEEP BALANCE ⚖️","NO FEAR MODE 😈",
"CONFIDENCE ON 🔋","REACTION KING ⚡",
"STAY ALIVE BRO 🕹️","HOLD STEADY 🛡️",
"TRUST YOUR MOVE 🎯","STAY FOCUSED 👁️",
"ONE SHOT COUNTS 💥","DISCIPLINE WINS 🧠",
"CALM PLAY 🔑","NO PANIC 😌",
"PERFECT FLOW 🌊","CONTROL MASTER 👑",
"SKILL CHECK 🔥","YOU ARE READY 🚀",
"NEXT TRY BETTER 📈","NEVER QUIT 💪",
"KEEP GRINDING 🔥","SMART WIN 🧠",
"LOCK TARGET 🎯","STAY SHARP 👁️",
"GAME FACE ON 😤","CLUTCH PLAYER 👑",
"DO IT AGAIN 🔁","WIN OR LEARN 🧠",
"LEVEL CLEARED 🏆","GAME BRAIN 🧠",
"POWER MOVE 💥","FINAL PUSH 🔥",
"CONTROL EVERYTHING 🎮","YOU GOT THIS 💪",
"NO MISTAKES 👀","STAY CLEAN 🎯",

# --- 301–400 ---
"FOCUS MODE 🔒","SKILL OVER SPEED 🧠",
"SMART GRIND 📈","STAY STRONG 💪",
"YOU ARE BUILT 🔥","DON'T STOP 🚀",
"ONE MORE LEVEL 🎮","CONTROL KING 👑",
"STAY ALERT 👁️","PLAY CLEAN 🎯",
"NO EXCUSES MODE 😤","GAME IQ 🧠",
"PERFECT BALANCE ⚖️","FINAL STAND 🔥",
"TRUST YOURSELF ❤️","NEXT MOVE 🎯",
"STAY READY ⚡","YOU ARE FAST 🏃",
"NO DOUBT 💥","WIN THE GAME 🏆",
"STAY CALM 🧘","FOCUS HARD 🔥",
"GAME FLOW 🌊","SMART CONTROL 🎮",
"LEVEL UP AGAIN 🔝","YOU ARE WINNING 👑",
"PLAY SMART 😎","DISCIPLINE FIRST 🧠",
"LOCK IT IN 🔒","NO RUSH ⏳",
"CONTROL = WIN 🎯","GAME MINDSET 🧠",
"STAY HUNGRY 🔥","ONE LAST TRY 🚀",
"POWER THROUGH 💥","STAY FIRM 🛡️",
"END STRONG 🏆","YOU ARE READY 😤",
"FOCUS ENDGAME 🎮","VICTORY MODE 👑",
"GAME COMPLETED 💥","LEGEND STATUS 🏆"

]




quote_text = ""
quote_alpha = 0
quote_y = 0
quote_color = (255,255,255)
quote_start_time = 0
QUOTE_DURATION = 2500
next_quote_time = 0

def trigger_quote():
    global quote_text, quote_alpha, quote_y, quote_color, quote_start_time, next_quote_time
    quote_text = random.choice(quotes)
    quote_y = random.randint(60, HEIGHT//2 - 60)
    quote_color = (random.randint(150,255),random.randint(150,255),random.randint(150,255))
    quote_alpha = 0
    quote_start_time = pygame.time.get_ticks()
    next_quote_time = quote_start_time + random.randint(5000,9000)

# ---------- RESET ----------
def reset_game():
    global ball_x, ball_y, ball_speed_y
    global planks, score
    global current_plank_id, game_over_played
    global current_hero, next_quote_time

    load_random_bg()
    ball_x = WIDTH//2
    ball_y = 80
    ball_speed_y = gravity

    planks = []
    for i in range(PLANK_COUNT):
        w = random.randint(MIN_PLANK_WIDTH, MAX_PLANK_WIDTH)
        planks.append({"x":random.randint(0,WIDTH-w),"y":HEIGHT+i*200,"w":w,"id":i,"land_time":None})

    score = 0
    current_plank_id = None
    game_over_played = False
    current_hero = hero_right
    next_quote_time = pygame.time.get_ticks() + 3000

# ---------- MAIN LOOP ----------
while True:
    clock.tick(60)
    screen.blit(bg,(0,0))
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit();sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit();sys.exit()
            if event.key == pygame.K_RETURN:
                reset_game()
                pygame.mixer.music.play(-1)
                game_state = PLAYING

    keys = pygame.key.get_pressed()

    if game_state == START:
        screen.blit(FONT.render("Last Plank",True,RED),(WIDTH//2-150,HEIGHT//2-40))
        screen.blit(SMALL_FONT.render("Press ENTER to Start",True,WHITE),(WIDTH//2-120,HEIGHT//2+10))
        pygame.display.update();continue

    if game_state == GAME_OVER:
        screen.blit(FONT.render("GAME OVER",True,WHITE),(WIDTH//2-150,HEIGHT//2-70))
        screen.blit(SMALL_FONT.render(f"Score : {int(score)}",True,WHITE),(WIDTH//2-70,HEIGHT//2-30))
        pygame.draw.rect(screen,GRAY,retry_button)
        screen.blit(SMALL_FONT.render("RESTART",True,BLACK),(retry_button.x+40,retry_button.y+12))
        pygame.display.update();continue

    if keys[pygame.K_LEFT]:
        ball_x -= ball_speed_x
        current_hero = hero_left
    if keys[pygame.K_RIGHT]:
        ball_x += ball_speed_x
        current_hero = hero_right

    ball_x = max(ball_radius,min(WIDTH-ball_radius,ball_x))
    ball_y += ball_speed_y

    for plank in planks:
        plank["y"] -= plank_speed
        if plank["y"] < -plank_height:
            plank["y"] = HEIGHT
            plank["w"] = random.randint(MIN_PLANK_WIDTH,MAX_PLANK_WIDTH)
            plank["x"] = random.randint(0,WIDTH-plank["w"])
            plank["land_time"] = None
            score += 10

        if plank["y"] <= ball_y+ball_radius <= plank["y"]+plank_height and plank["x"] <= ball_x <= plank["x"]+plank["w"] and ball_speed_y>0:
            ball_speed_y = 0
            ball_y = plank["y"]-ball_radius
            plank["land_time"] = current_time

    if ball_y > HEIGHT:
        pygame.mixer.music.stop()
        if not game_over_played:
            game_over_sound.play()
            game_over_played = True
        game_state = GAME_OVER

    ball_speed_y = gravity
    score += 2

    screen.blit(current_hero,(ball_x-HERO_SIZE//2,ball_y-HERO_SIZE//2))
    for plank in planks:
        pygame.draw.rect(screen,BLACK,(plank["x"],plank["y"],plank["w"],plank_height))

    screen.blit(SMALL_FONT.render(f"Score : {int(score)}",True,WHITE),(10,10))
    screen.blit(SMALL_FONT.render("ESC to Quit",True,WHITE),(WIDTH-120,10))

    if current_time >= next_quote_time:
        trigger_quote()

    if quote_text:
        elapsed = current_time-quote_start_time
        if elapsed < QUOTE_DURATION:
            quote_alpha = min(255,int(255*(1-elapsed/QUOTE_DURATION)))
            text = FONT.render(quote_text,True,quote_color)
            text.set_alpha(quote_alpha)
            screen.blit(text,(WIDTH//2-text.get_width()//2,quote_y))
        else:
            quote_text = ""

    pygame.display.update()
