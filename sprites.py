import pygame as pg
from random import choice, randrange
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(120, 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        self.standing_frames = [self.game.playersheet.get_image(67, 196, 66, 92), self.game.playersheet.get_image(0, 196, 66, 92)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_r = [self.game.playersheet.get_image(0, 0, 72, 97), self.game.playersheet.get_image(73, 0, 72, 97),
                            self.game.playersheet.get_image(146, 0, 72, 97),self.game.playersheet.get_image(0, 98, 72, 97)]

        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.jump_frame = self.game.playersheet.get_image(438, 93, 67, 94)
        self.jump_frame.set_colorkey(BLACK)


    def jump(self):
        self.rect.x +=.5
        hits = pg.sprite.spritecollide(self,self.game.platforms,False)
        self.rect.x -=5
        if hits:
            self.vel.y = -5

    def update(self):
        self.animate()
        self.acc = vec(0, 0.3)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH -3
        if self.pos.x < 0:
            self.pos.x = 3

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # show walk animation
        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.image = game.spritesheet.get_image(504, 720, 70, 70)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Door(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.image = game.spritesheet.get_image(648, 432, 70,70)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class DoorTop(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        #frame.set_colorkey(BLACK)
        self.game = game
        self.image = game.spritesheet.get_image(648, 360 ,70 ,70)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Spritesheet:
    #loads sprite Spritesheet
    def __init__ (self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width,height))
        image.blit(self.spritesheet, (0,0), (x,y,width,height))
        image = pg.transform.scale(image , (width  // 3, height // 3))
        return image

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = randrange(1,4)



    def load_images(self):
        self.standing_frames = [self.game.enemysheet.get_image(528, 147, 51, 73)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_r = [self.game.enemysheet.get_image(371, 386, 51, 73)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))

    def update(self):
        if self.rect.centerx > WIDTH or self.rect.centerx < 0:
            self.vx *=-1
        if self.vx > 0:
            self.image = self.walk_frames_l[0]
        elif self.vx < 0:
            self.image = self.walk_frames_r[0]
        self.rect.x += self.vx
