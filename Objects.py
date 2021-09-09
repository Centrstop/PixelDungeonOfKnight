from abc import ABC, abstractmethod

class Interactive(ABC):
    """ Abstract interactive object class """
    @abstractmethod
    def interact(self, engine, hero):
        pass


class AbstractObject(ABC):
    """ Abstract object class """
    @abstractmethod
    def __init__(self) -> None:
        pass

    def draw(self,display):
        pass


class Ally(AbstractObject, Interactive):
    """
    
    Class implements helper items
    Interaction with hero applies various effects

    """

    def __init__(self, name, icon, action, position):
        """ Initializing ally class """
        self.sprite = icon
        self.action = action
        self.position = position
        self.name = name
        self.delay_frame = 3
        self.sprite_index = 0
        self.sprite_delay = self.delay_frame

    def interact(self, engine, hero):
        """ Interaction hero and object """
        self.action(engine, hero)

    def draw(self, display, _min, size):
        """Draw object Ally"""
        if self.sprite_delay > 0:
            self.sprite_delay -= 1
        else:
            self.sprite_index += 1
            self.sprite_delay = self.delay_frame
        if self.sprite_index < len(self.sprite):
            pass
        else:
            self.sprite_index = 0
        
        display.blit(self.sprite[self.sprite_index], 
                     ((self.position[0] - _min[0]) * size,
                      (self.position[1] - _min[1]) * size))


class Creature(AbstractObject):
    """
    
    Class implements an abstract creature

    """
    def __init__(self, icon, stats, position):
        """ Initializing creature """
        self.sprite = icon
        self.stats = stats.copy()
        self.position = position
        self.hp = self.calc_max_HP()

    def calc_max_HP(self):
        """ Calculate maximum health of a creature """
        max_hp = 5 + self.stats["endurance"] * 2
        return max_hp
    
    def draw(self, display, _min, size):
        """Draw creature"""
        min_x, min_y = _min[0], _min[1]
        display.blit(self.sprite, ((self.position[0] - min_x) * size,
                                   (self.position[1] - min_y) * size))


class Hero(Creature):
    """
    
    Class implements logic of hero

    """
    def __init__(self, stats, icon):
        """ Initializing hero """
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        self.sprite_left = []
        self.sprite_right = []
        self.moved_left = False
        self.moved_right = False
        self.delay_frame = 2
        self.sprite_index = 0
        self.sprite_delay = self.delay_frame
        super().__init__(icon, stats, pos)

    def left(self):
        """ Hero moves to left """
        self.moved_left = True
        self.moved_right = False
        self.sprite_index = 0
        self.position[0] -= 1
    
    def right(self):
        """ Hero moves to right """
        self.moved_left = False
        self.moved_right = True
        self.sprite_index = 0
        self.position[0] += 1
    
    def up(self):
        """ Hero moves to up """
        self.moved_left = False
        self.moved_right = False
        self.sprite_index = 0
        self.position[1] -= 1
    
    def down(self):
        """ Hero moves to down """
        self.moved_left = False
        self.moved_right = False
        self.sprite_index = 0
        self.position[1] += 1

    def calc_max_EXP(self):
        """ Calculate maximum experience """
        return (100 * (2 ** (self.level - 1)))

    def level_up(self):
        """ Increase level of hero """
        while self.exp >= self.calc_max_EXP():
            yield "level up!"
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.hp = self.calc_max_HP()
    
    def draw(self, display, _min, size):
        """ Draw Hero """
        if self.sprite_delay > 0:
            self.sprite_delay -= 1
        else:
            self.sprite_index += 1
            self.sprite_delay = self.delay_frame
        if self.sprite_index < len(self.sprite):
            pass
        else:
            self.sprite_index = 0
        if not self.moved_right and not self.moved_left:
            display.blit(self.sprite[self.sprite_index], 
                        ((self.position[0] - _min[0]) * size,
                        (self.position[1] - _min[1]) * size))
        elif self.moved_left:
            display.blit(self.sprite_left[self.sprite_index], 
                        ((self.position[0] - _min[0]) * size,
                        (self.position[1] - _min[1]) * size))
        else:
            display.blit(self.sprite_right[self.sprite_index], 
                        ((self.position[0] - _min[0]) * size,
                        (self.position[1] - _min[1]) * size))


