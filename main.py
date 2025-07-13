# Example file showing a circle moving on screen
from random import randint
import os
import pygame
from Mario import mario, goomba

all_objects=[]

def load_sound(name):
    class NoneSound:
        def play(self):
            pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(name)
    sound = pygame.mixer.Sound(fullname)

    return sound
class GameObject():
    def __init__(self, image, x, y, speed, punch_sound = None):
        self.speed = speed
        self.image = image
        self.rect = self.image.get_rect().move(x,y)
        self.hitbox = self.rect.inflate(-self.rect.width*0.25, -self.rect.height*0.1)
        self.attacking = False
        self.hit = False
        self.last_hit = 0
        self.last_attack = 0
        self.attack_speed = 1000
        self.punch_sound = punch_sound
        self.orientation = 'right'

    def melee_attack(self, target):
        # if not self.attacking and pygame.time.get_ticks() > self.last_attack+self.speed:
        self.attacking = True
        self.last_attack = pygame.time.get_ticks()
        # attack_range = self.hitbox.scale_by(1.5)
        if self.orientation == 'right':
            attack_range = self.hitbox.move(25, 0)
        elif self.orientation == 'left':
            attack_range = self.hitbox.move(-25, 0)
        return attack_range.colliderect(target.hitbox)

    def stop_attack(self):
        self.attacking = False

    def update(self):
        if self.hit:
            self.spin()
        else:
            self.move(random=True)

    def change_orientaion(self, orientation):
        flip = pygame.transform.flip
        self.original = self.image
        if self.orientation != orientation and orientation == 'right':
            self.orientation = orientation
            self.image = flip(self.original, 1, 0)
        if self.orientation != orientation and orientation == 'left':
            self.orientation = orientation
            self.image = flip(self.original, 1, flip_y=0)

    def spin(self):
        center = self.rect.center
        self.hit = self.hit + 12
        if self.hit >= 360:
            self.hit = False
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.hit)
        self.rect = self.image.get_rect(center=center)

    def get_hit(self):
        if not self.hit and pygame.time.get_ticks() - self.last_hit > 1000:
            self.hit = True
            self.last_hit = pygame.time.get_ticks()
            self.original = self.image

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

def handle_fireball(fireball, targets):
    for ball in fireball:
        ball.x += 20
        for target in targets:
            if ball.colliderect(target.hitbox):
                target.get_hit()
                fireball.remove(ball)
            if not pygame.display.get_surface().get_rect().contains(ball):
                fireball.remove(ball)


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
punch_sound = load_sound('punch-2-37333.mp3')
fireball_image = pygame.image.load('Fireball.png').convert_alpha()
fireball_image = pygame.transform.scale(fireball_image, (25, 25))
mario = GameObject(mario_image, 10, 3, 3, punch_sound)
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

fireball = []

while running:
    # dt = clock.tick(60) / 1000
    clock.tick(60)
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

    keys = pygame.key.get_pressed()
    print(f'w {keys[pygame.K_w]}')
    if keys[pygame.K_w]:
        # player_pos.y -= 500 * dt
        mario.move(up=True)
    if keys[pygame.K_s]:
        # player_pos.y += 500 * dt
        mario.move(down=True)
    if keys[pygame.K_a]:
        # player_pos.x -= 500 * dt
        mario.move(left=True)
        mario.change_orientaion('left')
    if keys[pygame.K_d]:
        # player_pos.x += 500 * dt
        mario.move(right=True)
        mario.change_orientaion('right')
    if keys[pygame.K_SPACE]:
        if not mario.attacking and pygame.time.get_ticks() > mario.last_attack+mario.attack_speed:
            punch_sound.play()
            for o in objects:
                if mario.melee_attack(o):
                    o.get_hit()
            mario.stop_attack()
    # if keys[pygame.K_f]:
    #     if len(fireball) == 0:
    #         fireball.append(pygame.rect.Rect(mario.rect.centerx, mario.rect.centery,20,20))
    # for ball in fireball:
    #     screen.blit(fireball_image, ball)
    # handle_fireball(fireball, objects)
    for o in objects:
        # o.move(random=True)
        o.update()
        screen.blit(o.image, o.rect)
    pygame.display.flip()


    # for event in pygame.event.getlen(():
    # #     # if event.type == pygame.QUIT:
    # #     #     # going = False
    # #     # elif event.type == pygame.KEYDOWN and event.key  == pygame.K_ESCAPE:
    # #     #     # going = False
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #         print(f'mouse down')
    #     elif event.type == pygame.MOUSEBUTTONUP:
    #         print(f'mouse up')

    # flip() the display to put your work on screen

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.

pygame.quit()