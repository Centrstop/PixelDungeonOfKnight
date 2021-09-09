import pygame
import ScreenEngine as SE
import Logic
from Service import Service

class MainWindow:
    """

    Class main game window    

    """
    def __init__(self, title = "Pixel Dungeon of Knights", screen_size = (800, 600), sprite_size = 40):
        """ Initializing main game window """
        #Initializing pygame
        pygame.init()
        self._game_display = pygame.display.set_mode(screen_size)
        pygame.display.set_caption(title)
        
        #Initializing clock
        self._clock = pygame.time.Clock()

        #set size of game map
        Service.MAP_SIZE = (40,40)

        #Set size of window
        self._screen_size = screen_size
        self._sprite_size = sprite_size
        self._canvas_size = (int(screen_size[0] * 0.8), int(screen_size[1] * 0.8))

        self._engine = None     #game engine
        self._drawer = None     #game rendering
        self._service = None    #game functions
    
    def _create_game(self):
        """ Method create game """
        self._engine = Logic.GameEngine(self._sprite_size)
        self._engine.create_hero()
        self._service = Service(self._sprite_size)
        self._engine.reload_game()
        screen = self._screen_size
        canvas = self._canvas_size
        self._drawer = SE.GameSurface(canvas, pygame.SRCALPHA, canvas,
                       SE.MiniMap(((screen[0]-canvas[0]), (screen[1]-canvas[1])), pygame.SRCALPHA, (0, canvas[1]),
                       SE.ProgressBar((canvas[0], (screen[1] - canvas[1])), (canvas[0],0),
                       SE.InfoWindow(((screen[0]-canvas[0]), canvas[1]), (0, 0),
                       SE.HelpWindow(screen, pygame.SRCALPHA, (0, 0),
                       SE.ScreenHandle((0,0)))))))
        self._drawer.connect_engine(self._engine)

    def _resize_game(self):
        """ Method resize game element """
        self._engine.resize(self._sprite_size)
        self._service.resize(self._sprite_size)
        
    def _quit(self):
        """ Method exit game """
        pygame.display.quit()
        pygame.quit()
        exit(0)
    
    def start_game_loop(self):
        """ Event loop game """
        self._create_game()
        while self._engine.working:
            self._clock.tick(30)   #delay for 30 fps
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._engine.working = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        self._engine.show_help = not self._engine.show_help
                    if event.key == pygame.K_KP_PLUS:
                        self._sprite_size += 1 if self._sprite_size < 100 else 0
                        self._resize_game()
                    if event.key == pygame.K_KP_MINUS:
                        self._sprite_size -= 1 if self._sprite_size > 20 else 0
                        self._resize_game()
                    if event.key == pygame.K_r:
                        self._create_game()
                    if event.key == pygame.K_m:
                        self._engine.show_minimap = not self._engine.show_minimap
                    if event.key == pygame.K_ESCAPE:
                        self._engine.working = False
                    if self._engine.game_process:
                        if event.key == pygame.K_UP:
                            self._engine.move_up()
                        elif event.key == pygame.K_DOWN:
                            self._engine.move_down()
                        elif event.key == pygame.K_LEFT:
                            self._engine.move_left()
                        elif event.key == pygame.K_RIGHT:
                            self._engine.move_right()
                    else:
                        if event.key == pygame.K_RETURN:
                            self._reset_game()

            self._game_display.blit(self._drawer, (0, 0))
            self._drawer.draw(self._game_display)
            pygame.display.update()
        self._quit()


if __name__ == "__main__":
    game = MainWindow(screen_size=(800,600), sprite_size=60)
    game.start_game_loop()







