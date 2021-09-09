import pygame
import collections
from Service import Service

colors = {
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255),
    "red": (255, 0, 0, 255),
    "green": (0, 255, 0, 255),
    "blue": (0, 0, 255, 255),
    "wooden": (187, 132, 65, 255),
    "hero" : (128,128,128,128)
}


class ScreenHandle(pygame.Surface):
    """
    
    Base class rendering surface
    
    """
    def __init__(self, *args, **kwargs):
        """ Initializing class """
        if len(args) > 1:
            self.successor = args[-1]
            self.next_coord = args[-2]
            args = args[:-2]
        else:
            self.successor = None
            self.next_coord = (0, 0)
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])

    def draw(self, canvas):
        """ Method draw surface """
        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)

    def connect_engine(self, engine):
        """ Method connect game engine """
        engine.subscribe(self)
        self.engine = engine
        if self.successor is not None:
            self.successor.connect_engine(engine)
    
    def update(self, value):
        """ Method receiving notifications """
        pass




class GameSurface(ScreenHandle):
    """
    
    Class implements rendering of game surface
    
    """
        
    def draw_hero(self, _min, size):
        """ Method implements drawing of hero """
        self.engine.hero.draw(self, _min, size)

    def draw_map(self, _min):
        """ Method implements drawing of map """
        min_x = _min[0]
        min_y = _min[1]

        self.fill(colors["wooden"])
        if self.engine.map:
            for i in range(len(self.engine.map[0]) - min_x):
                for j in range(len(self.engine.map) - min_y):
                    self.blit(self.engine.map[min_y + j][min_x + i][
                              0], (i * self.engine.sprite_size, j * self.engine.sprite_size))
        else:
            self.fill(colors["white"])

    def draw_object(self, sprite, coord, _min):
        """ Method implements drawing of object """
        size = self.engine.sprite_size
        min_x, min_y = _min[0], _min[1]
        self.blit(sprite, ((coord[0] - min_x) * size,
                           (coord[1] - min_y) * size))

    def draw(self, canvas):
        """ Method implements drawing of game surface """
        size = self.engine.sprite_size
        min_x = 0
        min_y = 0

        max_view_sprites_x = int(self.get_width() / size + 0.5)
        max_view_sprites_y = int(self.get_height() / size + 0.5)

        max_map_sprites_x = len(self.engine.map[0])
        max_map_sprites_y = len(self.engine.map)

        center_view_x = max_view_sprites_x // 2
        center_view_y = max_view_sprites_y // 2

        if max_view_sprites_x < max_map_sprites_x and self.engine.hero.position[0] > center_view_x:
            min_x = self.engine.hero.position[0] - center_view_x
            if self.engine.hero.position[0] > (max_map_sprites_x - center_view_x):
                min_x = max_map_sprites_x - (2 * center_view_x)
        
        if max_view_sprites_y < max_map_sprites_y and self.engine.hero.position[1] > center_view_y:
            min_y = self.engine.hero.position[1] - center_view_y
            if self.engine.hero.position[1] > (max_map_sprites_y - center_view_y):
                min_y = max_map_sprites_y - (2 * center_view_y)

        self.draw_map((min_x, min_y))
        for obj in self.engine.objects:
            obj.draw(self, (min_x, min_y), size)
        self.draw_hero((min_x, min_y),size)

        super().draw(canvas)

class MiniMap(ScreenHandle):
    """
    
    Class implements rendering of mini map surface
    
    """
    def draw(self, canvas):
        """ Method implements drawing of mini map surface """
        self.fill(colors["wooden"])
        self.point_size = int(self.get_height() / len(self.engine.map[0]))
        if not self.engine.show_minimap:
            super().draw(canvas)
            return None
        if self.engine.map:
            for i in range(len(self.engine.map)):
                for j in range(len(self.engine.map[0])):
                    if self.engine.map[i][j] == Service.wall:
                        color = colors["black"]
                        pygame.draw.rect(self, color,
                                         (j*self.point_size,
                                          i*self.point_size,
                                          self.point_size,
                                          self.point_size))
        for obj in self.engine.objects:
            if obj.name == "objects":
                color = colors["green"]
            elif obj.name == "enemies":
                color = colors["red"]
            elif obj.name == "ally":
                color = colors["blue"]
            else:
                color = colors["wooden"]
            pygame.draw.rect(self, color,
                             (obj.position[0]*self.point_size, 
                              obj.position[1]*self.point_size, 
                              self.point_size,
                              self.point_size))
        pygame.draw.rect(self, colors['white'],
                         (self.engine.hero.position[0]*self.point_size,
                          self.engine.hero.position[1]*self.point_size,
                          self.point_size, 
                          self.point_size))
        super().draw(canvas)
        

