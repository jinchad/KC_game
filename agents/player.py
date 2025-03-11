import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
from dotenv import load_dotenv
from helper.load_img import LoadImage

# Loading .env file
load_dotenv()

WIDTH = int(os.getenv("WIDTH", 400))
HEIGHT = int(os.getenv("HEIGHT", 600))

"""Loading in images"""
images = LoadImage()
images.load_images()


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

