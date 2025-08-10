# Example file showing a circle moving on screen
from random import randint
import os
import pygame
from Mario import mario, goomba
import math
from game_object import  Mario, Monster

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

def handle_fireball(fireball, targets):
    for direction, ball in fireball:
        if direction == 'right':
            ball.x += 20
        elif direction == 'left':
            ball.x -= 20
        for target in targets:
            if ball.colliderect(target.hitbox):
                target.get_hit()
                fireball.remove((direction,ball))
                break
        if not pygame.display.get_surface().get_rect().contains(ball):
            fireball.remove((direction, ball))

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
mario = Mario(mario_image, 10, 3, 3, punch_sound)
all_objects.append(mario)
objects = [] #obecjts list contains monsters and mario
objects.append(mario)

monsters = [] #monsters list only contains monsters

for x in range(5):
    o = Monster(goomba_image, 200 + x *55, 250,2)
    objects.append(o)
    monsters.append(o)
    all_objects.append(o)

clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

fireball = []
loots=[]
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
    # print(f'w {keys[pygame.K_w]}')
    if keys[pygame.K_w]:
        player_pos.y -= 500 * dt
        mario.move(objects, up=True)
    if keys[pygame.K_s]:
        # player_pos.y += 500 * dt
        mario.move(objects, down=True)
    if keys[pygame.K_a]:
        # player_pos.x -= 500 * dt
        mario.move(objects, left=True)
        mario.change_orientaion('left')
    if keys[pygame.K_d]:
        # player_pos.x += 500 * dt
        mario.move(objects, right=True)
        mario.change_orientaion('right')
    if keys[pygame.K_SPACE]:
        if not mario.attacking and pygame.time.get_ticks() > mario.last_attack+mario.attack_speed:
            punch_sound.play()
            for o in objects:
                if mario.melee_attack(o):
                    o.get_hit()
            mario.stop_attack()
    if keys[pygame.K_f]:
        if pygame.time.get_ticks() > mario.last_attack+mario.attack_speed and mario.fireball_count > 0:
            mario.fireball_count -= 1
            mario.last_attack = pygame.time.get_ticks()
            print('fireball -1')
            if mario.orientation  == 'right':
                fireball.append(('right', pygame.rect.Rect(mario.rect.centerx, mario.rect.centery, 20, 20)))
            elif mario.orientation == 'left':
                fireball.append(('left', pygame.rect.Rect(mario.rect.centerx, mario.rect.centery, 20, 20)))
            # fireball.append(pygame.rect.Rect(mario.rect.centerx, mario.rect.centery,20,20))
    for direction, ball in fireball:
        screen.blit(fireball_image, ball)
    handle_fireball(fireball, objects)
    for o in monsters:
        o.update(mario, objects)
        if o.health_point <0:
            objects.remove(o)
            loots.append(pygame.rect.Rect(o.rect.centerx, o.rect.centery, 20, 20))
        distance_x = mario.rect.centerx - o.rect.centerx
        distance_y = mario.rect.centery - o.rect.centery
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        o_attack_range = o.hitbox.move(10 / distance * distance_x, 10 / distance * distance_y)
        if o_attack_range.colliderect(mario.hitbox) and not mario.hit:
            print('hit')
            # mario.get_hit()
            mario.rect = mario.rect.move(30/distance * distance_x, 30/distance * distance_y)
            mario.hitbox = mario.rect.inflate(-mario.rect.width * 0.25, -mario.rect.height * 0.1)

        screen.blit(o.image, o.rect)
    for l in loots:
        screen.blit(fireball_image, l)
        if mario.hitbox.colliderect(l):
            mario.fireball_count += 5
            loots.remove(l)


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