class ProgressBar(ScreenHandle):
    """
    
    Class implements rendering of progress bar surface
    
    """
    def __init__(self, *args, **kwargs):
        """ Initializing class """
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])

    def draw(self, canvas):
        """ Method implements drawing of progress bar surface """
        self.fill(colors["wooden"])
        width = self.get_width()
        height = self.get_height()
        pix_w = width / 640 #Set relative pixel size
        pix_h = height / 120 #Set relative pixel size
        font_size = int(20 * pix_h) #Set relative font size

        pygame.draw.rect(self, colors["black"], (int(50 * pix_w), int(30 * pix_h), int(200 * pix_w), int(30 * pix_h)), 2)
        pygame.draw.rect(self, colors["black"], (int(50 * pix_w), int(70 * pix_h), int(200 * pix_w), int(30 * pix_h)), 2)

        pygame.draw.rect(self, colors["red"], 
                         (int(50 * pix_w), int(30 * pix_h), int(200 * pix_w) * self.engine.hero.hp / self.engine.hero.calc_max_HP(), int(30 * pix_h)))
        pygame.draw.rect(self, colors["green"],
                         (int(50 * pix_w), int(70 * pix_h), int(200 * pix_w) * self.engine.hero.exp / self.engine.hero.calc_max_EXP(), int(30 * pix_h)))

        font = pygame.font.SysFont("comicsansms", font_size)
        self.blit(font.render(f'Hero at {self.engine.hero.position}', True, colors["black"]),
                  (int(300 * pix_w), int(0 * pix_h)))

        self.blit(font.render(f'{self.engine.level} floor', True, colors["black"]),
                  (int(10 * pix_w), int(0 * pix_h)))

        self.blit(font.render(f'HP', True, colors["black"]),
                  (int(10 * pix_w), int(30 * pix_h)))
        self.blit(font.render(f'Exp', True, colors["black"]),
                  (int(10 * pix_w), int(70 * pix_h)))

        self.blit(font.render(f'{self.engine.hero.hp}/{self.engine.hero.calc_max_HP()}', True, colors["black"]),
                  (int(60 * pix_w), int(30 * pix_h)))
        self.blit(font.render(f'{self.engine.hero.exp}/{self.engine.hero.calc_max_EXP()}', True, colors["black"]),
                  (int(60 * pix_w), int(70 * pix_h)))

        self.blit(font.render(f'Level', True, colors["black"]),
                  (int(300 * pix_w), int(30 * pix_h)))
        self.blit(font.render(f'Gold', True, colors["black"]),
                  (int(300 * pix_w), int(70 * pix_h)))

        self.blit(font.render(f'{self.engine.hero.level}', True, colors["black"]),
                  (int(360 * pix_w), int(30 * pix_h)))
        self.blit(font.render(f'{self.engine.hero.gold}', True, colors["black"]),
                  (int(360 * pix_w), int(70 * pix_h)))

        self.blit(font.render(f'Str', True, colors["black"]),
                  (int(420 * pix_w), int(30 * pix_h)))
        self.blit(font.render(f'Luck', True, colors["black"]),
                  (int(420 * pix_w), int(70 * pix_h)))

        self.blit(font.render(f'{self.engine.hero.stats["strength"]}', True, colors["black"]),
                  (int(480 * pix_w), int(30 * pix_h)))
        self.blit(font.render(f'{self.engine.hero.stats["luck"]}', True, colors["black"]),
                  (int(480 * pix_w), int(70 * pix_h)))

        self.blit(font.render(f'SCORE', True, colors["black"]),
                  (int(550 * pix_w), int(30 * pix_h)))
        self.blit(font.render(f'{self.engine.score:.4f}', True, colors["black"]),
                  (int(550 * pix_w), int(70 * pix_h)))

        super().draw(canvas)


class InfoWindow(ScreenHandle):
    """
    
    Class implements rendering of info window surface
    
    """
    def __init__(self, *args, **kwargs):
        """ Initializing class """
        super().__init__(*args, **kwargs)
        self.len = 20
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)

    def update(self, value):
        """ Method receiving notifications """
        self.data.append(f"> {str(value)}")

    def draw(self, canvas):
        """ Method implements drawing of info window surface """
        self.fill(colors["wooden"])
        pix_h = self.get_height() / 480
        pix_w = self.get_width() / 160

        font_size = int(10 * pix_h)
        font = pygame.font.SysFont("comicsansms", font_size)

        shift = int(18 * pix_h)
        
        for i, text in enumerate(self.data):
            self.blit(font.render(text, True, colors["black"]),
                      (int(10 * pix_w), int(20 * pix_h) + shift * i))

        super().draw(canvas)



class HelpWindow(ScreenHandle):
    """
    
    Class implements rendering of help window surface
    
    """
    def __init__(self, *args, **kwargs):
        """ Initializing class """
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)
        self.data.append([" →", "Move Right"])
        self.data.append([" ←", "Move Left"])
        self.data.append([" ↑ ", "Move Top"])
        self.data.append([" ↓ ", "Move Bottom"])
        self.data.append([" H ", "Show Help"])
        self.data.append([" M ", "Show Minimap"])
        self.data.append(["Num+", "Zoom +"])
        self.data.append(["Num-", "Zoom -"])
        self.data.append([" R ", "Restart Game"])
    
    def draw(self, canvas):
        """ Method implements drawing of help window surface """
        if not self.engine.show_help:
            self.fill((0, 0, 0, 0))
            super().draw(canvas)
            return None
        else:
            alpha = 128
            self.fill((0, 0, 0, alpha))
            size = self.get_size()
            pix_h = self.get_height() / 800
            pix_w = self.get_width() / 600
            line_size = 5
            font_size = int(24 * pix_h)
            font = pygame.font.SysFont("sans", font_size)
            if self.engine.show_help:
                pygame.draw.lines(self, colors["red"], True,
                                  [(0, 0), (size[0], 0), 
                                   (size[0], size[1]), (0, size[1])],
                                  line_size)
                for i, text in enumerate(self.data):
                    self.blit(font.render(text[0], True, ((128, 128, 255))),
                              (int(200 * pix_w), int(100 * pix_h) + int(30 * pix_h) * i))
                    self.blit(font.render(text[1], True, ((128, 128, 255))),
                              (int(250 * pix_w), int(100 * pix_h) + int(30 * pix_h) * i))
        
        super().draw(canvas)