class Enemy(Creature, Interactive):
    """ 
    
    Class implements enemy
    
    """
    def __init__(self, name, icon, stats, exp, position):
        """ Initializing enemy """
        super().__init__(icon, stats, position)
        self.exp = exp
        self.name = name
        self.delay_frame = 2
        self.sprite_index = 0
        self.hp = self.calc_max_HP()
        self.sprite_delay = self.delay_frame
    
    def interact(self, engine, hero):
        """ Interaction of enemy and hero """
        engine.score += 50 * (self.hp / hero.hp)    #points for killing an enemy
        hero.exp += self.exp    #experience for killing an enemy
        hero.hp -= int(self.hp * 0.2)   #spent health for killing an enemy  

        if hero.hp > hero.calc_max_HP():
            hero.hp = hero.calc_max_HP()
        for message in hero.level_up():
            engine.notify(message)
        if hero.hp < 1:
            hero.hp = 0
            engine.notify("You lose")
            engine.end_game()

    
    def draw(self, display, _min, size):
        """ Draw Enemy """
        if self.sprite_delay > 0:
            self.sprite_delay -= 1
        else:
            self.sprite_index += 1
            self.sprite_delay = self.delay_frame
        if self.sprite_index < len(self.sprite):
            pass
        else:
            self.sprite_index = 0
        
        display.blit(self.sprite[self.sprite_index], 
                     ((self.position[0] - _min[0]) * size,
                      (self.position[1] - _min[1]) * size))


class Effect(Hero):
    """
    
    Base class implement effects applied to hero

    """
    def __init__(self, base):
        """ Initializing class """
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    @property
    def moved_right(self):
        return self.base.moved_right
    
    @moved_right.setter
    def moved_right(self, value):
        self.base.moved_right = value

    @property
    def moved_left(self):
        return self.base.moved_left
    
    @moved_left.setter
    def moved_left(self, value):
        self.base.moved_left = value

    @property
    def sprite_right(self):
        return self.base.sprite_right
    
    @sprite_right.setter
    def sprite_right(self, value):
        self.base.sprite_right = value

    @property
    def sprite_left(self):
        return self.base.sprite_left
    
    @sprite_left.setter
    def sprite_left(self, value):
        self.base.sprite_left = value

    @property
    def delay_frame(self):
        return self.base.delay_frame
    
    @delay_frame.setter
    def delay_frame(self, value):
        self.base.delay_frame = value
    
    @property
    def sprite_index(self):
        return self.base.sprite_index
    
    @sprite_index.setter
    def sprite_index(self, value):
        self.base.sprite_index = value

    @property
    def sprite_delay(self):
        return self.base.sprite_delay
    
    @sprite_delay.setter
    def sprite_delay(self, value):
        self.base.sprite_delay = value

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite
    
    @sprite.setter
    def sprite(self, value):
        self.base.sprite = value

    @abstractmethod
    def apply_effect(self):
        pass


class Berserk(Effect):
    """ Class implements Berserk effect """
    def __init__(self, base):
        super().__init__(base)

    def apply_effect(self):
        self.stats["strength"] += 20


class Blessing(Effect):
    """ Class implements Blessing effect """
    def __init__(self, base):
        super().__init__(base)

    def apply_effect(self):
        self.stats["luck"] += 10


class Weakness(Effect):
    """ Class implements Weakness effect """
    def __init__(self, base):
        super().__init__(base)

    def apply_effect(self):
        self.stats["strength"] -= 20
        self.stats["luck"] -= 10


class Enchantment(Effect):
    """ Class implements Enchantment effect """
    def __init__(self, base):
        super().__init__(base)
    
    def apply_effect(self):
        self.stats["endurance"] += 1
        self.stats["luck"] -= 1
