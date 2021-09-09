from abc import ABC
import pygame
import random
import yaml
import os
import Objects
import Labirint

class Service:
    level_list = list()
    object_list_prob = dict()
    wall = [0]    #sprite for wall 
    floor1 = [0]    #sprite for floor
    floor2 = [0]    #sprite for floor
    floor3 = [0]    #sprite for floor
    MAP_SIZE = (20, 20) #game map size
    
    def __init__(self, sprite_size):
        """Init class Service

        init texture game
        init objects game
        init levels game 

        """
        self.OBJECT_TEXTURE = os.path.join("texture", "objects")
        self.ENEMY_TEXTURE = os.path.join("texture", "enemies")
        self.ALLY_TEXTURE = os.path.join("texture", "ally")

        self.wall[0] = self.create_sprite(os.path.join("texture", "wall.png"), sprite_size)
        self.floor1[0] = self.create_sprite(os.path.join("texture", "Ground_1.png"), sprite_size)
        self.floor2[0] = self.create_sprite(os.path.join("texture", "Ground_2.png"), sprite_size)
        self.floor3[0] = self.create_sprite(os.path.join("texture", "Ground_3.png"), sprite_size)

        object_list_tmp = dict()

        with open("objects.yml", "r") as file:
            object_list_tmp = yaml.load(file.read())
            Service.object_list_prob = object_list_tmp
            object_list_actions = {'reload_game': self.reload_game,
                                   'add_gold': self.add_gold,
                                   'apply_blessing': self.apply_blessing,
                                   'remove_effect': self.remove_effect,
                                   'restore_hp': self.restore_hp,
                                   'apply_enchantment': self.apply_enchantment}

            for obj in Service.object_list_prob['objects']:
                prop = Service.object_list_prob['objects'][obj]
                prop_tmp = object_list_tmp['objects'][obj]
                for i in range(prop_tmp['sprite-count']):
                    img_str = f"{os.path.join(self.OBJECT_TEXTURE, prop_tmp['sprite'][0])}_{i}.png"
                    prop['sprite'].append(self.create_sprite(img_str, sprite_size))
                del prop['sprite'][0]
                prop['action'] = object_list_actions[prop_tmp['action']]

            for ally in Service.object_list_prob['ally']:
                prop = Service.object_list_prob['ally'][ally]
                prop_tmp = object_list_tmp['ally'][ally]
                for i in range(prop_tmp['sprite-count']):
                    img_str = f"{os.path.join(self.ALLY_TEXTURE, prop_tmp['sprite'][0])}_{i}.png"
                    prop['sprite'].append(self.create_sprite(img_str, sprite_size))
                del prop['sprite'][0]
                prop['action'] = object_list_actions[prop_tmp['action']]

            for enemy in Service.object_list_prob['enemies']:
                prop = Service.object_list_prob['enemies'][enemy]
                prop_tmp = object_list_tmp['enemies'][enemy]
                for i in range(prop_tmp['sprite-count']):
                    img_str = f"{os.path.join(self.ENEMY_TEXTURE, prop_tmp['sprite'][0])}_{i}.png"
                    prop['sprite'].append(self.create_sprite(img_str, sprite_size))
                del prop['sprite'][0]

        with open("levels.yml", "r") as file:
            Service.level_list = yaml.load(file.read())['levels']
            Service.level_list.append({'map': self.EndMap.Map(), 'obj': self.EndMap.Objects()})


    def resize(self, sprite_size):
        """Method resize

        Resize texture game

        """
        self.wall[0] = self.create_sprite(os.path.join("texture", "wall.png"), sprite_size)
        self.floor1[0] = self.create_sprite(os.path.join("texture", "Ground_1.png"), sprite_size)
        self.floor2[0] = self.create_sprite(os.path.join("texture", "Ground_2.png"), sprite_size)
        self.floor3[0] = self.create_sprite(os.path.join("texture", "Ground_3.png"), sprite_size)
        with open("objects.yml", "r") as file:
            object_list_tmp = yaml.load(file.read())
            for obj in Service.object_list_prob['objects']:
                prop = Service.object_list_prob['objects'][obj]
                prop['sprite'].clear()
                prop_tmp = object_list_tmp['objects'][obj]
                for i in range(prop_tmp['sprite-count']):
                    img_str = f"{os.path.join(self.OBJECT_TEXTURE, prop_tmp['sprite'][0])}_{i}.png"
                    prop['sprite'].append(self.create_sprite(img_str, sprite_size))
                
                
            for ally in Service.object_list_prob['ally']:
                prop = Service.object_list_prob['ally'][ally]
                prop['sprite'].clear()
                prop_tmp = object_list_tmp['ally'][ally]
                for i in range(prop_tmp['sprite-count']):
                    img_str = f"{os.path.join(self.ALLY_TEXTURE, prop_tmp['sprite'][0])}_{i}.png"
                    prop['sprite'].append(self.create_sprite(img_str, sprite_size))
                
            for enemy in Service.object_list_prob['enemies']:
                prop = Service.object_list_prob['enemies'][enemy]
                prop['sprite'].clear()
                prop_tmp = object_list_tmp['enemies'][enemy]
                for i in range(prop_tmp['sprite-count']):
                    img_str = f"{os.path.join(self.ENEMY_TEXTURE, prop_tmp['sprite'][0])}_{i}.png"
                    prop['sprite'].append(self.create_sprite(img_str, sprite_size))
                

    @staticmethod
    def create_sprite(img, sprite_size):
        """ Method create sprite from image """
        icon = pygame.image.load(img)
        icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
        sprite = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA).convert_alpha()
        sprite.blit(icon, (0, 0))
        return sprite
    
    @staticmethod
    def reload_game(engine, hero):
        """ Method reload game """
        level_list = Service.level_list
        level_list_max = len(level_list) - 1
        engine.level += 1
        engine.objects = []
        hero.position = [1, 1]
        generator = level_list[min(engine.level, level_list_max)]
        _map = generator['map'].get_map()
        engine.load_map(_map)
        engine.add_objects(generator['obj'].get_objects(_map))
        engine.add_hero(hero)

    @staticmethod
    def end_game(engine, hero):
        """ Method end game """
        engine.level = len(Service.level_list) - 2
        Service.reload_game(engine, hero)


    @staticmethod
    def restore_hp(engine, hero):
        """ Method restore hero hp """
        engine.score += 0.1
        hero.hp = hero.calc_max_HP()
        engine.notify("HP restored")

    @staticmethod
    def apply_blessing(engine, hero):
        """ Method apply blessing effect to hero """
        if hero.gold >= int(20 * 1.5**engine.level) - 2 * hero.stats["intelligence"]:
            engine.score += 0.2
            hero.gold -= int(20 * 1.5**engine.level) - \
                             2 * hero.stats["intelligence"]
            if random.randint(0, 1) == 0:
                engine.hero = Objects.Blessing(hero)
                engine.notify("Blessing applied")
            else:
                engine.hero = Objects.Berserk(hero)
                engine.notify("Berserk applied")
        else:
            engine.score -= 0.1
            engine.notify("Nothing has happened")

    @staticmethod
    def remove_effect(engine, hero):
        """ Method remove effect to hero """
        if hero.gold >= int(10 * 1.5**engine.level) - 2 * hero.stats["intelligence"] and "base" in dir(hero):
            hero.gold -= int(10 * 1.5**engine.level) - \
                             2 * hero.stats["intelligence"]
            engine.hero = hero.base
            if engine.hero.hp > engine.hero.calc_max_HP():
                engine.hero.hp = engine.hero.calc_max_HP()
            engine.notify("Effect removed")
        else:
            engine.notify("Nothing has happened")

    @staticmethod
    def apply_enchantment(engine, hero):
        """ Method apply enchantment effect to hero """
        if random.randint(0, 1) == 1:
            engine.score +=100.0
            engine.hero = Objects.Enchantment(hero)
            engine.notify("You are enchanted")
        else:
            engine.notify("Nothing has happened")

    @staticmethod
    def add_gold(engine, hero):
        """ Method add gold to hero """
        if random.randint(1, 10) == 1:
            engine.score -= 0.05
            engine.hero = Objects.Weakness(hero)
            engine.notify("You were cursed")
        else:
            engine.score += 0.1
            gold = int(random.randint(10, 1000) * (1.1**(engine.hero.level - 1)))
            hero.gold += gold
            engine.notify("gold added")
    
    @staticmethod
    def get_empty_coord(_map, objects):
        """ Method search empty coord on map """
        max_cord = (len(_map[0]), len(_map))
        coord = (random.randint(1, max_cord[0]-2), random.randint(1, max_cord[1]-2))
        intersect = True
        while intersect:
            intersect = False
            if _map[coord[1]][coord[0]] == Service.wall:
                intersect = True
                coord = (random.randint(1, max_cord[0]-2),
                         random.randint(1, max_cord[1]-2))
                continue
            for obj in objects:
                if coord == obj.position or coord == (1, 1):
                    intersect = True
                    coord = (random.randint(1, max_cord[0]-2),
                             random.randint(1, max_cord[1]-2))
        return coord
    
    class MapFactory(yaml.YAMLObject):
        """
        
        Class factory map and objects
        Class read parameters from yaml file
        
        """
        @classmethod
        def from_yaml(cls, loader, node):
            """ Constructor for yaml file """
            _map = cls.Map()
            _obj = cls.Objects()
            config = loader.construct_mapping(node)
            _obj.config.update(config)
            return {'map': _map, 'obj': _obj}
    
        @classmethod
        def get_map(cls):
            """ Method get Map class """
            return cls.Map()
    
        @classmethod
        def get_objects(cls):
            """ Method get Objects class """
            return cls.Objects()
        
        class Map():
            """ Class Map """
            pass

        class Objects():
            """ Class Objects """
            pass




    class EndMap(MapFactory):
        """
        
        Class Map - last level game

        """

        yaml_tag = "!end_map"

        class Map:
            """ Class generates a map """
            def __init__(self):
                self.Map = ['000000000000000000000000000000000000000',
                            '0                                     0',
                            '0                                     0',
                            '0  0   0   000   0   0  00000  0   0  0',
                            '0  0  0   0   0  0   0  0      0   0  0',
                            '0  000    0   0  00000  0000   0   0  0',
                            '0  0  0   0   0  0   0  0      0   0  0',
                            '0  0   0   000   0   0  00000  00000  0',
                            '0                                   0 0',
                            '0                                     0',
                            '000000000000000000000000000000000000000'
                            ]
                self.Map = list(map(list, self.Map))
                for i in self.Map:
                    for j in range(len(i)):
                        i[j] = Service.wall if i[j] == '0' else Service.floor1
            
            def get_map(self):
                return self.Map

        class Objects:
            """ Class generates objects """
            def __init__(self):
                self.objects = []
                self.config = {}

            def get_objects(self, _map):
                return self.objects


    class RandomMap(MapFactory):
        """
        
        Class generates a random map

        """
        yaml_tag = "!random_map"

        class Map:
            """ Class generates a map """
            def __init__(self):
                self.Map = [[0 for _ in range(Service.MAP_SIZE[1])] for _ in range(Service.MAP_SIZE[0])]
                for i in range(Service.MAP_SIZE[0]):
                    for j in range(Service.MAP_SIZE[1]):
                        if i == 0 or j == 0 or i == (Service.MAP_SIZE[0] - 1) or j == (Service.MAP_SIZE[1] - 1):
                            self.Map[j][i] = Service.wall
                        else:
                            self.Map[j][i] = [Service.wall, Service.floor1, Service.floor2, Service.floor3][random.randint(0, 3)]

            def get_map(self):
                return self.Map

        class Objects:
            """ Class generates objects """
            def __init__(self):
                self.objects = []
                self.config = {}

            def get_objects(self, _map):
                for obj_name in Service.object_list_prob['objects']:
                    prop = Service.object_list_prob['objects'][obj_name]
                    for _ in range(random.randint(prop['min-count'], prop['max-count'])):
                        coord = Service.get_empty_coord(_map, self.objects)
                        self.objects.append(Objects.Ally("objects",
                            prop['sprite'], prop['action'], coord))

                for obj_name in Service.object_list_prob['ally']:
                    prop = Service.object_list_prob['ally'][obj_name]
                    for _ in range(random.randint(prop['min-count'], prop['max-count'])):
                        coord = Service.get_empty_coord(_map, self.objects)
                        self.objects.append(Objects.Ally("ally",
                            prop['sprite'], prop['action'], coord))

                for obj_name in self.config.keys():
                    prop = Service.object_list_prob['enemies'][obj_name]
                    for _ in range(self.config[obj_name]):
                        coord = Service.get_empty_coord(_map, self.objects)
                        self.objects.append(Objects.Enemy("enemies",
                            prop['sprite'], prop, prop['experience'], coord))

                return self.objects


    class EmptyMap(MapFactory):
        """
        
        Class generates an empty map
        
        """

        yaml_tag = "!empty_map"
        
        class Map:
            """ Class generates a map """
            def __init__(self):
                self.Map = [[0 for _ in range(Service.MAP_SIZE[1])] for _ in range(Service.MAP_SIZE[0])]
                for i in range(Service.MAP_SIZE[0]):
                    for j in range(Service.MAP_SIZE[1]):
                        if i == 0 or j == 0 or i == (Service.MAP_SIZE[0] - 1) or j == (Service.MAP_SIZE[1] - 1):
                            self.Map[j][i] = Service.wall
                        else:
                            self.Map[j][i] = [Service.floor1, Service.floor2, Service.floor3][random.randint(0, 2)]
            
            def get_map(self):
                return self.Map

        
        class Objects:
            """ Class generates objects """
            def __init__(self):
                self.objects = []
                self.config = {}
            
            def get_objects(self,_map):
                for obj_name in Service.object_list_prob['objects']:
                    prop = Service.object_list_prob['objects'][obj_name]
                    for _ in range(random.randint(prop['min-count'], prop['max-count'])):
                        coord = Service.get_empty_coord(_map, self.objects)
                        self.objects.append(Objects.Ally("objects",
                            prop['sprite'], prop['action'], coord))

                for obj_name in Service.object_list_prob['ally']:
                    prop = Service.object_list_prob['ally'][obj_name]
                    for _ in range(random.randint(prop['min-count'], prop['max-count'])):
                        coord = Service.get_empty_coord(_map, self.objects)
                        self.objects.append(Objects.Ally("ally",
                            prop['sprite'], prop['action'], coord))

                for obj_name in self.config.keys():
                    prop = Service.object_list_prob['enemies'][obj_name]
                    for _ in range(self.config[obj_name]):
                        coord = Service.get_empty_coord(_map, self.objects)
                        self.objects.append(Objects.Enemy("enemies",
                            prop['sprite'], prop, prop['experience'], coord))

                return self.objects


    class SpecialMap(MapFactory):
        """
        
        Class generates a maze
        
        """

        yaml_tag = "!special_map"

        class Map:
            """ Class generates a map """
            def __init__(self):
                self.Map = Labirint.Labirint((Service.MAP_SIZE[0]-1,Service.MAP_SIZE[1]-1)).get_labirint()
                for i in range(len(self.Map)):
                    for j in range(len(self.Map[0])):
                        if self.Map[j][i] == 0:
                            self.Map[j][i] = Service.wall
                        else:
                            self.Map[j][i] = [Service.floor1, Service.floor2, Service.floor3][random.randint(0, 2)]
            
            def get_map(self):
                return self.Map
        

        class Objects:
            """ Class generates objects """
            def __init__(self) -> None:
                self.objects = []
                self.config = {}
            
            def get_objects(self, _map):
                for obj_name in Service.object_list_prob['objects']:
                    prop = Service.object_list_prob['objects'][obj_name]
                    for i in range(random.randint(prop['min-count'], prop['max-count'])):
                        coord = Service.get_empty_coord(_map, self.objects)
                        self.objects.append(Objects.Ally("objects",
                            prop['sprite'], prop['action'], coord))

                for obj_name in Service.object_list_prob['ally']:
                    prop = Service.object_list_prob['ally'][obj_name]
                    for i in range(random.randint(prop['min-count'], prop['max-count'])):
                        coord = Service.get_empty_coord(_map, self.objects)
                        self.objects.append(Objects.Ally("ally",
                            prop['sprite'], prop['action'], coord))

                for obj_name in self.config.keys():
                    prop = Service.object_list_prob['enemies'][obj_name]
                    for i in range(self.config[obj_name]):
                        coord = Service.get_empty_coord(_map, self.objects)
                        self.objects.append(Objects.Enemy("enemies",
                            prop['sprite'], prop, prop['experience'], coord))
                return self.objects
    
