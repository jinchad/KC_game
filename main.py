import pygame
import random
from load_img import LoadImage

WIDTH = 480
HEIGHT = 600
FPS = 60

"""Define colors as constants"""
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

"""Initialise pygame and create window"""
pygame.init()

"""Enable sound effects in game"""
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

"""Loading in images"""
images = LoadImage()
images.load_images()

"""Arrow dictionary containing x coordinates"""
arrow_dict = {
    images.left_arrow : WIDTH/5,
    images.right_arrow : 4*WIDTH/5,
    images.up_arrow : 2*WIDTH/5,
    images.down_arrow : 3*WIDTH/5
}

"""Set speed of the game"""
clock = pygame.time.Clock()

"""Creating player sprite"""
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(images.player_idle_1, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/4 	
        self.rect.bottom = HEIGHT/4

        self.idle = True
        self.idle_sprite_1 = True

        self.idle_animation_speed = 2000
        self.last_update = pygame.time.get_ticks()

        self.attack_animation_speed = 200
        self.last_attack = pygame.time.get_ticks()

        self.count = 0

    def update(self):
        curr_time = pygame.time.get_ticks()
        
        if self.idle:
            if curr_time - self.last_update > self.idle_animation_speed:
                if self.idle_sprite_1:
                    # setting to idle sprite 2
                    self.image = pygame.transform.scale(images.player_idle_2, (100, 100))
                    self.idle_sprite_1 = False
                else:
                    # setting to idle sprite 1
                    self.image = pygame.transform.scale(images.player_idle_1, (100, 100))
                    self.idle_sprite_1 = True
                self.last_update = curr_time

        else:
            if curr_time - self.last_attack > self.attack_animation_speed:
                self.image = pygame.transform.scale(images.player_attack_1, (100, 100))
            
            if curr_time - self.last_attack > 3000:
                self.idle = True

    def attack(self):
        self.idle = False
        self.image = pygame.transform.scale(images.player_attack_2, (100, 100))
        self.last_attack = pygame.time.get_ticks()

class Arrow(pygame.sprite.Sprite):
    def __init__(self, centerx = WIDTH/4, image = images.up_arrow):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (50, 50))

        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = HEIGHT - 10
        self.speedy = 3

        self.arrow_dir = image
    
    def update(self):
        self.rect.y -= self.speedy
        

class ArrowBW(Arrow):
    def __init__(self, centerx = WIDTH / 4, image = images.up_arrow_bw, hit_image = images.up_arrow_hit, miss_image = images.down_arrow_miss):
        super().__init__(centerx, image)
        self.idle = pygame.transform.scale(image, (50, 50))
        self.hit = pygame.transform.scale(hit_image, (52, 52))
        self.miss = pygame.transform.scale(miss_image, (52, 52))
        self.rect.bottom = HEIGHT/2
        self.speed = 0

        self.arrow_hit = False
        self.last_arrow_hit = pygame.time.get_ticks()

        self.arrow_miss = False
        self.last_arrow_miss = pygame.time.get_ticks()
    
    def update(self):
        curr_time = pygame.time.get_ticks()
        if self.arrow_hit and curr_time - self.last_arrow_hit > 300:
            self.image = self.idle
            self.arrow_hit = False
        
        if self.arrow_miss and curr_time-self.last_arrow_miss > 300:
            self.image = self.idle
            self.arrow_miss= False
    
    def score(self):
        curr_time = pygame.time.get_ticks()
        self.image = self.hit
        self.arrow_hit = True
        self.last_arrow_hit = curr_time

    def fail(self):
        curr_time = pygame.time.get_ticks()
        self.image = self.miss
        self.arrow_miss = True
        self.last_arrow_miss = curr_time

        
class GameMaster:
    def __init__(self):
        self.last_arrow = pygame.time.get_ticks()
        self.arrow_intervals = 500
        self.arrow_choices = [images.up_arrow, images.down_arrow, images.left_arrow, images.right_arrow]
        
        self.start = False

    def choose_next_arrow(self):
        curr_time = pygame.time.get_ticks()
        if curr_time-self.last_arrow > self.arrow_intervals and self.start:
            next_arrow = random.choice(list(arrow_dict.keys()))
            self.last_arrow = curr_time
            return Arrow(image = next_arrow, centerx= arrow_dict[next_arrow])
        else:
            return None

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

left_arrow_sprites = pygame.sprite.Group()
right_arrow_sprites = pygame.sprite.Group()
up_arrow_sprites = pygame.sprite.Group()
down_arrow_sprites = pygame.sprite.Group()

