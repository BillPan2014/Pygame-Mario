# Example file showing a circle moving on screen
from random import randint

import pygame
from Mario import mario, goomba

all_objects=[]

class GameObject():
    def __init__(self, image, x, y, speed):
        self.speed = speed
        self.image = image
        self.rect = self.image.get_rect().move(x,y)
        self.hitbox = self.rect.inflate(-self.rect.width*0.25, -self.rect.height*0.1)


    def move(self, up=False, down=False, left=False, right=False,random=False):
        if right:
            # self.pos.right += self.speed
            new_rect = self.rect.move(self.speed,0)
        if left:
            # self.pos.right -= self.speed
            new_rect = self.rect.move(-self.speed,0)
        if down:
            # self.pos.top += self.speed
            new_rect = self.rect.move(0, self.speed)
        if up:
            # self.pos.top -= self.speed
            new_rect = self.rect.move(0, -self.speed)
        if random:
            # self.pos.right += self.speed * randint(-1,1)
            # self.pos.top += self.speed * randint(-1,1)
            new_rect = self.rect.move(self.speed * randint(-1,1),self.speed * randint(-1,1))

        new_hitbox = new_rect.inflate(-self.rect.width*0.25, -self.rect.height*0.1)
        if not pygame.display.get_surface().get_rect().contains(new_rect):
            return
        if self.check_collision(new_hitbox):
            return

        self.rect = new_rect
        self.hitbox = new_hitbox

    def check_collision(self, rect):
        for obj in all_objects:
            if obj is not self and rect.colliderect(obj.hitbox):
                return True
        return False



        # if self.pos.right > WIDTH:
        #     self.pos.left = 0
        # if self.pos.top > HEIGHT - SPRITE_HEIGHT:
        #     self.pos.top = 0
        # if self.pos.right < SPRITE_WIDTH:
        #     self.pos.right = WIDTH
        # if self.pos.top < 0:
        #     self.pos.top = HEIGHT - SPRITE_HEIGHT
# pygame setup
pygame.init()
screen = pygame.display.set_mode((728, 408))
mario_image = pygame.image.load('Mario.png').convert_alpha()
mario_image = pygame.transform.scale(mario_image, (100, 100))
mario_image = pygame.transform.flip(mario_image, True, False)
goomba_image = pygame.image.load('Goomba.png').convert_alpha()
goomba_image = pygame.transform.scale(goomba_image, (50, 50))
background_image = pygame.image.load('Background.png').convert_alpha()
background_image = pygame.transform.scale(background_image, (728, 408))
mario = GameObject(mario_image, 10, 3, 3)
all_objects.append(mario)
objects = []
for x in range(5):
    o = GameObject(goomba_image, 200 + x *55, 250,3)
    objects.append(o)
    all_objects.append(o)
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("light blue")
    screen.blit(background_image, (0, 0))
    # pygame.draw.circle(screen, "red", player_pos, 20)
    screen.blit(mario.image, mario.rect)
    for o in objects:
        o.move(random=True)
        screen.blit(o.image, o.rect)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        # player_pos.y -= 500 * dt
        mario.move(up=True)
    if keys[pygame.K_s]:
        # player_pos.y += 500 * dt
        mario.move(down=True)
    if keys[pygame.K_a]:
        # player_pos.x -= 500 * dt
        mario.move(left=True)
    if keys[pygame.K_d]:
        # player_pos.x += 500 * dt
        mario.move(right=True)
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()