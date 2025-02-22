import pygame
import random
from load_img import LoadImage

WIDTH = 480
HEIGHT = 600
FPS = 60

MAX_HP_BAR_LENGTH = WIDTH*2/3


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
    """
    The Player class is used to store all methods unique to the player.

    This is a child class of the pygame Sprite class.

    Attributes:
        image (Surface): Image displayed as the current player sprite
        rect (Rect): pygame Rect object from the input image
        rect.centerx (Float): Float indicating the x coordinate of the center x coordinate of the image
        rect.bottom (Float): Float indicating the y coordinate at the bottom of the image

        idle (bool): Boolean value indicating that the player is in "idle" status
        idle_sprite_1 (bool): Boolean value indicating that the player's image is idle_sprite_1.

        idle_animation_speed (int): Determines the milliseconds between each sprite switch while the character is in idle
        last_update (int): Integer value serving as a timestamp determining the last time that the player's idle sprite was last updated. 

        attack_animation_speed (int): Determines the milliseconds between each sprite switch while the character is attacking
        last_attack (int): Integer value serving as a timestamp determining the last time that the player's attack sprite was last updated.
    """
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

    def update(self):
        """
        Update method which is called whenever the sprite group is updated.
        
        Args:
            None

        Returns:
            None
        """
        curr_time = pygame.time.get_ticks() # obtaining the current time stamp
        
        # if statement checking if the player is in "idle" form
        if self.idle: 
            # if statement checking if the time difference between the current time stamp and the last idle sprite timestamp exceeds the idle animation speed
            if curr_time - self.last_update > self.idle_animation_speed:
                # if statement checking if the user's sprite is idle_sprite_1
                if self.idle_sprite_1:
                    # setting player image to idle sprite 2
                    self.image = pygame.transform.scale(images.player_idle_2, (100, 100))

                    # setting idle_sprite_1 to False. The next switch will be to idle sprite 1
                    self.idle_sprite_1 = False
                else:
                    # setting player image to idle sprite 1
                    self.image = pygame.transform.scale(images.player_idle_1, (100, 100))

                    # setting idle_sprite_1 to True. The next switch will be to idle sprite 2
                    self.idle_sprite_1 = True

                # updating the last idle time stamp to the new time stamp after updating the sprite
                self.last_update = curr_time
        # else statement for when player is NOT in "idle" form
        else:
            # if statement checking if the time difference between the current time stamp and the last attack time stamp exceeds the attack animation speed
            if curr_time - self.last_attack > self.attack_animation_speed:

                # setting the player image to player_attack_1
                self.image = pygame.transform.scale(images.player_attack_1, (100, 100))
            
            # if statment checking if the time difference between the current time stamp and the last attack time stamp exceeds 3000 ms
            if curr_time - self.last_attack > 3000:

                # setting the player to idle status, which changes the player sprite to "idle" instead of attack
                self.idle = True

    def attack(self): 
        """
        The attack() method is used to change the player sprite. 

        Args: 
            None
        
        Returns:
            None
        """
        # setting the player's idle status to "False" as the player is in attack mode and no longer idling
        self.idle = False

        # Setting the player's image to player_attack_2
        self.image = pygame.transform.scale(images.player_attack_2, (100, 100))

        # updating the player's last attack time stamp to the current time stamp. This is used to determine when the player's sprite should change.
        self.last_attack = pygame.time.get_ticks()

    def lose(self):
        self.image = pygame.transform.scale(images.player_lose, (125, 62))

class Arrow(pygame.sprite.Sprite):
    """
    The Arrow class is used to store all methods unique to the Arrow sprite.

    The Arrow class is a child class of the pygame Sprite class.

    Args:
        centerx (float): This is a float determing the center x coordinate of the arrow sprite
        image (Surface): This is a pygame surface that determines the sprite of the arrow

    Attributes:
        image (Surface): Pygame Surface that is the arrow sprite image
        rect (Rect): Pygame Rect object that is converted from the arrow sprite image
        rect.centerx (float): Float determining the x coordinate of the center of the arrow sprite
        rect/bottom (int): Integer determining the y coordinate of the bottom of the sprite
        speedy (int): Integer determining the speed of the arrow as it ascends in the screen
        arrow_dir (Surface): Pygame Surface determining the direction of the arrow. This is used to determine what to do with the sprite in the game. 
    """

    def __init__(self, centerx = WIDTH/4, image = images.up_arrow):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (50, 50))

        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = HEIGHT - 10
        self.speedy = 3

        self.arrow_dir = image
    
    def update(self):
        """
        This method update() is used to update the position of the Arrow sprite when the Sprite Group updates

        Args:
            None
        
        Returns:
            None
        """
        # Updating the y coordinate of the image with the speed of the arrow
        self.rect.y -= self.speedy
        

