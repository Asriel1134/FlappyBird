import pygame
from ..components import bird, pillar, brick, pillar1
from .. import setup, tools, sound
from .. import constants as C


class Level:
    def __init__(self):
        self.start()

    def start(self):
        self.setup_background()
        self.setup_bird()
        self.setup_pillar()
        self.setup_pillar1()
        self.setup_brick()
        self.mark = 0
        self.setup_settle()
        self.finished = False
        self.finishing = False
        self.starting = True
        self.entering = True
        self.save = False
        self.hit_played = False
        self.die_played = False
        self.over_played = False
        self.scoreboard_played = False
        self.next = 'menu'
        self.finish_timer = 0
        self.start_timer = 0
        self.entry_timer = 0
        self.settle_timer = 0
        self.pillar_timer = 0
        self.brick_timer = 0
        self.mark_timer = 0
        self.sound_timer = 0
        self.random_timer = 0
        self.frame_index = 0
        self.random_timer = 0
        self.invincible_timer = 0
        self.rand = 0
        self.ground_x1 = 0
        self.ground_x2 = self.ground_x1 + self.ground_size[0]
        self.ground_vel = 2
        self.button_start_y = self.button_rank_y = self.game_ground_h * 0.6643
        self.dis_invincible = True

    def create_random(self):
        self.rand = setup.random

    def random_select(self):
        self.rand = setup.random
        if not self.starting and not self.bird.dead:
            if self.random_timer == 0 and self.rand < 2 / 3:
                self.random_timer = pygame.time.get_ticks()
                self.rand = setup.random
                self.create_pillar()
            elif pygame.time.get_ticks() - self.random_timer > 1700 and self.rand < 2 / 3:
                self.random_timer = pygame.time.get_ticks()
                self.rand = setup.random
                self.create_pillar()
            self.pillar_group.update(self)
            self.pillar_group.draw(self.game_ground)
            if self.random_timer == 0 and 2 / 3 < self.rand < 4 / 3:
                self.random_timer = pygame.time.get_ticks()
                self.rand = setup.random
                self.create_pillar1()
            elif pygame.time.get_ticks() - self.random_timer > 1700 and 2 / 3 < self.rand < 4 / 3:
                self.random_timer = pygame.time.get_ticks()
                self.rand = setup.random
                self.create_pillar1()
            self.pillar1_group.update(self)
            self.pillar1_group.draw(self.game_ground)
            if self.random_timer == 0 and self.rand > 4 / 3 and self.mark > 15:
                self.random_timer = pygame.time.get_ticks()
                self.rand = setup.random
                self.create_brick()
            elif pygame.time.get_ticks() - self.random_timer > 1700 and self.rand > 4 / 3 and self.mark > 1:
                self.random_timer = pygame.time.get_ticks()
                self.rand = setup.random
                self.create_brick()
            self.brick_group.update(self)
        self.pillar_group.draw(self.game_ground)
        self.pillar1_group.draw(self.game_ground)
        self.brick_group.draw(self.game_ground)

    def setup_background(self):
        if setup.random < 1:
            self.background = tools.get_image(setup.CHONG['game_bg_1'], 0, 0, 288, 512)
        else:
            self.background = tools.get_image(setup.CHONG['game_bg_3'], 0, 0, 288, 512)

        self.get_ready = tools.get_image(setup.GRAPHICS['atlas'], 584, 116, 196, 62)
        self.get_ready_size = self.get_ready.get_size()

        self.guide = tools.get_image(setup.GRAPHICS['atlas'], 586, 182, 110, 98)
        self.guide_size = self.guide.get_size()

        self.ground = tools.get_image(setup.CHONG['ground'], 0, 0, 336, 112, (66, 66, 66))
        self.ground_size = self.ground.get_size()

        self.viewport = setup.SCREEN.get_rect()
        self.game_ground = pygame.Surface((288, 512))
        self.game_ground_w, self.game_ground_h = self.game_ground.get_size()

    def setup_bird(self):
        self.bird = bird.Bird()
        self.bird.x = self.game_ground_w * 1.25 / 5
        self.bird.y = self.game_ground_h * 1.9 / 4

    def setup_pillar(self):
        self.pillar_group = pygame.sprite.Group()

    def setup_pillar1(self):
        self.pillar1_group = pygame.sprite.Group()

    def setup_brick(self):
        self.brick_group = pygame.sprite.Group()


    def create_pillar(self):
        pillar_up = pillar.Pillar(0)
        pillar_down = pillar.Pillar(1)
        pillar_down.rect.bottom = (self.game_ground_h - self.ground_size[1]) * (setup.random / 2) * 0.4 + self.game_ground_h * 0.15
        pillar_up.rect.top = pillar_down.rect.bottom + self.game_ground_h * 0.24
        pillar_up.rect.x = pillar_down.rect.x = self.game_ground_w + pillar_down.image.get_size()[0]
        self.pillar_group.add(pillar_down)
        self.pillar_group.add(pillar_up)

    def create_pillar1(self):
        pillar1_up = pillar1.Pillar1(0)
        pillar1_down = pillar1.Pillar1(1)
        pillar1_down.rect.bottom = (self.game_ground_h - self.ground_size[1]) * (setup.random / 2) * 0.4 + self.game_ground_h * 0.15
        pillar1_up.rect.top = pillar1_down.rect.bottom + self.game_ground_h * 0.19
        pillar1_up.rect.x = pillar1_down.rect.x = self.game_ground_w + pillar1_down.image.get_size()[0]
        self.pillar_group.add(pillar1_down)
        self.pillar_group.add(pillar1_up)

    def create_brick(self):
        brick_down = brick.Brick()
        brick_down.rect.bottom = (self.game_ground_h - self.ground_size[1]) * (
                setup.random / 2) * 0.4 + self.game_ground_h * 0.15
        brick_down.rect.x = brick_down.rect.x = self.game_ground_w + brick_down.image.get_size()[0]
        self.brick_group.add(brick_down)


    def check_collisions(self):
        col2 = pygame.sprite.spritecollideany(self.bird, self.brick_group)
        col = pygame.sprite.spritecollideany(self.bird, self.pillar_group) or \
              pygame.sprite.spritecollideany(self.bird, self.pillar1_group)

        if pygame.time.get_ticks() - self.invincible_timer > 3000:
            self.invincible_timer = 0
            self.dis_invincible = True

        if col2:
            self.invincible_timer = 0
            self.invincible_timer = pygame.time.get_ticks()
            self.dis_invincible = False
            col2.kill()
        elif col:
            if self.dis_invincible == False:
                pass
            else:
                self.bird.dead = True
                if not self.hit_played:
                    self.sound_timer = pygame.time.get_ticks()
                    sound.hit.play()
                    self.hit_played = True
                if pygame.time.get_ticks() - self.sound_timer > 100 and not self.die_played and self.sound_timer != 0:
                    sound.die.play()
                    self.die_played = True

        if pygame.time.get_ticks() - self.invincible_timer > 3000:
            self.invincible_timer = 0
            self.dis_invincible = True









    def update_mark(self):
        self.mark = int(self.mark)
        self.mark_image = tools.creat_labels(str(self.mark), setup.FONT_big)
        self.mark_size = self.mark_image.get_size()

    def update(self, surface, keys, mouse):
        if mouse[4]:
            self.mark += 1
        if mouse[3]:
            pygame.time.Clock().tick(45)

        self.game_ground.blit(self.background, self.viewport)

        self.check_collisions()

        if self.starting:
            if mouse[0]:
                self.starting = False
            self.game_ground.blit(self.get_ready,
                                  ((self.game_ground_w - self.get_ready_size[0]) / 2, (self.game_ground_h * 1.2 / 4)))
            self.game_ground.blit(self.guide,
                                  ((self.game_ground_w - self.guide_size[0]) / 2, (self.game_ground_h * 1.75 / 4)))
        else:
            if self.start_timer == 0:
                self.start_timer = pygame.time.get_ticks()
                self.game_ground.blit(self.get_ready, (
                    (self.game_ground_w - self.get_ready_size[0]) / 2, (self.game_ground_h * 1.2 / 4)))
                self.game_ground.blit(self.guide,
                                      ((self.game_ground_w - self.guide_size[0]) / 2, (self.game_ground_h * 1.75 / 4)))
            else:
                if pygame.time.get_ticks() - self.start_timer < 510:
                    self.get_ready.set_alpha(255 - int((pygame.time.get_ticks() - self.start_timer) / 2))
                    self.guide.set_alpha(255 - int((pygame.time.get_ticks() - self.start_timer) / 2))
                    self.game_ground.blit(self.get_ready, (
                        (self.game_ground_w - self.get_ready_size[0]) / 2, (self.game_ground_h * 1.2 / 4)))
                    self.game_ground.blit(self.guide, (
                        (self.game_ground_w - self.guide_size[0]) / 2, (self.game_ground_h * 1.75 / 4)))

        self.random_select()

        if not self.bird.dead:
            self.update_ground()
        self.game_ground.blit(self.ground, (self.ground_x1, self.game_ground_h - self.ground_size[1]))
        self.game_ground.blit(self.ground, (self.ground_x2, self.game_ground_h - self.ground_size[1]))

        self.update_bird(mouse)

        self.update_mark()
        if not self.bird.over:
            self.game_ground.blit(self.mark_image,
                                  ((self.game_ground_w - self.mark_size[0]) / 2, (self.game_ground_h * 0.64 / 4)))

        if self.bird.over:
            self.settle(mouse)

        if self.entering:
            self.level_entry(self.game_ground)
        self.finish(self.game_ground)

        if not self.dis_invincible:
            if pygame.time.get_ticks() - self.invincible_timer < 3000:
                gold = pygame.Surface((self.game_ground_w, self.game_ground_h))
                gold = gold.convert_alpha()
                gold.fill((255, 255, 0, 150 - int((pygame.time.get_ticks() - self.invincible_timer) / 20)))
                self.game_ground.blit(gold, (0, 0))

        surface.blit(tools.change_multi(self.game_ground), (0, 0))


    def update_bird(self, mouse):
        if mouse[0]:
            if self.bird.state is 'float':
                self.bird.state = 'fly'
        self.bird.update(mouse, self)
        self.game_ground.blit(self.bird.image, (self.bird.x, self.bird.y))

    def update_ground(self):
        self.ground_x1 -= self.ground_vel
        self.ground_x2 -= self.ground_vel
        if self.ground_x1 < -self.ground_size[0] - self.ground_vel:
            self.ground_x1 = self.ground_x2 + self.ground_size[0]
        if self.ground_x2 < -self.ground_size[0] - self.ground_vel:
            self.ground_x2 = self.ground_x1 + self.ground_size[0]

    def finish(self, surface):
        if self.finishing:
            if self.finish_timer == 0:
                self.finish_timer = pygame.time.get_ticks()
            else:
                if pygame.time.get_ticks() - self.finish_timer < 510:
                    black = pygame.Surface((self.game_ground_w, self.game_ground_h))
                    black = black.convert_alpha()
                    black.fill((0, 0, 0, int((pygame.time.get_ticks() - self.finish_timer) / 2)))
                    surface.blit(black, (0, 0))
                else:
                    self.game_ground.fill((0, 0, 0, 255))
                    self.finished = True

    def setup_settle(self):
        self.Scoreboard = pygame.Surface((234, 126))
        self.Scoreboard = self.Scoreboard.convert_alpha()
        self.Scoreboard.fill((0, 0, 0, 0))
        self.sb_bg = tools.get_image(setup.GRAPHICS['atlas'], 2, 516, 234, 126)
        self.copper = tools.get_image(setup.GRAPHICS['atlas'], 224, 954, 44, 44)
        self.silver = tools.get_image(setup.GRAPHICS['atlas'], 224, 906, 44, 44)
        self.gold = tools.get_image(setup.GRAPHICS['atlas'], 242, 564, 44, 44)
        self.platinum = tools.get_image(setup.GRAPHICS['atlas'], 242, 516, 44, 44)
        self.game_over = tools.get_image(setup.GRAPHICS['atlas'], 784, 116, 204, 54)
        self.button_start = tools.get_image(setup.GRAPHICS['atlas'], 702, 234, 116, 70)
        self.button_rank = tools.get_image(setup.CHONG['rank'], 0, 0, 116, 60)

    def settle(self, mouse):
        if not self.save:
            tools.update_rank(setup.rank_list1, self.mark, "./resources/rank1.txt")
            self.save = True
        if 9 < self.mark < 20:
            self.medal = self.copper
        elif self.mark < 30:
            self.medal = self.silver
        elif self.mark < 50:
            self.medal = self.gold
        else:
            self.medal = self.platinum
        self.Scoreboard.blit(self.sb_bg, (0, 0))
        if self.mark > 9:
            self.Scoreboard.blit(self.medal, (30, 44))

        if self.mark_timer == 0:
            self.mark_timer = pygame.time.get_ticks()
            self.mark_small_image = tools.creat_labels(str(0), setup.FONT_big)
        if pygame.time.get_ticks() - self.mark_timer < 1150:
            self.mark_small_image = tools.creat_labels(str(0), setup.FONT_big)
        else:
            if int((pygame.time.get_ticks() - self.mark_timer - 1150) / 30) < self.mark:
                self.mark_small_image = tools.creat_labels(
                    str(int((pygame.time.get_ticks() - self.mark_timer - 1150) / 30)), setup.FONT_big)
            else:
                self.mark_small_image = tools.creat_labels(
                    str(self.mark), setup.FONT_big)
        self.mark_small_image = pygame.transform.scale(self.mark_small_image, (
            int(0.5 * self.mark_small_image.get_size()[0]), int(0.5 * self.mark_small_image.get_size()[1])))
        self.Scoreboard.blit(self.mark_small_image, (210 - self.mark_small_image.get_size()[0], 38))

        self.best_small_image = tools.creat_labels(str(setup.rank_list1[0]), setup.FONT_big)
        self.best_small_image = pygame.transform.scale(self.best_small_image, (
            int(0.5 * self.best_small_image.get_size()[0]), int(0.5 * self.best_small_image.get_size()[1])))
        self.Scoreboard.blit(self.best_small_image, (210 - self.best_small_image.get_size()[0], 80))

        if self.settle_timer == 0:
            self.settle_timer = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.settle_timer < 255:  # 死后屏幕闪白
            white = pygame.Surface((self.game_ground_w, self.game_ground_h))
            white = white.convert_alpha()
            white.fill((255, 255, 255, 255 - int((pygame.time.get_ticks() - self.settle_timer))))
            self.game_ground.blit(white, (0, 0))
        elif pygame.time.get_ticks() - self.settle_timer < 600:  # game_over
            self.game_ground.blit(self.game_over, (
                (self.game_ground_w - self.game_over.get_size()[0]) / 2, (self.game_ground_h * 1 / 4)))
            if not self.over_played:
                sound.swooshing.play()
                self.over_played = True

        elif pygame.time.get_ticks() - self.settle_timer < 945:  # 计分板上升
            self.game_ground.blit(self.game_over, (
                (self.game_ground_w - self.game_over.get_size()[0]) / 2, (self.game_ground_h * 1 / 4)))
            self.game_ground.blit(self.Scoreboard, ((self.game_ground_w - self.Scoreboard.get_size()[0]) / 2,
                                                    self.game_ground_h - int(self.game_ground_h * 0.62 * (
                                                            pygame.time.get_ticks() - self.settle_timer - 600) / 345)))
            if not self.scoreboard_played:
                sound.swooshing.play()
                self.scoreboard_played = True

        elif pygame.time.get_ticks() - self.settle_timer < 1200:  # 计分板悬停
            self.game_ground.blit(self.game_over, (
                (self.game_ground_w - self.game_over.get_size()[0]) / 2, (self.game_ground_h * 1 / 4)))
            self.game_ground.blit(self.Scoreboard,
                                  ((self.game_ground_w - self.Scoreboard.get_size()[0]) / 2, self.game_ground_h * 0.38))

        else:  # 按钮
            self.game_ground.blit(self.game_over, (
                (self.game_ground_w - self.game_over.get_size()[0]) / 2, (self.game_ground_h * 1 / 4)))
            self.game_ground.blit(self.Scoreboard,
                                  ((self.game_ground_w - self.Scoreboard.get_size()[0]) / 2, self.game_ground_h * 0.38))
            if int((pygame.time.get_ticks() - self.mark_timer - 1150) / 30) > self.mark:
                self.game_ground.blit(self.button_start, (self.game_ground_w / 18, self.button_start_y))
                self.game_ground.blit(self.button_rank, (
                    self.game_ground_w * 17 / 18 - self.button_rank.get_size()[0], self.button_rank_y))
                if mouse[0]:
                    if C.SCREEN_W / 18 < pygame.mouse.get_pos()[0] < C.SCREEN_W / 18 + self.button_start.get_size()[
                        0] * C.MULTI and self.button_start_y * C.MULTI < pygame.mouse.get_pos()[
                        1] < self.button_start_y * C.MULTI + self.button_start.get_size()[1] * C.MULTI:
                        self.button_start_y = self.game_ground_h * 0.668
                        if not self.finishing:
                            self.finishing = True
                            self.next = 'level'
                    if C.SCREEN_W * 17 / 18 - self.button_rank.get_size()[0] * C.MULTI < pygame.mouse.get_pos()[
                        0] < C.SCREEN_W * 17 / 18 + self.button_start.get_size()[0] and self.button_rank_y * C.MULTI < \
                            pygame.mouse.get_pos()[1] < self.button_rank_y * C.MULTI + self.button_start.get_size()[
                        1] * C.MULTI:
                        self.button_rank_y = self.game_ground_h * 0.668
                        if not self.finishing:
                            self.finishing = True
                            self.next = 'rank'
                elif not mouse[0]:
                    self.button_start_y = self.button_rank_y = self.game_ground_h * 0.6643

    def level_entry(self, surface):
        if self.entry_timer == 0:
            self.game_ground.fill((0, 0, 0, 255))
            self.entry_timer = pygame.time.get_ticks()
            sound.swooshing.play()
        else:
            if pygame.time.get_ticks() - self.entry_timer < 510:
                black = pygame.Surface((self.game_ground_w, self.game_ground_h))
                black = black.convert_alpha()
                black.fill((0, 0, 0, 255 - int((pygame.time.get_ticks() - self.entry_timer) / 2)))
                self.game_ground.blit(black, (0, 0))
