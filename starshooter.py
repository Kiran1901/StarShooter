import pygame
import random
from os import  path

img_dir = path.join(path.dirname(__file__), 'img')

width = 768
height = 680
FPS = 30

#colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#initialize pygame and window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Kiran's StarShooter")
clock = pygame.time.Clock()

class bullet(pygame.sprite.Sprite):
    def __init__(self, x ,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (8,16))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy= -10
    def update(self):
        self.rect.y += self.speedy

        if self.rect.bottom < 0:
            self.kill()

class player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (69,53))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center= (width / 2, height - 30)
        self.speedx = 5

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.speedx= -8
        if keystate[pygame.K_RIGHT]:
            self.speedx= 8

        self.rect.x += self.speedx

        if self.rect.x > width-40:
            self.rect.x= width-40
        if self.rect.x < 0:
            self.rect.x=0

    def shoot(self):
        bul = bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bul)
        bullets.add(bul)

class mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.transform.scale(mob_img, (69,68))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1, width-60)
        self.rect.y = random.randrange(-120 , -60)
        self.speedy = random.randrange(5, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.top > height  or  self.rect.x <-60  or  self.rect.x >width:
            self.rect.x= random.randrange(1,width-60)
            self.rect.y = random.randrange(-120, -60)
            self.speedy = random.randrange(5, 8)
            #self.speedx = random.randrange(-3, 3)

#loading graphics
background_img = pygame.image.load(path.join(img_dir, "blue.png")).convert()
background = pygame.transform.scale(background_img, (width,height))
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip_blue.png")).convert()
mob_img = pygame.image.load(path.join(img_dir, "meteorBrown.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserBlue.png")).convert()

#sprite groups
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player=player()
all_sprites.add(player)
for i in range(8):
    m = mob()
    all_sprites.add(m)
    mobs.add(m)

#game loop
running= True
while running:

    clock.tick(FPS)

    #events(process input)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()


        if event.type == pygame.QUIT:
            running = False

    #update
    all_sprites.update()

    hits = pygame.sprite.groupcollide(mobs, bullets , True , True)
    for hit in hits:
        m = mob()
        all_sprites.add(m)
        mobs.add(m)
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False

    #draw
    screen.fill(black)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)

    #after drawing everything flip the board
    pygame.display.flip()

pygame.quit()