import pygame
import pygame.mixer
pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
TILE = 32

pygame.display.set_caption("Tank1990")

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

fontUI = pygame.font.Font(None, 30)

pygame.mixer.init()
bullet_sound = pygame.mixer.Sound('Sounds/shot.wav')
pygame.mixer.music.load("Sounds/background_song1.mp3")

imgTanks = [
    pygame.image.load('PNG/Tanks/Tank1.png')
]
imgBangs = [
    pygame.image.load('PNG/bang/bang1.png'),
    pygame.image.load('PNG/bang/bang2.png'),
    pygame.image.load('PNG/bang/bang3.png'),
]

DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]

class UI:
    def __init__(self):
        pass

    def update(self):
        pass

    pygame.mixer.music.play(-1)
    def draw(self):
        i = 0
        for obj in objects:
            if obj.type == 'tank':
                pygame.draw.rect(window, obj.color, (5 + i * 70, 5, 22, 22))

                text = fontUI.render(str(obj.hp), 1, obj.color)
                rect = text.get_rect(center = (5 + i * 70 + 32, 5 + 11))
                window.blit(text, rect)
                i += 1

background_image = pygame.image.load("PNG/maps/Map2.png")
obstacle_image = pygame.image.load("PNG/Obstacles/barrelRed_side.png").convert_alpha()

obstacle = pygame.sprite.Sprite()
obstacle.image = obstacle_image
obstacle.rect = obstacle_image.get_rect()
obstacle.rect.center = (WIDTH // 2, HEIGHT // 2)

obstacles = pygame.sprite.Group()
obstacles.add(obstacle)

def draw(self):
    i = 0
    for obj in objects:
        if obj.type == 'tank':
            pygame.draw.rect(window, obj.color, (5 + i * 70, 5, 22, 22))

            text = fontUI.render(str(obj.hp), 1, obj.color)
            rect = text.get_rect(center=(5 + i * 70 + 32, 5 + 11))
            window.blit(text, rect)
            i += 1


class Tank:
    def __init__(self, color, px, py, direct, keyList):
        objects.append(self)
        self.type = 'tank'

        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.moveSpeed = 2
        self.hp = 5

        self.shotTimer = 0
        self.shotDelay = 60
        self.bulletSpeed = 5
        self.bulletDamage = 1

        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        self.keySHOT = keyList[4]

        self.rank = 0
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 5, self.image.get_height() - 5))
        self.rect = self.image.get_rect(center=self.rect.center)

        oldX, oldY = self.rect.topleft
        if keys[self.keyLEFT]:
            self.rect.x -= self.moveSpeed
            self.direct = 3
        elif keys[self.keyRIGHT]:
            self.rect.x += self.moveSpeed
            self.direct = 1
        elif keys[self.keyUP]:
            self.rect.y -= self.moveSpeed
            self.direct = 0
        elif keys[self.keyDOWN]:
            self.rect.y += self.moveSpeed
            self.direct = 2

        for obj in objects:
            if obj != self and obj.type == 'block' and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY

        if keys[self.keySHOT] and self.shotTimer == 0:
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay
            bullet_sound.play()

        if self.shotTimer > 0: self.shotTimer -= 1

    def draw(self):
        window.blit(self.image, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)
            print(self.color, 'dead')


class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage

    def update(self):
        self.px += self.dx
        self.py += self.dy

        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.type != 'bang' and obj.rect.collidepoint(self.px, self.py):
                    obj.damage(self.damage)
                    bullets.remove(self)
                    Bang(self.px, self.py)
                    break

    def draw(self):
        pygame.draw.circle(window, 'red', (self.px, self.py), 2)


class Bang:
    def __init__(self, px, py):
        objects.append(self)
        self.type = 'bang'

        self.px, self.py = px, py
        self.frame = 0

    def update(self):
        self.frame += 0.2
        if self.frame >= 3: objects.remove(self)

    def draw(self):
        image = imgBangs[int(self.frame)]
        rect = image.get_rect(center=(self.px, self.py))
        window.blit(image, rect)


bullets = []
objects = []
Tank('blue', 100, 275, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
Tank('red', 650, 275, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP_ENTER))
ui = UI()

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False


    keys = pygame.key.get_pressed()

    # Рисование заднего фона
    window.blit(background_image, (0, 0))
    for bullet in bullets: bullet.update()
    for obj in objects: obj.update()
    obstacles.draw(window)
    ui.update()

    # если это убрать, то пули и объекты исчезнут
    for bullet in bullets: bullet.draw()
    for obj in objects: obj.draw()
    ui.draw()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
