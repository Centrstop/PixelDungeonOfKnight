from Service import Service
from Objects import Hero
import os

class GameEngine:
    """
    
    Class implements main logic of the game

    """
    def __init__(self, sprite_size) -> None:
        self.objects = []
        self.map = None
        self.hero = None
        self.level = -1
        self.working = True
        self.subscribers = set()
        self.score = 0.
        self.game_process = True
        self.show_help = False
        self.sprite_size = sprite_size
        self.show_minimap = True
        self.base_stats = {
            "strength": 20,
            "endurance": 20,
            "intelligence": 5,
            "luck": 5
        }

    def subscribe(self, obj):
        """ Method subscribe objects for messaging """
        self.subscribers.add(obj)

    def unsubscribe(self, obj):
        """ Method unsubscribe objects """
        if obj in self.subscribers:
            self.subscribers.remove(obj)

    def notify(self, message):
        """ Method sends message to objects """
        for i in self.subscribers:
            i.update(message)

    # HERO
    def create_hero(self):
        """ Method creation hero """

        self.img_count_hero = 4 # number of pictures on different sides of hero

        sprite_idle = []    #images as we move down
        sprite_left = []    #images as we move left
        sprite_right = []   #images as we move right

        for i in range(self.img_count_hero):
            img_str_idle = f"{os.path.join('texture', 'Hero')}_{i}.png"
            img_str_left = f"{os.path.join('texture', 'HeroLeft')}_{i}.png"
            img_str_right = f"{os.path.join('texture', 'HeroRight')}_{i}.png"
            sprite_idle.append(Service.create_sprite(img_str_idle, self.sprite_size))
            sprite_left.append(Service.create_sprite(img_str_left, self.sprite_size))
            sprite_right.append(Service.create_sprite(img_str_right, self.sprite_size))

        hero = Hero(self.base_stats, sprite_idle)
        hero.sprite_left = sprite_left
        hero.sprite_right = sprite_right
        self.add_hero(hero)

    def add_hero(self, hero):
        """ Method add hero """
        self.hero = hero
    
    def interact(self):
        """ Method interaction with hero"""
        for obj in self.objects:
            if list(obj.position) == self.hero.position:
                self.delete_object(obj)
                obj.interact(self, self.hero)

    # RESIZE
    def resize(self, sprite_size):
        """ Method resize game elements """
        self.sprite_size = sprite_size
        sprite_idle = []
        sprite_left = []
        sprite_right = []
        for i in range(self.img_count_hero):
            img_str_idle = f"{os.path.join('texture', 'Hero')}_{i}.png"
            img_str_left = f"{os.path.join('texture', 'HeroLeft')}_{i}.png"
            img_str_right = f"{os.path.join('texture', 'HeroRight')}_{i}.png"
            sprite_idle.append(Service.create_sprite(img_str_idle, self.sprite_size))
            sprite_left.append(Service.create_sprite(img_str_left, self.sprite_size))
            sprite_right.append(Service.create_sprite(img_str_right, self.sprite_size))

        self.hero.sprite = sprite_idle  
        self.hero.sprite_left = sprite_left
        self.hero.sprite_right = sprite_right

    # MOVEMENT
    def move_up(self):
        """ Method moves hero up """
        self.score += 0.02
        if self.map[self.hero.position[1] - 1][self.hero.position[0]] == Service.wall:
            return
        self.hero.up()
        self.interact()

    def move_down(self):
        """ Method moves hero down """
        self.score += 0.02
        if self.map[self.hero.position[1] + 1][self.hero.position[0]] == Service.wall:
            return
        self.hero.down()
        self.interact()

    def move_left(self):
        """ Method moves hero left """
        self.score += 0.02
        if self.map[self.hero.position[1]][self.hero.position[0] - 1] == Service.wall:
            return
        self.hero.left()
        self.interact()

    def move_right(self):
        """ Method moves hero right """
        self.score += 0.02
        if self.map[self.hero.position[1]][self.hero.position[0] + 1] == Service.wall:
            return
        self.hero.right()
        self.interact()

    # MAP
    def load_map(self, game_map):
        """ Method saves map """
        self.map = game_map

    # OBJECTS
    def add_object(self, obj):
        """ Method add object """
        self.objects.append(obj)

    def add_objects(self, objects):
        """ Method add objects """
        self.objects.extend(objects)

    def delete_object(self, obj):
        """ Method delete object """
        self.objects.remove(obj)

    def delete_objects(self):
        """ Method delete objects """
        self.objects.clear()
    
    def reload_game(self):
        """ Method reload game """
        Service.reload_game(self, self.hero)
    
    def end_game(self):
        """ Method end game """
        Service.end_game(self, self.hero)