arrow_sprites = pygame.sprite.Group()
arrow_sprites.add(left_arrow_sprites, right_arrow_sprites, up_arrow_sprites, down_arrow_sprites)

game_master = GameMaster()

left_arrow_bw = ArrowBW(centerx = arrow_dict[images.left_arrow], image = images.left_arrow_bw, hit_image=images.left_arrow_hit, miss_image=images.left_arrow_miss)

right_arrow_bw = ArrowBW(centerx = arrow_dict[images.right_arrow], image = images.right_arrow_bw,hit_image=images.right_arrow_hit, miss_image=images.right_arrow_miss)

up_arrow_bw = ArrowBW(centerx = arrow_dict[images.up_arrow], image = images.up_arrow_bw, hit_image=images.up_arrow_hit, miss_image=images.up_arrow_miss)

down_arrow_bw = ArrowBW(centerx = arrow_dict[images.down_arrow], image = images.down_arrow_bw, hit_image=images.down_arrow_hit, miss_image=images.down_arrow_miss)

bw_arrows = [left_arrow_bw, right_arrow_bw, up_arrow_bw, down_arrow_bw]

bw_arrow_sprites = pygame.sprite.Group(bw_arrows)
for bw_arrow in bw_arrows:
    bw_arrow_sprites.add(bw_arrow)

running = True
while running:
    
    """Keep loop running at the right speed"""
    clock.tick(FPS)
    
    collisions = pygame.sprite.groupcollide(arrow_sprites, bw_arrow_sprites, False, False)

    """Process input (events)"""
    for event in pygame.event.get():
        """Check for closing window"""
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_1:
                game_master.start = True
                player.idle = False

            if event.key == pygame.K_2:
                game_master.start = False

            if event.key == pygame.K_UP:
                player.attack()
                for arrow in up_arrow_sprites.sprites():
                    if arrow in collisions:
                        up_arrow_bw.score()
                        arrow.kill()
                        break
                    else:
                        up_arrow_bw.fail()

            if event.key == pygame.K_DOWN:
                player.attack()
                for arrow in down_arrow_sprites.sprites():
                    if arrow in collisions:
                        down_arrow_bw.score()
                        arrow.kill()
                        break
                    else:
                        down_arrow_bw.fail()

            if event.key == pygame.K_LEFT:
                player.attack()
                for arrow in left_arrow_sprites.sprites():
                    if arrow in collisions:
                        left_arrow_bw.score()
                        arrow.kill()
                        break
                    else:
                        left_arrow_bw.fail()

            if event.key == pygame.K_RIGHT:
                player.attack()
                for arrow in right_arrow_sprites.sprites():
                    if arrow in collisions:
                        right_arrow_bw.score()
                        arrow.kill()
                        break
                    else:
                        right_arrow_bw.fail()

    # Case where a right arrow has aligned completely with the right arrow bw and has not been pressed by the player. 
    for arrow in right_arrow_sprites:
        if arrow.rect.bottom <= HEIGHT/2:
            if arrow in collisions:
                arrow.kill()
                right_arrow_bw.fail()
    
    for arrow in left_arrow_sprites:
        if arrow.rect.bottom <= HEIGHT/2:
            if arrow in collisions:
                arrow.kill()
                left_arrow_bw.fail()
    
    for arrow in up_arrow_sprites:
        if arrow.rect.bottom <= HEIGHT/2:
            if arrow in collisions:
                arrow.kill()
                up_arrow_bw.fail()
    
    for arrow in down_arrow_sprites:
        if arrow.rect.bottom <= HEIGHT/2:
            if arrow in collisions:
                arrow.kill()
                down_arrow_bw.fail()
    
    # choosing arrows 
    arrow = game_master.choose_next_arrow()
    
    # adding arrow to the respective sprite groups
    if arrow != None:
        if arrow.arrow_dir == images.up_arrow:
            up_arrow_sprites.add(arrow)
        elif arrow.arrow_dir == images.down_arrow:
            down_arrow_sprites.add(arrow)
        elif arrow.arrow_dir == images.left_arrow:
            left_arrow_sprites.add(arrow)
        else:
            right_arrow_sprites.add(arrow)
        arrow_sprites.add(arrow)

    """Update"""
    all_sprites.update()
    arrow_sprites.update()
    bw_arrow_sprites.update()

    """Drawing/Rendering"""
    screen.fill(BLACK)

    # Lesson 6 : Step C4
        #screen.blit(background, background_rect)

    """Blit the sprites images"""
    all_sprites.draw(screen)
    bw_arrow_sprites.draw(screen)
    arrow_sprites.draw(screen)
    pygame.display.flip()

"""Close the game"""
pygame.quit()
        
