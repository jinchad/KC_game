import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
from dotenv import load_dotenv
from helper.load_img import LoadImage

# Initializing the width and heigh variables for the pygame display and the game difficulty from the .env
load_dotenv()
WIDTH = int(os.getenv("WIDTH", 400))
HEIGHT = int(os.getenv("HEIGHT", 600))
GAME_DIFFICULTY = os.getenv("GAME_DIFFICULTY", "easy").lower()

# match case for setting the appropriate game difficulty variables
match GAME_DIFFICULTY:
    case "easy":
        difficulty_dict = {
            "percentage_loss": 40, # percentage loss is an integer that scales inversely with the player's hp loss.
            "percentage_gain": 20 # percentage gain is an integer that scales inversely with the player's hp gain.
        }
    case "medium":
        difficulty_dict = {
            "percentage_loss": 30,
            "percentage_gain": 25
        }
    case "hard":
        difficulty_dict = {
            "percentage_loss": 20,
            "percentage_gain": 30
        }
    case "extreme":
        difficulty_dict = {
            "percentage_loss": 15,
            "percentage_gain": 40
        }
# maximum possible length of the HP bar will be 2/3 that of the display width
MAX_HP_BAR_LENGTH = WIDTH*2/3

# tuple representing the RGB values of red and green colours
RED = (255,0,0)
GREEN = (0,255,0)

# loading in images
images = LoadImage()
images.load_images()

class HealthBar(pygame.sprite.Sprite):
    """
    This class creates a HealthBar object for the player. 
    
    This healthbar is the red healthbar in the game, representing the lost hp for the player. 
    
    The size of this healthbar remains constant throughout the game and only the green healthbar, which is placed on top of this healthbar, will have its size reduced.

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

    """
    def __init__(self, width: int = MAX_HP_BAR_LENGTH, height: int = HEIGHT/30, color: str = RED):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.color = color
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()

        # setting the colour of the player's missing hp bar to color. 
        self.image.fill(self.color)

        # setting center x coordinate of the healthbar to center of the display
        self.rect.centerx = WIDTH/2

        # setting the bottom y coordinate of the image rect to 2/5 of the display height
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

        Kindly refer to attributes documented in the HealthBar class for other attributes pertaining to this class
    """
    def __init__(self, width = MAX_HP_BAR_LENGTH/2, height = HEIGHT / 30, color = GREEN):
        super().__init__(width, height, color)
        self.rect.centerx = WIDTH/2 - width/2
    
    def lose_health(self):
        """
        This function is used when a player loses hp due to missing an arrow.

        The scale of healthbar reduction is dependent on the percentage loss attribute.

        Args:
            None

        Return:
            None        
        """
        # reducing the width of the health bar
        self.width -= MAX_HP_BAR_LENGTH/2/difficulty_dict["percentage_loss"]

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
        self.width += MAX_HP_BAR_LENGTH/2/difficulty_dict["percentage_gain"]

        # taking the minimum between the new width of the health bar and the maximum possible length of the healthbar
        self.width = min(self.width, MAX_HP_BAR_LENGTH)

        # recreating the healthbar as a pygame Surface 
        self.image = pygame.Surface((self.width, self.height))

        # filling the pygame Surface with the color
        self.image.fill(self.color)
    
    def enemy_score(self):
        """
        This function is used when a player loses hp due to enemy scoring.

        The scale of healthbar reduction is dependent on the percentage loss attribute.

        A seperate method is used instead of the lose_health() as the penalty from an enemy scoring should be softer than when the player makes a mistake

        Args:
            None

        Return:
            None        
        """
        # reducing the width of the health bar
        self.width -= MAX_HP_BAR_LENGTH/10/difficulty_dict["percentage_loss"]

        # taking the maximum between 0 and the width of the health bar. This ensures that the width of the health bar does not drop below 0. 
        self.width = max(self.width, 0)

        # recreating the healthbar as a pygame Surface 
        self.image = pygame.Surface((self.width, self.height))

        # filling the pygame Surface with the color
        self.image.fill(self.color)

