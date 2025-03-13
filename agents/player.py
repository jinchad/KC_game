import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
from dotenv import load_dotenv
from helper.load_img import LoadImage

# Loading .env file and initializing the pygame display width and height
load_dotenv()
WIDTH = int(os.getenv("WIDTH", 400))
HEIGHT = int(os.getenv("HEIGHT", 600))

# loading in images
images = LoadImage()
images.load_images()


class Player(pygame.sprite.Sprite):
    """
    The Player class is used to store all methods unique to the player.

    This is a child class of the pygame Sprite class.

    Attributes:
        image (Surface): Image displayed as the current player sprite
        rect (Rect): pygame Rect object from the input image

        idle (bool): Boolean value indicating that the player is in "idle" status
        idle_sprite_1 (bool): Boolean value indicating that the player's image is idle_sprite_1.

        idle_animation_speed (int): Determines the milliseconds between each sprite switch while the character is in idle
        last_update (int): Integer value serving as a timestamp determining the last time that the player's idle sprite was last updated. 

        attack_animation_speed (int): Determines the milliseconds between each sprite switch while the character is attacking
        last_attack (int): Integer value serving as a timestamp determining the last time that the player's attack sprite was last updated.

        sprite_idle_1 (Surface): stores the first idle image of the sprite
        sprite_idle_2 (Surface): stores the second idle image of the sprite
        sprite_attack_1 (Surface): stores the first attack image of the sprite
        sprite_attack_2 (Surface): stores the second attack image of the sprite
        sprite_lose (Surface): stores the lose image of the sprite

    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(images.player_idle_1, (100, 100))
        self.rect = self.image.get_rect()

        # setting the center x coordinate of the player sprite to 1/4 of pygame display width
        self.rect.centerx = WIDTH/4 	

        # setting the bottom y coordinate of the player sprite to 1/4 of the pygame display height
        self.rect.bottom = HEIGHT/4

        self.idle = True
        self.idle_sprite_1 = True

        self.idle_animation_speed = 2000
        self.last_update = pygame.time.get_ticks()

        self.attack_animation_speed = 200
        self.last_attack = pygame.time.get_ticks()

        self.sprite_idle_1 = images.player_idle_1
        self.sprite_idle_2 = images.player_idle_2
        self.sprite_attack_1 = images.player_attack_1
        self.sprite_attack_2 = images.player_attack_2
        self.sprite_lose = images.player_lose

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
                    self.image = pygame.transform.scale(self.sprite_idle_2, (100, 100))

                    # setting idle_sprite_1 to False. The next switch will be to idle sprite 1
                    self.idle_sprite_1 = False
                else:
                    # setting player image to idle sprite 1
                    self.image = pygame.transform.scale(self.sprite_idle_1, (100, 100))

                    # setting idle_sprite_1 to True. The next switch will be to idle sprite 2
                    self.idle_sprite_1 = True

                # updating the last idle time stamp to the new time stamp after updating the sprite
                self.last_update = curr_time
        # else statement for when player is NOT in "idle" form
        else:
            # if statement checking if the time difference between the current time stamp and the last attack time stamp exceeds the attack animation speed
            if curr_time - self.last_attack > self.attack_animation_speed:

                # setting the player image to player_attack_1
                self.image = pygame.transform.scale(self.sprite_attack_1, (100, 100))
            
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
        self.image = pygame.transform.scale(self.sprite_attack_2, (100, 100))

        # updating the player's last attack time stamp to the current time stamp. This is used to determine when the player's sprite should change.
        self.last_attack = pygame.time.get_ticks()

    def lose(self):
        """
        This method changes the sprite's image to a lose image

        Args:
            None
        
        Returns:
            None
        """
        # updating sprite image to lose
        self.image = pygame.transform.scale(self.sprite_lose, (125, 62))

class Enemy(Player):
    """
    This is the Enemy class that creates the imagery for the enemy sprite.

    It is a child class of the player class.

    Attributes:
        image (Surface): Image displayed as the current enemy sprite

        sprite_idle_1 (Surface): stores the first idle image of the enemy
        sprite_idle_2 (Surface): stores the second idle image of the enemy
        sprite_attack_1 (Surface): stores the first attack image of the enemy
        sprite_attack_2 (Surface): stores the second attack image of the enemy
        sprite_lose (Surface): stores the lose image of the enemy

        Kindly refer to the doc strings for the Player class for further elaboration on the class attributes.s
    """
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(images.enemy_idle_1, (100, 100))

        # setting the center x coordinate of the player sprite to 3/4 of pygame display width
        self.rect.centerx = WIDTH*3/4 	

        # setting the bottom y coordinate of the player sprite to 1/4 of the pygame display height
        self.rect.bottom = HEIGHT/4

        self.sprite_idle_1 = images.enemy_idle_1
        self.sprite_idle_2 = images.enemy_idle_2
        self.sprite_attack_1 = images.enemy_attack_1
        self.sprite_attack_2 = images.enemy_attack_2
        self.sprite_lose = images.enemy_lose