import pygame
import math

from main import objects
from random import randint

class GameObject():
    def __init__(self, image, x, y, speed, health_point = 5):
        self.speed = speed
        self.image = image
        self.rect = self.image.get_rect().move(x,y)
        self.hitbox = self.rect.inflate(-self.rect.width*0.25, -self.rect.height*0.1)
        self.attacking = False
        self.hit = False
        self.last_hit = 0
        self.last_attack = 0
        self.attack_speed = 1000
        self.health_point = health_point

    def get_hit(self):
        if not self.hit and pygame.time.get_ticks() - self.last_hit > 1000:
            self.hit = True
            self.last_hit = pygame.time.get_ticks()
            self.original = self.image
            self.health_point -= 1

    def check_collision(self, rect, objects):
        # obstacle = objects.copy()
        # obstacle.append(mario)
        for obj in objects:
            if obj is not self and rect.colliderect(obj.hitbox):
                return True
        return False

class Mario(GameObject):
    def __init__(self, image, x, y, speed, punch_sound = None, health_point = 5, fireball_count = 5):
        super.__init__(image, x, y, speed, health_point = health_point)
        self.orientation = 'right'
        self.fireball_count = fireball_count
        self.punch_sound = punch_sound

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

    def change_orientaion(self, orientation):
        flip = pygame.transform.flip
        self.original = self.image
        if self.orientation != orientation and orientation == 'right':
            self.orientation = orientation
            self.image = flip(self.original, 1, 0)
        if self.orientation != orientation and orientation == 'left':
            self.orientation = orientation
            self.image = flip(self.original, 1, flip_y=0)

    def move(self, objects, up=False, down=False, left=False, right=False):
        if right:
            new_rect = self.rect.move(self.speed, 0)
        if left:
            new_rect = self.rect.move(-self.speed, 0)
        if down:
            new_rect = self.rect.move(0, self.speed)
        if up:
            new_rect = self.rect.move(0, -self.speed)

        new_hitbox = new_rect.inflate(-self.rect.width * 0.25, -self.rect.height * 0.1)
        if not pygame.display.get_surface().get_rect().contains(new_rect):
            return
        if self.check_collision(new_hitbox, objects):
            return
        self.rect = new_rect
        self.hitbox = new_hitbox


class Monster(GameObject):
    def __init__(self, image, x, y, speed, punch_sound = None, health_point = 5):
        super.__init__(image, x, y, speed, health_point = health_point)


    def update(self, mario, objects):
        if self.hit:
            self.spin()
        else:
            self.move(mario, objects)

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

    def move(self, mario, objects):
        # self.pos.right += self.speed * randint(-1,1)
        # self.pos.top += self.speed * randint(-1,1)
        distance_x = mario.rect.centerx - self.rect.centerx
        distance_y = mario.rect.centery - self.rect.centery
        distance = math.sqrt(distance_x**2 + distance_y**2)
        speed_x = distance_x/distance*self.speed
        speed_y = distance_y/distance*self.speed
        new_rect = self.rect.move(speed_x*(1+randint(-1,0)),speed_y*(1+randint(-1,0)))
        # new_rect = self.rect.move(self.speed * randint(-1,1),self.speed * randint(-1,1))
        new_hitbox = new_rect.inflate(-self.rect.width*0.25, -self.rect.height*0.1)
        if not pygame.display.get_surface().get_rect().contains(new_rect):
            return
        if self.check_collision(new_hitbox, objects):
            return
        self.rect = new_rect
        self.hitbox = new_hitbox


