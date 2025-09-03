#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.2)
fire_sound = mixer.Sound('fire.ogg')
fire_sound.set_volume(0.5)

font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)
font3 = font.Font(None, 50)

win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOST!', True, (180, 0, 0))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    
    def fire(self):
        keys = key.get_pressed()
        if keys[K_SPACE]:
            bullets.add(Bullet('bullet.png', self.rect.x + 30, self.rect.y - 20, 20, 40, -10))

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            global lost
            self.rect.x = randint(0, 680)
            self.rect.y = -40
            lost += 1

class EnemyAsteroin(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


win_width = 700
win_height = 500
clock = time.Clock()
display.set_caption('shooter')
window = display.set_mode((win_width, win_height))
backround = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
bullets = sprite.Group()
bullets.add(Bullet('bullet.png', 350, 500, 20, 40, 3))

lives = 3


ship = Player('rocket.png', 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(0, 620), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1):
    asteroid = EnemyAsteroin('asteroid.png', randint(0, 620), -40, 80, 50, randint(1, 2))
    asteroids.add(asteroid)

finish = False
run = True

score = 0
lost = 0
goal = 25
max_lost = 34
rel_time = False
num_fire = 0
color = (28, 252, 3)

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and not rel_time:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(backround,(0,0))

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        ship.update()
        ship.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)

        if sprite.groupcollide(monsters, bullets, True, False):
            score = score + 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)

        
        if sprite.spritecollide(ship, monsters, True):
            lives -= 1
            monster = Enemy('ufo.png', randint(0, 620), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

            if lives == 2:
                color = (252, 219, 3)
            elif lives == 1:
                color = (196, 2, 2)

        if sprite.spritecollide(ship, asteroids, True):
            lives -= 1
            asteroid = EnemyAsteroin('asteroid.png', randint(0, 620), -40, 80, 50, randint(1, 2))
            asteroids.add(asteroid)

        if lives == 0:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))


        text = font2.render('Счёт: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        cur_lives = font3.render(str(lives), 1, color)
        window.blit(cur_lives, (650, 20))

        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        display.update()
        clock.tick(60)