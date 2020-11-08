import pygame as pg
import random
from settings import *
from sprites import *
from os import path
pg.init()
bg = pg.image.load('bg.png')
ship = pg.image.load('ship.png')
class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()


    def load_data(self):
        self.dir = path.dirname(__file__)
        img = path.join(self.dir, 'IMG')
        self.spritesheet = Spritesheet(path.join(img, SPRITESHEET))
        self.playersheet = Spritesheet(path.join(img, PLAYERSHEET))
        self.enemysheet = Spritesheet(path.join(img, ENEMYSHEET))


    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.mob = Mob(self, 400, HEIGHT - 50)
        self.mob = Mob(self, 400, HEIGHT - 225)
        self.mob = Mob(self, 400, HEIGHT - 400)
        self.mob = Mob(self, 400, HEIGHT - 575)
        self.mob = Mob(self, 400, HEIGHT - 750)
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.door = Door(self, 1260, HEIGHT - 45)
        self.doortop = DoorTop(self, 1260, HEIGHT - 65)
        for plat in PLAT_LIST:
            Platform(self, *plat)



        self.run()





    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        #collision
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            self.player.pos.y = hits[0].rect.top
            self.player.vel.y = 1
        if(pg.sprite.collide_rect(self.player,self.door)):
            self.playing = False;
            g.show_win_screen()
        if (pg.sprite.collide_rect(self.player, self.mob)):
            self.playing = False
            g.show_go_screen()




    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        # Game Loop - draw
        self.screen.blit(bg,(0,0))
        self.screen.blit(ship,(1,1))
        self.all_sprites.draw(self.screen)
        self.screen.blit(ship,(1,1))
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/8)
        self.draw_text("Escape the Ghosts!", 22, WHITE, WIDTH /2, HEIGHT / 4)
        self.draw_text("Press any key to play", 22, WHITE, WIDTH /2, HEIGHT * 3 /4)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        self.screen.fill(RED)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH/2, HEIGHT/8)
        self.draw_text("You suck", 22, WHITE, WIDTH /2, HEIGHT / 4)
        self.draw_text("Press any key to play", 22, WHITE, WIDTH /2, HEIGHT * 3 /4)
        pg.display.flip()
        self.wait_for_key()

    def show_win_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("Congratulations you win!", 22, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Press any key to play again", 15, WHITE, WIDTH / 2, 750)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()


pg.quit()
