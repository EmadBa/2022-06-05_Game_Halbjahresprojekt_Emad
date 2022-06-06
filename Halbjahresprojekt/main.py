import pygame, sys, random
from pygame.constants import (QUIT, KEYDOWN, KEYUP, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE, K_ESCAPE, K_RETURN, K_c)
import os



class Settings(object):
    window = {'width':800, 'height':400}
    fps = 60
    title = "Street Runner"
    path = {}
    path['file'] = os.path.dirname(os.path.abspath(__file__))
    path['image'] = os.path.join(path['file'], "images")
    path['sound'] = os.path.join(path['file'], "Sounds")
    path['highscore']= os.path.join(path['file'], "score.txt")

    score = 0
    lives= 3

    def dim():
        return (Settings.window['width'], Settings.window['height'])

    @staticmethod
    def filepath(name):
        return os.path.join(Settings.path['file'], name)

    @staticmethod
    def imagepath(name):
        return os.path.join(Settings.path['image'], name)
    @staticmethod
    def soundpath(name):
        return os.path.join(Settings.path['sound'], name)


class Timer(object):
    def __init__(self, duration, with_start = True):
        self.duration = duration
        if with_start:
            self.next = pygame.time.get_ticks()
        else:
            self.next = pygame.time.get_ticks() + self.duration

    def is_next_stop_reached(self):
        if pygame.time.get_ticks() > self.next:
            self.next = pygame.time.get_ticks() + self.duration
            return True
        return False

    def change_duration(self, delta=10):
        self.duration += delta
        if self.duration < 0:
            self.duration = 0

class Background(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(Settings.imagepath(filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.dim()))
        self.width=self.image.get_width()
        self.x = 0
        self.y = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x,self.y))
        screen.blit(self.image, (self.x+self.width,self.y))
    def update(self,speed):
        self.x -= speed
        Settings.score +=1
        if abs(self.x)>self.width:
            self.x = 0
        

