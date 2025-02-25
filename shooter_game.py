from pygame import  *
from random import *
from time import time as timer
win_widht = 700
win_height = 500
fps = 60
lost = 0
score = 0
life = 3
rel_time = False
mw = display.set_mode((win_widht,win_height))
display.set_caption('шутер')
background = transform.scale(image.load('galaxy.jpg'),(win_widht,win_height))
finish = False
run = True
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
font.init()
fire_sound = mixer.Sound('fire.ogg')
font1 = font.SysFont('Arial',36)
lose = font1.render('YOU LOSE!',True,(255,0,0))
win = font1.render('You WIN!',True,(255,255,0))
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed,):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        mw.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80,620)
            self.rect.y = 0
            lost += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
asteroids = sprite.Group()    
player = Player('rocket.png',350,400,80,100,10)
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(2):
    asteroid = Enemy('asteroid.png',randint(80,620),-50,80,50,randint(2,7))
    asteroids.add(asteroid)
for i in range(5):
    monster = Enemy('ufo.png',randint(80,620),-50,80,50,randint(1,6))
    monsters.add(monster)
num_fire = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    player.fire()
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    start = timer()
    if not finish:
        mw.blit(background,(0,0))
        text = font1.render('Счет: '+str(score),True,(255,255,255))
        mw.blit(text,(10,20))
        text_lose = font1.render('Пропущено:'+str(lost),1,(255,255,255))
        mw.blit(text_lose,(10,50))
        if life == 3:
            text_life = font1.render(str(life),1,(0,255,0))
        elif life == 2:
            text_life = font1.render(str(life),1,(255,255,0))
        else:
            text_life = font1.render(str(life),1,(255,0,0))
        mw.blit(text_life,(620,10))
        player.update()
        player.reset()
        monsters.draw(mw)
        monsters.update()
        asteroids.update()
        asteroids.draw(mw)
        bullets.update()
        bullets.draw(mw)  
        if rel_time == True:
            cur_time = timer()
            if cur_time - start < 3:
                reload = font1.render('Wair reload!...',1,(150,0,0))
                mw.blit(reload,(260,460))
            else:
                num_fire = 0
                rel_time = False  
        colides = sprite.groupcollide(monsters,bullets,True,True)
        for i in colides:
            score +=1
            monster = Enemy('ufo.png',randint(80,620),-50,80,50,randint(1,6))
            monsters.add(monster)
        if sprite.spritecollide(player,monsters,False) or sprite.spritecollide(player,asteroids,False):
            sprite.spritecollide(player,monsters,True)
            sprite.spritecollide(player,asteroids,True)
            life -= 1
        if lost >= 3 or life == 0:
            finish = True
            mw.blit(lose,(200,200))
        if score >= 10 :
            finish = True
            mw.blit(win,(200,200))
            

        display.update()
    time.delay(fps)
    
    
