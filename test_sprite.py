import pygame

def create_sprite(img, sprite_size):
        """ Method create sprite from image """
        icon = pygame.image.load(img)
        icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
        sprite = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA).convert_alpha()
        sprite.blit(icon, (0, 0))
        return sprite

class TestSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(TestSprite, self).__init__()
        self.images = []
        self.images.append(create_sprite('image_part_001.png',60))
        self.images.append(create_sprite('image_part_002.png',60))
        self.images.append(create_sprite('image_part_003.png',60))
        self.images.append(create_sprite('image_part_004.png',60))
        self.images.append(create_sprite('image_part_005.png',60))
        self.images.append(create_sprite('image_part_006.png',60))
        self.images.append(create_sprite('image_part_007.png',60))
        self.images.append(create_sprite('image_part_008.png',60))
        self.images.append(create_sprite('image_part_009.png',60))
        self.images.append(create_sprite('image_part_010.png',60))
        # assuming both images are 64x64 pixels

        self.index = 0
        self.count_delay = 2
        self.image = self.images[self.index]
        self.rect = pygame.Rect(5, 5, 64, 64)

    def update(self):
        '''This method iterates through the elements inside self.images and 
        displays the next one each tick. For a slower animation, you may want to 
        consider using a timer of some sort so it updates slower.'''
        if self.count_delay > 0:
            self.count_delay -= 1
        else:
            self.index += 1
            self.count_delay = 2
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

def main():
    pygame.init()
    screen = pygame.display.set_mode((250, 250))

    my_sprite = TestSprite()
    my_group = pygame.sprite.Group(my_sprite)
    clock = pygame.time.Clock()
    while True:
        clock.tick(25)
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

        # Calling the 'my_group.update' function calls the 'update' function of all 
        # its member sprites. Calling the 'my_group.draw' function uses the 'image'
        # and 'rect' attributes of its member sprites to draw the sprite.
        #my_group.draw(screen)
        #my_group.update()
        screen.blit(my_group, (0, 0))
        pygame.display.flip()

if __name__ == '__main__':
    main()