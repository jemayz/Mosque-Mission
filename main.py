from random import randrange
from generator import *


class Mosque:
    def __init__(self):
        self.img = pygame.image.load('mosque4.jpg').convert_alpha()
        self.img = pygame.transform.scale(self.img, (TILE - 10, TILE - 10))
        self.rect = self.img.get_rect()
        self.set_pos()

    def set_pos(self):
        self.rect.topleft = randrange(cols) * TILE + 5, randrange(rows) * TILE + 5

    def draw(self):
        game_surface.blit(self.img, self.rect)


def is_collide(x, y):
    tmp_rect = player_rect.move(x, y)
    if tmp_rect.collidelist(walls_collide_list) == -1:
        return False
    return True


def go_Mosque():
    for mosque in mosque_list:
        if player_rect.collidepoint(mosque.rect.center):
            mosque.set_pos()
            return True
    return False


def is_game_over():
    global time, score, record, FPS
    if time < 0:
        pygame.time.wait(700)
        player_rect.center = TILE // 2, TILE // 2
        [mosque.set_pos() for mosque in mosque_list]
        set_record(record, score)
        record = get_record()
        time, score, FPS = 60, 0, 60


def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')
            return 0


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))


FPS = 60
pygame.init()
game_surface = pygame.Surface(RES)
surface = pygame.display.set_mode((WIDTH + 300, HEIGHT))
clock = pygame.time.Clock()

# images
bg_game = pygame.image.load('bg2.jpg').convert()
bg = pygame.image.load('bg2.jpg').convert()

# get maze
maze = generate_maze()

# player settings
player_speed = 5
player_img = pygame.image.load('muslim3.png').convert_alpha()
player_img = pygame.transform.scale(player_img, (TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))
player_rect = player_img.get_rect()
player_rect.center = TILE // 2, TILE // 2
directions = {'a': (-player_speed, 0), 'd': (player_speed, 0), 'w': (0, -player_speed), 's': (0, player_speed)}
keys = {'a': pygame.K_a, 'd': pygame.K_d, 'w': pygame.K_w, 's': pygame.K_s}
direction = (0, 0)

# mosque settings
mosque_list = [Mosque() for i in range(1)]

# collision list
walls_collide_list = sum([cell.get_rects() for cell in maze], [])

# timer, score, record
pygame.time.set_timer(pygame.USEREVENT, 1000)
time = 60
score = 0
record = get_record()

# fonts
font = pygame.font.SysFont('Impact', 150)
text_font = pygame.font.SysFont('Impact', 80)

while True:
    surface.blit(bg, (WIDTH, 0))
    surface.blit(game_surface, (0, 0))
    game_surface.blit(bg_game, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.USEREVENT:
            time -= 1

    # controls and movement
    pressed_key = pygame.key.get_pressed()
    for key, key_value in keys.items():
        if pressed_key[key_value] and not is_collide(*directions[key]):
            direction = directions[key]
            break
    if not is_collide(*direction):
        player_rect.move_ip(direction)

    # draw maze
    [cell.draw(game_surface) for cell in maze]

    # gameplay
    if go_Mosque():
        FPS += 10
        score += 27
    is_game_over()

    # draw player
    game_surface.blit(player_img, player_rect)

    # draw mosque
    [mosque.draw() for mosque in mosque_list]

    # draw stats
    surface.blit(text_font.render('TIME', True, pygame.Color('cyan'), True), (WIDTH + 50, 0))
    surface.blit(font.render(f'{time}', True, pygame.Color('cyan')), (WIDTH + 50, 70))
    surface.blit(text_font.render('Score:', True, pygame.Color('pink'), True), (WIDTH + 50, 230))
    surface.blit(font.render(f'{score}', True, pygame.Color('pink')), (WIDTH + 50, 310))
    surface.blit(text_font.render('Record:', True, pygame.Color('red'), True), (WIDTH + 30, 470))
    surface.blit(font.render(f'{record}', True, pygame.Color('red')), (WIDTH + 50, 540))

    # print(clock.get_fps())
    pygame.display.flip()
    clock.tick(FPS)