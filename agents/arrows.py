import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
from dotenv import load_dotenv
from helper.load_img import LoadImage

# loading width and height of pygame from .env
load_dotenv()
WIDTH = int(os.getenv("WIDTH", 400))
HEIGHT = int(os.getenv("HEIGHT", 600))

# loading in images
images = LoadImage()
images.load_images()

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
        speedy (int): Integer determining the speed of the arrow as it ascends in the screen
        arrow_dir (Surface): Pygame Surface determining the direction of the arrow. This is used to determine what to do with the sprite in the game. 
    """

    def __init__(self, centerx = WIDTH/4, image = images.up_arrow_player, arrow_dir: str = "up"):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(image, (50, 50))
        self.rect = self.image.get_rect()
        self.speedy = 3
        self.arrow_dir = arrow_dir

        # setting the center x coordinate of the image rect to centerx input
        self.rect.centerx = centerx

        # setting the bottom y coordinate 
        self.rect.bottom = HEIGHT - 10

    
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

        if self.rect.bottom < HEIGHT/2-self.speedy:
            self.kill()

        

class ArrowBW(Arrow):
    """
    The ArrowBW class is used to store all methods unique to the ArrowBW sprite.

    The ArrowBW class is a child class to the Arrow class

    Args:
        centerx (float): This is a float determing the center x coordinate of the arrow sprite
        image (Surface): This is a pygame surface that determines the sprite of the arrow
        hit_image (Surface): This is a pygame surface that determines the hit image of the arrow
        miss_image (Surface): This is a pygame surface that determines the miss image of the arrow

    Attributes:
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
        """
        This method is used to change the BW arrow sprite to a fail sprite, indicating a failed goal

        Args:
            None

        Returns:
            None
        """
        # obtaining the current timestamp
        curr_time = pygame.time.get_ticks()

        # setting the image of the arrow sprite to "miss"
        self.image = self.miss

        # updating arrow_miss to True as the sprite is now in the "miss" status
        self.arrow_miss = True

        # updating the last arrow miss line
        self.last_arrow_miss = curr_time

        