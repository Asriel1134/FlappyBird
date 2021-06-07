import pygame
from .. import setup, tools, sound


class Brick(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.rect = self.image.get_rect()
        self.marked = False

    def load_image(self):
        self.image = tools.get_image(setup.CHONG['brick_0'], 0, 0, 25, 50)

    def update(self, level):
        self.rect.x -= 2
        if not self.marked:
            if self.rect.x + self.image.get_size()[0 ] < level.bird.rect.x:
                self.marked = True
                sound.playSound01.play()