class ArrowBW(Arrow):
    """
    The ArrowBW class is used to store all methods unique to the ArrowBW sprite.

    The ArrowBW class is a child class to the Arrow class

    Args:
        centerx (float): This is a float determing the center x coordinate of the arrow sprite
        image (Surface): This is a pygame surface that determines the sprite of the arrow
        hit_image (Surface): This is a pygame surface that determines the hit image of the arrow
        miss_image (Surface): This is a pygame surface that determines the miss image of the arrow

    Attributes
        idle (Surface): Pygame Surface that is the arrow sprite image
        hit (Surface): Pygame Surface that is the arrow sprite hit image
        miss (Surface): Pygame Surface that is the arrow sprite miss image
        rect.bottom (float): Float determining the y coordinate of the bottom of the sprite
        
        arrow_hit (bool): determines if the arrow sprite is in "hit" status
        last_arrow_hit (int): stores the timestamp of the last arrow "hit"

        arrow_miss (bool): determines if the arrow sprite is in "miss" status
        last_arrow_miss (int): stores the timestamp of the last arrow "miss"
    """
    def __init__(self, centerx = WIDTH / 4, image = images.up_arrow_bw, hit_image = images.up_arrow_hit, miss_image = images.down_arrow_miss):
        super().__init__(centerx, image)
        self.idle = pygame.transform.scale(image, (50, 50))
        self.hit = pygame.transform.scale(hit_image, (52, 52))
        self.miss = pygame.transform.scale(miss_image, (52, 52))
        self.rect.bottom = HEIGHT/2

        self.arrow_hit = False
        self.last_arrow_hit = pygame.time.get_ticks()

        self.arrow_miss = False
        self.last_arrow_miss = pygame.time.get_ticks()
    
    def update(self):
        """
        The method update() is used to update the BW arrow as the sprite group updates. 

        It's main purpose is to check for the current arrow sprite image and determine if it's time to change it.

        Args:
            None
        
        Returns:
            None
        """
        # obtaining the current time stamp
        curr_time = pygame.time.get_ticks()

        # if statement determining if the arrow is in "hit" status, then checking if the time difference between the current time stamp and the last arrow hit exceeds 300
        if self.arrow_hit and curr_time - self.last_arrow_hit > 300:
            # arrow sprites image is updated to idle if so
            self.image = self.idle

            # arrow_hit updated to false as the arrow is now in idle
            self.arrow_hit = False

        # if statement determining if the arrow is in "miss" status, then checking if the time difference between the current time stamp and the last arrow miss exceeds 300
        if self.arrow_miss and curr_time-self.last_arrow_miss > 300:
            # arrow sprites image is updated to idle if so
            self.image = self.idle

            # arrow_hit updated to false as the arrow is now in idle
            self.arrow_miss= False
    
    def score(self):
        """
        The method score() is used to update the arrow sprite image to "hit"

        Args:
            None

        Returns:
            None
        """
        # obtaining the current timestamp
        curr_time = pygame.time.get_ticks()

        # setting the image of the arrow sprite to "hit"
        self.image = self.hit

        # updating arrow_hit to True as the sprite is now in "hit" status
        self.arrow_hit = True

        # updating the last arrow hit to current timestamp for future reference
        self.last_arrow_hit = curr_time

    def fail(self):
        curr_time = pygame.time.get_ticks()
        self.image = self.miss
        self.arrow_miss = True
        self.last_arrow_miss = curr_time

        
