import pygame
from .. import setup, tools, sound


class Pillar1(pygame.sprite.Sprite):
    def __init__(self, direction=0):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        if direction == 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.marked = False

    def load_image(self):
        self.image_down = tools.get_image(setup.CHONG['zhu_down_1'], 0, 0, 26, 309)
        self.image_up = tools.get_image(setup.CHONG['zhu_up_1'], 0, 0, 26, 309)

    def update(self, level):
        self.rect.x -= 2
        if not self.marked:
            if self.rect.x + self.image.get_size()[0] < level.bird.rect.x:
                self.marked = True
                level.mark += 0.5
                sound.playSound01.play()



