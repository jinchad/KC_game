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
MAX_HP_BAR_LENGTH = WIDTH*2/3
RED = (255,0,0)
GREEN = (0,255,0)

"""Loading in images"""
images = LoadImage()
images.load_images()

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