class GameMaster:
    """
    The GameMaster class is used to decide when and which arrows to send out in game.

    Attributes:
        last_arrow (int): stores the time stamp of the last arrow that has been sent out
        arrow_intervals (int): determines the time difference between each arrow in milliseconds
        arrow_choices (List[Surface]): stores the four possible arrow choices that are pygame Surfaces
        start (bool): determines if the game has started, which determines if the arrows should start sending out
    """
    def __init__(self):
        self.last_arrow = pygame.time.get_ticks()
        self.arrow_intervals = 500
        self.arrow_choices = [images.up_arrow, images.down_arrow, images.left_arrow, images.right_arrow]
        
        self.start = False

    def choose_next_arrow(self):
        """
        The choose_next_arrow() method is used to decide which arrow to send out next.

        This is done through using the random.choice which randomly decides which arrow to send out from arrow_choices

        Args:
            None
        
        Returns:
            if arrow is sent out
                Arrow class with the correct sprite and x coordinates 
            else
                None
        """
        # obtaining the current timestamp in game
        curr_time = pygame.time.get_ticks()

        # if statement checking if the time difference between the current timestamp and the last arrow timestamp exceeds the arrow interval time stamp and if self.start is True
        if curr_time-self.last_arrow > self.arrow_intervals and self.start:
            # choosing a random arrow from the 4 choices
            next_arrow = random.choice(list(arrow_dict.keys()))

            # updating the last_arrow timestamp with the current timestamp
            self.last_arrow = curr_time

            # returning an Arrow class with the correct sprite and x coordinate
            return Arrow(image = next_arrow, centerx= arrow_dict[next_arrow])
        else:
            # returns none if it's not yet time to send out the next arrow
            return None
        
class HealthBar(pygame.sprite.Sprite):
    """
    This class creates a HealthBar object for the player. 
    
    This healthbar is the red healthbar in the game, representing the lost hp for the player. The size of this healthbar remains constant throughout the game and only the green healthbar, which is placed on top of this healthbar, will have its size reduced.

    This is also a child class of the pygame Sprite class.

    Args:
        width (int): optional argument for the width of the health bar
        height(int): optional argument for the height of the health bar
        color (str): optional argument for colour of the health bar representing the lost player hp

    Attributes:
        width (int): width of the health bar
        height (int): height of the health bar
        color (int): color of the health bar
        image (Surface): pygame Surface object creating the rectangular healthbar
        rect (Rect): pygame Rect object of the healthbar
        rect.centerx (float): the center x coordinate of the healthbar
        rect.bottom (float): the bottom y coordinate of the healthbar

    """
    def __init__(self, width: int = MAX_HP_BAR_LENGTH, height: int = HEIGHT/30, color: str = RED):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.color = color
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT*2/5

class GreenHealthBar(HealthBar):
    """
    This class creates the green health bar, representing the remaining hp of the player.

    A player losing hp is represented by reducing the width of this healthbar. 
    
    This is a child class of the HealthBar class.

    Args:
        width (int): optional argument for the width of the health bar
        height(int): optional argument for the height of the health bar
        color (str): optional argument for colour of the health bar representing the lost player hp

    Attributes:
        rect.centerx (float): the center x coordinate of the healthbar
        percentage_loss (int): integer representing the amount of hp gained/loss each increment/decrement. The hp gained/lost is inversely proportional to the value here

        Kindly refer to attributes documented in the HealthBar class for other attributes pertaining tot his class
    """
    def __init__(self, width = MAX_HP_BAR_LENGTH/2, height = HEIGHT / 30, color = GREEN):
        super().__init__(width, height, color)
        self.rect.centerx = WIDTH/2 - width/2
        self.percentage_loss = 40
    
    
    def lose_health(self):
        """
        This function is used when a player loses hp.

        The scale of healthbar reduction is dependent on the percentage loss attribute.

        Args:
            None

        Return:
            None        
        """
        # reducing the width of the health bar
        self.width -= MAX_HP_BAR_LENGTH/2/self.percentage_loss

        # taking the maximum between 0 and the width of the health bar. This ensures that the width of the health bar does not drop below 0. 
        self.width = max(self.width, 0)

        # recreating the healthbar as a pygame Surface 
        self.image = pygame.Surface((self.width, self.height))

        # filling the pygame Surface with the color
        self.image.fill(self.color)

    def gain_health(self):
        """
        This function is used when a player gains hp.

        The scale of healthbar gained is dependent on the percentage loss attribute.

        Args:
            None

        Return:
            None        
        """
        # increasing the width of the health bar
        self.width += MAX_HP_BAR_LENGTH/2/self.percentage_loss

        # taking the minimum between the new width of the health bar and the maximum possible length of the healthbar
        self.width = min(self.width, MAX_HP_BAR_LENGTH)

        # recreating the healthbar as a pygame Surface 
        self.image = pygame.Surface((self.width, self.height))

        # filling the pygame Surface with the color
        self.image.fill(self.color)