class Runner(pygame.sprite.Sprite):
    def __init__(self, time):
        super().__init__()
        self.images = {'up':[], 'down':[], 'left':[], 'right':[],'stop':[]}
        for i in range(0,6):
            picture = pygame.image.load(Settings.imagepath(f"move{i}.png")).convert()
            picture.set_colorkey((0, 0, 0))

            self.images['right'].append(picture)
            self.images['left'].append(picture)
            self.images['stop'].append(picture)

        self.jump= 0 
        self.direction = 'stop'
        self.imageindex = 0
        self.image = self.images[self.direction][self.imageindex]
        self.rect = self.image.get_rect()

        self.rect.center = (self.rect.width//2, Settings.window['height']-self.rect.height // 2 )
        self.animation_time = Timer(time)

    def update(self):
        self.update_imageindex()
        if self.direction == 'right':
            self.start()
            self.animation_time = Timer(10)
            if self.rect.right < Settings.window['width'] - self.rect.width:
                self.rect.right += self.speed
            else:
                self.stop()
        elif self.direction == 'left':
            self.start()
            self.animation_time = Timer(10)
            if self.rect.left < self.rect.width//2:
                self.stop()
            else:
                self.rect.right -= self.speed


        if self.jump > 0 or self.rect.y < 330 :
            self.rect.y -= self.jump
            self.jump -= 1
        if self.rect.y > 330 :
            self.rect.y = 330 
        if self.rect.y == 330 and self.jump < 0 :
            self.jump = 0
            
    def turn(self, direction):
        self.direction = direction

    def stop(self):
        self.speed = 0       
        self.direction='stop'

    def jumping(self):
        self.jump= 20

    def start(self):
        self.speed = 5

    def update_imageindex(self):
        if self.animation_time.is_next_stop_reached():
            self.imageindex += 1
            if self.imageindex >= len(self.images[self.direction]):
                self.imageindex = 0
            else:
                self.image = self.images[self.direction][self.imageindex]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Bird(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.images = []
        for i in range(0,5):
            picture = pygame.image.load(Settings.imagepath(f"bird{i}.png")).convert()
            picture.set_colorkey((0, 0, 0))
            picture = pygame.transform.flip(picture, True, False)
            picture = pygame.transform.scale(picture, (75,75))
            self.images.append(picture)

        self.imageindex = 0
        self.image = self.images[self.imageindex]

        self.rect = self.image.get_rect()
        self.animation_time = Timer(100)
        self.rect.left = Settings.window['width'] 
        self.rect.bottom= Settings.window['height'] - 70

    def update(self,speed):
        self.update_imageindex()
        self.rect.left -= speed

        if self.rect.left < -50:
            self.kill()

    def update_imageindex(self):
        if self.animation_time.is_next_stop_reached():
            self.imageindex += 1
            if self.imageindex >= len(self.images):
                self.imageindex = 0
            else:
                self.image = self.images[self.imageindex]

class Hindernisse(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.images = [pygame.image.load(Settings.imagepath("fo1.png")).convert_alpha(), pygame.image.load(Settings.imagepath(f"fo2.png")).convert_alpha()]
        self.image = random.choice(self.images)
        self.image = pygame.transform.scale(self.image, (60,50))
        self.rect = self.image.get_rect()

        self.rect.left = Settings.window['width'] + 200
        self.rect.bottom= Settings.window['height']
        
    def update(self,speed):
        self.rect.left -= speed

        if self.rect.left < -100:
            self.kill()

class Car(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load(Settings.imagepath("car.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (155,60))
        self.rect = self.image.get_rect()

        self.rect.left = Settings.window['width'] + 500
        self.rect.bottom= Settings.window['height']
        
    def update(self,speed):
        self.rect.left -= speed

        if self.rect.left < -400:
            self.kill()


class Game(object):
    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.dim())
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()

        # Sound
        self.bg_music =pygame.mixer.music.load(Settings.soundpath("music.mp3"))
        pygame.mixer.music.play(-1)

        self.jump_sound = pygame.mixer.Sound(Settings.soundpath("jump.ogg"))
        self.hits_sound = pygame.mixer.Sound(Settings.soundpath("hits.wav"))
        self.gameover_sound = pygame.mixer.Sound(Settings.soundpath("gameover.ogg"))

        # Für Schwerigkeit des Spiels
        self.bgspeed= 1
        self.runtimer = 100
        # Font
        self.font = pygame.font.Font(pygame.font.get_default_font(), 52)
        self.font_score= pygame.font.Font("freesansbold.ttf",16)

        self.runner = Runner(self.runtimer)
        self.background = Background("street.jpg")

        self.bird= pygame.sprite.Group()
        self.bird.add(Bird())

        self.hindernisse= pygame.sprite.Group()
        self.hindernisse.add(Hindernisse())

        self.car= pygame.sprite.Group()

        self.running = False
        self.pause = False
        self.game_over = False
        self.continue_game = False
        another_live = False

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                elif event.key == K_RIGHT:
                    self.runner.turn('right')
                elif event.key == K_LEFT:
                    self.runner.turn('left')
                elif event.key == K_SPACE and self.runner.jump == 0 and self.pause == False and self.game_over == False and self.continue_game == False:
                    pygame.mixer.Sound.play(self.jump_sound)
                    self.runner.jumping()

                if self.continue_game == False and self.game_over == False:
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
                if self.game_over == True or self.continue_game == True:
                    if event.key == pygame.K_RETURN:
                        self.restart()

            elif event.type == KEYUP:
                if event.key == K_RIGHT:
                    self.runner.turn('stop')
                    self.runner.animation_time = Timer(self.runtimer)
                elif event.key == K_LEFT:
                    self.runner.turn('stop')
                    self.runner.animation_time = Timer(self.runtimer)

    def draw(self) -> None:
        self.background.draw(self.screen)
        self.runner.draw(self.screen)
        self.bird.draw(self.screen)
        self.hindernisse.draw(self.screen)
        self.car.draw(self.screen)
        if self.pause:
            self.pause_window()
        if self.game_over:
            self.gameover_window()
        if self.continue_game:
            self.continue_window()
        self.score_text = self.font_score.render(f"Score: {Settings.score}",True, (0, 0, 0))
        self.screen.blit(self.score_text,(0,0))
        self.lives_test = self.font_score.render(f"Lives: {Settings.lives}",True, (0, 0, 0))
        self.screen.blit(self.lives_test,(Settings.window['width']-60,0))
        pygame.display.flip()

    def update(self) -> None:
        self.background.update(self.bgspeed)
        self.runner.update()
        self.bird.update(self.bgspeed)
        self.hindernisse.update(self.bgspeed)
        self.car.update(self.bgspeed)
        if len(self.bird) < 1:
            self.bird.add(Bird())
        if len(self.hindernisse)<1:
            self.hindernisse.add(Hindernisse())
        if Settings.score > 3000:       # ab Score 3000 neue Hindernisse(Auto)
            if len(self.car) < 1:
                self.car.add(Car())

#   Schwerigkeit des Spiels
#   Hinweis: Das Spiel müsste nicht sofort so schwere sein aber
#   damit man merken könnte,  wie es schwer aus sieht
        if Settings.score > 3000:
            self.bgspeed = 12
            self.runtimer= 10

        elif Settings.score > 2500:
            self.bgspeed = 10
            self.runtimer= 20

        elif Settings.score > 2000:
            self.bgspeed = 8
            self.runtimer= 40

        elif Settings.score > 1000:
            self.bgspeed = 6
            self.runtimer= 50

        elif Settings.score > 500:
            self.bgspeed = 4
            self.runtimer= 75

        elif Settings.score > 100:  #hier z.B könnte ab 2000
            self.bgspeed = 2
            self.runtimer = 75

        # neue Leben-Möglichkeiten
        if Settings.score == 10000:
            Settings.lives +=1

        if Settings.score == 5000:
            Settings.lives +=1

        if Settings.score == 1000:
            Settings.lives +=1

        #kollision
        self.hits1 = pygame.sprite.spritecollide(self.runner, self.bird, False, pygame.sprite.collide_mask)
        self.hits2 = pygame.sprite.spritecollide(self.runner, self.hindernisse, False, pygame.sprite.collide_mask)
        self.hits3= pygame.sprite.spritecollide(self.runner, self.car, False, pygame.sprite.collide_mask)
        if self.hits1 or self.hits2 or self.hits3 :
            Settings.lives -=1
            if Settings.lives > 0 :
                pygame.mixer.Sound.play(self.hits_sound)
                self.continue_game = True
            else:
                pygame.mixer.Sound.play(self.gameover_sound)
                self.gameover()

    # Continue Fesnter
    def continue_window(self):
        loss = pygame.Surface(self.screen.get_size())
        loss.set_alpha(200)
        self.screen.blit(loss, (0, 0))
        text_loss = self.font.render("YOU LOST !!!", True, (255, 191, 0))
        text_loss_rect=text_loss.get_rect()
        text_loss_rect.center = (Settings.window['width'] // 2, Settings.window['height'] // 2 )
        self.screen.blit(text_loss, text_loss_rect)

        score = pygame.Surface(self.screen.get_size())
        score.set_alpha(0)
        score.fill((0, 0, 0))
        self.screen.blit(score, (0, 0))
        text_score = self.font.render("Your Score: {0}".format(Settings.score), True, (255, 127, 80))
        text_score_rect=text_score.get_rect()
        text_score_rect.center = (Settings.window['width'] // 2, Settings.window['height'] // 2 - 70)
        self.screen.blit(text_score, text_score_rect)

        highscore = pygame.Surface(self.screen.get_size())
        highscore.set_alpha(0)
        highscore.fill((0, 0, 0))
        self.screen.blit(highscore, (0, 0))
        text_highscore = self.font.render("Highscore: {0}".format(self.get_highscore()), True, (222, 49, 99))
        text_highscore_rect=text_highscore.get_rect()
        text_highscore_rect.center = (Settings.window['width'] // 2, Settings.window['height'] // 2 - 140)
        self.screen.blit(text_highscore, text_highscore_rect)

        lives = pygame.Surface(self.screen.get_size())
        lives.set_alpha(0)
        lives.fill((0, 0, 0))
        self.screen.blit(lives, (0, 0))
        text_lives = self.font.render("Lives: {0}".format(Settings.lives), True, (223, 255, 0))
        text_lives_rect=text_lives.get_rect()
        text_lives_rect.center = (Settings.window['width'] // 2, Settings.window['height'] // 2 +65)
        self.screen.blit(text_lives, text_lives_rect)

        restart = pygame.Surface(self.screen.get_size())
        restart.set_alpha(0)
        restart.fill((0, 0, 0))
        self.screen.blit(restart, (0, 0))
        text_restart = self.font_score.render("Press \"enter\" to continue ...", True, (218, 247, 166 ))
        text_restart_rect=text_restart.get_rect()
        text_restart_rect.center = (Settings.window['width'] // 2, Settings.window['height'] // 2 + 110)
        self.screen.blit(text_restart, text_restart_rect)

    # Pause-Fenster
    def pause_window(self):
        pause = pygame.Surface(self.screen.get_size())
        pause.set_alpha(200)
        self.screen.blit(pause, (0, 0))
        text_pause = self.font.render("PAUSE", True, (255, 0, 0))
        text_pause_rect=text_pause.get_rect()
        text_pause_rect.center = (Settings.window['width'] // 2, Settings.window['height'] // 2)
        self.screen.blit(text_pause, text_pause_rect)

    # Gameover-Fenster
    def gameover_window(self):
        gameover = pygame.Surface(self.screen.get_size())
        gameover.set_alpha(200)
        self.screen.blit(gameover, (0, 0))
        text_gameover = self.font.render("GAME OVER", True, (255, 0, 0))
        text_gameover_rect=text_gameover.get_rect()
        text_gameover_rect.center = (Settings.window['width'] // 2, Settings.window['height'] // 2 + 30)
        self.screen.blit(text_gameover, text_gameover_rect)

        score = pygame.Surface(self.screen.get_size())
        score.set_alpha(0)
        score.fill((0, 0, 0))
        self.screen.blit(score, (0, 0))
        text_score = self.font.render("Your Score: {0}".format(Settings.score), True, (255, 127, 80))
        text_score_rect=text_score.get_rect()
        text_score_rect.center = (Settings.window['width'] // 2, Settings.window['height'] // 2 - 30)
        self.screen.blit(text_score, text_score_rect)

        highscore = pygame.Surface(self.screen.get_size())
        highscore.set_alpha(0)
        highscore.fill((0, 0, 0))
        self.screen.blit(highscore, (0, 0))
        text_highscore = self.font.render("Highscore: {0}".format(self.get_highscore()), True, (222, 49, 99))
        text_highscore_rect=text_highscore.get_rect()
        text_highscore_rect.center = (Settings.window['width'] // 2, Settings.window['height'] // 2 - 90)
        self.screen.blit(text_highscore, text_highscore_rect)

        restart = pygame.Surface(self.screen.get_size())
        restart.set_alpha(0)
        restart.fill((0, 0, 0))
        self.screen.blit(restart, (0, 0))
        text_restart = self.font_score.render("Press \"enter\" to restart the game ...", True, (218, 247, 166 ))
        text_restart_rect=text_restart.get_rect()
        text_restart_rect.center = (Settings.window['width'] // 2, Settings.window['height'] // 2 + 110)
        self.screen.blit(text_restart, text_restart_rect)

    def run(self):
        """Starting point of the game.

        Call this method in order to start the game. It contains the main loop.
        """
        self.running = True
        while self.running:
            self.clock.tick(Settings.fps)
            self.watch_for_events()
            self.draw()
            if  self.pause == False and self.game_over == False and self.continue_game == False:
                self.update()

        pygame.quit()


# die höchste gespeicherte Score zu holen, setzen und speichern
    def get_highscore(self):
        with open(Settings.path['highscore']) as txt:
            highscore = txt.read()
        return highscore

    def set_highscore(self,highscore):
        with open(Settings.path['highscore'], 'w') as txt:
            txt.write(str(highscore))

    def save_highscore(self):
        if Settings.score > int(self.get_highscore()):
            self.set_highscore(Settings.score)

    def gameover(self):
        self.save_highscore()
        self.game_over = True

# Zur Widerholung des Spiels
    def restart(self):
        if Settings.lives > 0:
            game = Game()
            game.run()
        else:
            Settings.score= 0
            Settings.lives= 3
            game = Game()
            game.run()

if __name__ == '__main__':
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 30"
    game = Game()
    game.run()
