import pygame
import sys
import os

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 480
BASE_DIR = "./Pygame-Tutorials-master/Game/"

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("First Game")

walkRight = []
walkLeft = []
walkRightEnemy = []
walkLeftEnemy = []
bg = pygame.image.load(os.path.join(BASE_DIR, "bg.jpg"))
char = pygame.image.load(os.path.join(BASE_DIR, "standing.png"))

for i in range(1, 10):
    walkRight.append(pygame.image.load(os.path.join(BASE_DIR, "R{}.png".format(i))))
    walkLeft.append(pygame.image.load(os.path.join(BASE_DIR, "L{}.png".format(i))))

for i in range(1, 12):
    walkRightEnemy.append(pygame.image.load(os.path.join(BASE_DIR, "R{}E.png".format(i))))
    walkLeftEnemy.append(pygame.image.load(os.path.join(BASE_DIR, "L{}E.png".format(i))))

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound(os.path.join(BASE_DIR, "bullet.mp3"))
hitSound = pygame.mixer.Sound(os.path.join(BASE_DIR, "hit.mp3"))
music = pygame.mixer.music.load(os.path.join(BASE_DIR, "music.mp3"))
pygame.mixer.music.play(-1)

score = 0

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            # win.blit(char, (self.x, self.y))
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))

        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont("comicsans", 100)
        text = font1.render("-5", 1, (255, 0, 0))
        win.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update()

        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class enemy(object):
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.walkCount = 0
        self.vel = 3
        self.path = [self.x, self.end]
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(walkRightEnemy[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(walkLeftEnemy[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - 5 * (10 - self.health), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0
        else:
            if self.x + self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.visible = False

def redrawGameWindow():
    # win.fill((0, 0, 0)) # fill black
    win.blit(bg, (0, 0))
    # pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    text = font.render("Score: " + str(score), 1, (0, 0, 0))
    win.blit(text, (360, 10))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()

font = pygame.font.SysFont("comicsans", 30, True)
man = player(300, 410, 64, 64)
bullets = []
goblin = enemy(100, 410, 64, 64, 450)
shootLoop = 0

while True:
    clock.tick(27)

    if goblin.visible == True:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()

    for bullet in bullets:
        if goblin.visible == True:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                    hitSound.play()
                    goblin.hit()
                    bullets.pop(bullets.index(bullet))
                    score += 1

        if bullet.x < SCREEN_WIDTH and bullet.x >= 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), facing))
            bulletSound.play()

        shootLoop = 1

    if keys[pygame.K_LEFT]:
        man.x -= man.vel
        man.x = max(man.x, 0)
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT]:
        man.x += man.vel
        man.x = min(man.x, SCREEN_WIDTH - man.width)
        man.left = False
        man.right = True
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if not man.isJump:
        '''
        if keys[pygame.K_UP]:
            y -= vel
            y = max(y, 0)
        if keys[pygame.K_DOWN]:
            y += vel
            y = min(y, SCREEN_HEIGHT - height)
        '''
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1

            man.y -= neg * (man.jumpCount ** 2) * 0.5
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()
