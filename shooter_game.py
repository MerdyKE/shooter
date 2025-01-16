from pygame import *
from random import *

WIDTH, HEIGHT = 700, 500

window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Шутер")

class GameSprite(sprite.Sprite):
    def __init__(self, image_name, speed, x, y, x1, y1 ):
        super().__init__()
        self.image = transform.scale(image.load(image_name),(x1, y1))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x1 = x1
        self.y1 = y1

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

players = sprite.Group()

class Player(GameSprite):
    def fire( self ):
        bullet_png = 'bullet.png'
        bullet = Bullet(bullet_png, 5, player.rect.centerx, player.rect.y, 25,40)
        shoot.play()
        bullets.add(bullet)
        

    def update( self ):
        keys = key.get_pressed()
        if keys[ K_a ] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[ K_d ] and self.rect.x < WIDTH - 70:
            self.rect.x += self.speed


lost = 0

score = 0

class Enemy(GameSprite):
    def update( self ):
        self.rect.y += self.speed
        global lost
        if self.rect.y > HEIGHT:
            self.rect.x = randint(80,WIDTH - 80)
            self.rect.y = 0
            lost = lost + 1
        global sprites_lits
        sprites_lits = sprite.spritecollide(
            player, enemys, False 
        )


bullets = sprite.Group()

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
        sprites_list = sprite.groupcollide(
            enemys, bullets, True, True
        )
        global score
        score += len(sprites_list)

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        qwe = sprite.groupcollide(
            astr, bullets, False, True
        )

galaxy = transform.scale(image.load("galaxy.jpg"), (WIDTH, HEIGHT))
player = Player('rocket.png', 5, 330, 390, 70, 100)
players.add(player)

ufo = 'ufo.png'
num_monsters = 10
enemys = sprite.Group()
for i in range( num_monsters):
    enemy = Enemy(ufo, randint(1,3),randint(30,650),50,60,50 )
    enemys.add(enemy)

# asteroid = 'asteroid.png'
# num_astr = 3
# astr = sprite.Group()
# for i in range(num_astr):
#     ast = Enemy(asteroid,1,randint(30,650),50,60,50 )
#     astr.add(ast)


health = 3

game = True
finish = False

font.init()
font1 = font.Font(None, 36)
font = font.Font(None, 72)



mixer.init()
mixer.music.load("space.ogg")
mixer.music.set_volume(0.5)
mixer.music.play()
shoot = mixer.Sound('fire.ogg')


clock = time.Clock()
FPS = 60



while game:
    if finish != True:
        window.blit(galaxy, (0,0))



        players.update()
        players.draw(window)

        enemys.update()
        enemys.draw(window)

        bullets.update()
        bullets.draw(window)

        # astr.update()
        # astr.draw(window)

        text_lose = font1.render('Пропущено:' + str(lost),1,(255,255,255))
        text_score = font1.render('Счёт:' + str(score),1,(255,255,255))
        # text_health = font1.render('Жизней:' + str(health),1,(255,255,255))

        window.blit(text_score,(20,20))
        window.blit(text_lose,(20,50))
        # window.blit(text_health,(20,80))

        # if len(sprites_lits) >= 1:
        #     health - 1

    for e in event.get():

        if e.type == QUIT:
            game = False
        
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()

    if lost >= 5:
        LOSE = font.render('Ты проиграл!',1,(255,0,0))
        window.blit(LOSE,(200,220))
        finish = True

    if score >= num_monsters:
        window.blit(galaxy, (0,0))
        WIN = font.render('Ты выиграл!',1,(0,255,0))
        window.blit(WIN,(200,220))
        finish = True

    display.update()
    clock.tick(FPS)