all_sprites = pygame.sprite.Group()
player = Player()
healthbar = HealthBar()
player_healthbar = GreenHealthBar()

all_sprites.add(player)
all_sprites.add(healthbar)
all_sprites.add(player_healthbar)

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
game_over = False
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
                up_fail = True
                for arrow in up_arrow_sprites.sprites():
                    if arrow in collisions:
                        up_arrow_bw.score()
                        arrow.kill()
                        player_healthbar.gain_health()
                        up_fail = False
                        break
                if up_fail:
                    up_arrow_bw.fail()
                    player_healthbar.lose_health()

            if event.key == pygame.K_DOWN:
                player.attack()
                down_fail = True
                for arrow in down_arrow_sprites.sprites():
                    if arrow in collisions:
                        down_arrow_bw.score()
                        arrow.kill()
                        player_healthbar.gain_health()
                        down_fail = False
                        break
                if down_fail:
                    down_arrow_bw.fail()
                    player_healthbar.lose_health()

            if event.key == pygame.K_LEFT:
                player.attack()
                left_fail = True
                for arrow in left_arrow_sprites.sprites():
                    if arrow in collisions:
                        left_arrow_bw.score()
                        arrow.kill()
                        player_healthbar.gain_health()
                        left_fail = False
                        break
                if left_fail:
                    left_arrow_bw.fail()
                    player_healthbar.lose_health()

            if event.key == pygame.K_RIGHT:
                player.attack()
                right_fail = True
                for arrow in right_arrow_sprites.sprites():
                    if arrow in collisions:
                        right_arrow_bw.score()
                        arrow.kill()
                        player_healthbar.gain_health()
                        right_fail = False
                        break
                if right_fail:
                    right_arrow_bw.fail()
                    player_healthbar.lose_health()

    # Case where a right arrow has aligned completely with the right arrow bw and has not been pressed by the player. 
    for arrow in right_arrow_sprites:
        if arrow.rect.bottom <= HEIGHT/2:
            if arrow in collisions:
                arrow.kill()
                right_arrow_bw.fail()
                player_healthbar.lose_health()
    
    for arrow in left_arrow_sprites:
        if arrow.rect.bottom <= HEIGHT/2:
            if arrow in collisions:
                arrow.kill()
                left_arrow_bw.fail()
                player_healthbar.lose_health()
    
    for arrow in up_arrow_sprites:
        if arrow.rect.bottom <= HEIGHT/2:
            if arrow in collisions:
                arrow.kill()
                up_arrow_bw.fail()
                player_healthbar.lose_health()
    
    for arrow in down_arrow_sprites:
        if arrow.rect.bottom <= HEIGHT/2:
            if arrow in collisions:
                arrow.kill()
                down_arrow_bw.fail()
                player_healthbar.lose_health()
    
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
    
    if player_healthbar.width <= 0:
        player.lose()
        game_over = True

    """Update"""
    if game_over == False:
        all_sprites.update()
        arrow_sprites.update()
    bw_arrow_sprites.update()

    """Drawing/Rendering"""
    screen.fill(BLACK)

    #screen.blit(background, background_rect)

    """Blit the sprites images"""
    
    all_sprites.draw(screen)
    bw_arrow_sprites.draw(screen)
    arrow_sprites.draw(screen)

    if game_over:
        font = pygame.font.SysFont(None, 72)
        text_surface = font.render("GAME OVER", True, RED)
        text_rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 4))
        screen.blit(text_surface, text_rect)
    pygame.display.flip()

"""Close the game"""
pygame.quit()
        
