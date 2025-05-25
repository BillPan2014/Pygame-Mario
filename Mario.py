import random
class Character:
    def __init__(self, name, ability, size = 'big', lives = 5, position = [0, 0]):
        self.name = name
        self.size = size
        self.position = position
        self.ability = ability
        self.lives = lives
        self.weapon = Weapon(name = 'Fist', special = 'none', uses = 99999999999999)
    def attack(self):
        self.weapon.uses -= 1
        self.position[0]
    def move(self,direction):
        if direction == 'left':
            self.position[0] -= 1
        if direction == 'right':
            self.position[0] += 1
        print(f'You are at {self.position}!')

    def jump(self):
        self.position[1] += 5
        print(f'You are at {self.position}!')

    def fall(self):
        self.position[1] -= 1
        print(f'You are at {self.position}!')

    def die(self):
        if self.size == 'big':
                if random.random() > 0.2:
                    self.size = 'small'
                    print(f'You are small now!')
                elif random.random() > 0.8:
                    self.lives -= 1
                    print(f'Critical hit! You have {self.lives} lives! You are big now!')
                    self.size = 'big'
                else:
                    print(f'Miss! You still have {self.lives} lives! You are still big!')
        else:
            if random.random() > 0.2:
                self.lives -=1
                print(f'You have {self.lives} lives! You are big now!')
                self.size = 'big'
            elif random.random() > 0.8:
                self.lives -= 1
                self.size = 'small'
                print(f'Critical hit! You have {self.lives} lives! You are small now!')
            else:
                print(f'Miss! You still have {self.lives} lives! You are still small!')

    # def pick_up(self):
    #     if

class Npc(Character):
    def __init__(self, name, ability, position, items):
        super().__init__(name,ability,position=position)
        self.items = items
        self.weapon = Weapon(name = 'Bow', special = 'none', range = 10)
    def interact(self):
        print(f'Hello I am {self.name}.')
        wanted = input('What can I do for you?\n')
        if wanted == 'buy':
            print(f'I have {self.items}')
    def move(self,direction):
        if direction == 'left':
            self.position[0] -= 2
        if direction == 'right':
            self.position[0] += 2
        print(f'You are at {self.position}!')
    def jump(self):
        self.position[1] += 3
        print(f'You are at {self.position}!')


class Enemy(Character):
    def __init__(self, name, ability, items, position=[10,0]):
        super().__init__(name, ability, position=position)
        self.items = items
    def move(self,direction):
        if direction == 'left':
            self.position[0] -= 1
        if direction == 'right':
            self.position[0] += 1
        print(f'You are at {self.position}!')

    def jump(self):
        self.position[1] += 5
        print(f'You are at {self.position}!')

    def fall(self):
        self.position[1] -= 1
        print(f'You are at {self.position}!')

    def die(self):
        if self.size == 'big':
            self.size = 'small'
            print(f'It is small now!')
        else:
            self.lives -=1
            print(f'It have {self.lives} lives!')
            self.size = 'big'

class Weapon:
    def __init__(self,special, name, range = 2, uses = 1000, damage = 1):
        self.damage = damage
        self.range = range
        self.name = name
        self.uses = uses
        self.special = special
    def repair(self):
        self.uses += 100

mario = Character(name = 'Mario', ability = 'none')
trader = Npc(name = 'Trader', ability = 'none', position = [0, 0], items = {'Extra life':10, 'Size':5, 'Sword':5, 'Bow':10})
goomba = Enemy(name = 'Goomba', ability = 'none', items = 'none', position = [20, 100])

