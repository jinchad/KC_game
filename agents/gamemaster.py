import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
from helper.load_img import LoadImage
import random
from agents.arrows import Arrow
from dotenv import load_dotenv

load_dotenv()

WIDTH = int(os.getenv("WIDTH", 400))

"""Loading in images"""
images = LoadImage()
images.load_images()

"""Arrow dictionary containing x coordinates"""
arrow_dict = {
    # images.left_arrow : WIDTH/5,
    # images.right_arrow : 4*WIDTH/5,
    images.up_arrow : 2*WIDTH/5,
    # images.down_arrow : 3*WIDTH/5
}

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
        self.arrow_choices = [
            images.up_arrow, 
            images.down_arrow, 
            images.left_arrow, 
            images.right_arrow
            ]

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
        