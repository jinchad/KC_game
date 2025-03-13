import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
from helper.load_img import LoadImage
import random
from agents.arrows import Arrow
from dotenv import load_dotenv

# initializing width and game difficiulty variables stored in .env
load_dotenv()
WIDTH = int(os.getenv("WIDTH", 400))
GAME_DIFFICULTY = os.getenv("GAME_DIFFICULTY", "easy").lower() # directly influences the arrow intervals and the enemy success probability

# game difficulty dict storing the arrow interval and enemy success probability
game_difficulty = {
            "easy": {
                "arrow interval":  500, # arrows come in intervals of 500 milliseconds
                "enemy success probability": 0.3 # enemy's probability of success is 1-0.3 = 0.7
            },
            "medium": {
                "arrow interval":  450, # arrows come in intervals of 450 milliseconds
                "enemy success probability": 0.2 # enemy's probability of success is 1-0.2 = 0.8
            },
            "hard": {
                "arrow interval":  400, # arrows come in intervals of 400 milliseconds
                "enemy success probability": 0.1 # enemy's probability of success is 1-0.1 = 0.9
            },
            "extreme": {
                "arrow interval":  300, # arrows come in intervals of 300 milliseconds
                "enemy success probability": 0.05 # enemy's probability of success is 1-0.05 = 0.95
            }
        }

# obtaining the appropriate game difficulty
difficulty_dict = game_difficulty[GAME_DIFFICULTY]

# duration of a round for player/bot is set to 20 arrows
ROUND_DURATION = difficulty_dict["arrow interval"]*20

# interval between each switch over, which is 2000 milliseconds
PLAYER_INTERVAL = 2000

# loading images 
images = LoadImage()
images.load_images()

# arrow dictionary containing a tuple, which contains the image sprite for player's arrow, image sprite for enemy's arrow, and x coordinate of the arrow
# each tuple is stored based on keys for each of the 4 arrow keys.
arrow_dict = {
    "left": (images.left_arrow_player, images.left_arrow_enemy, WIDTH/5),
    "right": (images.right_arrow_player, images.right_arrow_enemy, 4*WIDTH/5),
    "up": (images.up_arrow_player, images.up_arrow_enemy, 2*WIDTH/5),
    "down": (images.down_arrow_player, images.down_arrow_enemy, 3*WIDTH/5)
}

class GameMaster:
    """
    The GameMaster class is used to decide when and which arrows to send out in game. 
    
    In this class, the term "player" is used loosely as a gamemaster object is used to control the gameplay for both enemy and player sprites.

    Args:
        is_player (bool): boolean value indicating if the gamemaster object is for player or for enemy. This directly influences the type of arrow being sent out.

    Attributes:
        last_arrow (int): stores the time stamp of the last arrow that has been sent out
        round_start (int | None): stores the timestamp of the start of the game
        start (bool): determines if the game has started. If True, arrows will start being sent out
        is_player (bool): boolean value indicating if the gamemaster object is for player or for enemy
        player_end (int): integer indicating the timestamp in which the player's round has ended. This is used to determine if it's time for the opponent sprite to start.
    """
    def __init__(self, is_player: str):
        self.last_arrow = pygame.time.get_ticks()
        self.round_start = None
        self.start = False
        self.is_player = is_player
        self.player_end = 0

    def choose_next_arrow(self):
        """
        The choose_next_arrow() method is used to decide which arrow to send out next.

        This is done through using the random.choice which randomly decides which arrow to send out from arrow_dict

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
        if curr_time-self.last_arrow > difficulty_dict["arrow interval"] and self.start:

            # if statement checking if this player's round has exceeded the set duration of a single round. This logic helps decide when it's time for the gamemaster to stop.
            if curr_time - self.round_start >= ROUND_DURATION:
                # gamemaster is stopping
                self.start = False

                # round_start is set to None again as this player's round has ended
                self.round_start = None

                # set the player_end timestamp to the current time stamp
                self.player_end = curr_time

                # returning None as no arrows have been sent out
                return None
            
            # choosing a random arrow from the 4 choices
            next_arrow = random.choice(list(arrow_dict.keys()))

            # updating the last_arrow timestamp with the current timestamp
            self.last_arrow = curr_time

            # returning an Arrow class with the correct sprite and x coordinate
            if self.is_player:
                return Arrow(arrow_dir= next_arrow, image = arrow_dict[next_arrow][0], centerx= arrow_dict[next_arrow][2])
            else:
                return Arrow(arrow_dir= next_arrow, image = arrow_dict[next_arrow][1], centerx= arrow_dict[next_arrow][2])
        else:
            # returns none if it's not yet time to send out the next arrow
            return None
    
    def switch_player(self):
        """
        This method is used to determine if it's time to switch player turns.

        Args:
            None
        
        Returns:
            True if it's time to switch player turn
            False otherwise
        """
        # obtaining the current game timestamp
        curr_time = pygame.time.get_ticks()

        # if statement checking if there is any timestamp stored under player_end
        if self.player_end:
            # if statement that then checks if sufficient time has passed between the timestamp of the player's end and the current timestamp
            if curr_time - self.player_end >= PLAYER_INTERVAL:
                # sets player_end to None as it's no longer the player's turn and it has moved to the opponents
                self.player_end = None

                # return True as it is time to swap turns to the other player 
                return True 
            
            # returns False as even though the current player's turn has ended, insufficient time has passed for the other player to start
            return False
        
        # returns False as it's still the current player's turn
        return False

    def enemy_success(self):
        """
        This method is used to determine if a enemy (bot) has succeeded in choosing the correct arrow. 

        This method is used exclusively by gamemaster that is controlling the enemy sprite.

        Args:
            None
        
        Returns:
            if bot succeeds:
                return True 
            else:
                return False
        """
        # if statement checking if the gamemaster is controlling a bot
        if not self.is_player:
            # obtaining the enemy's chance for success
            enemy_chance = random.random()

            # obtaining the enemy's probability of success based on the game's difficulty setting
            enemy_success_probability = difficulty_dict["enemy success probability"]

            # returns True if enemy succeeds else False
            return True if enemy_chance >= enemy_success_probability else False
        else:
            # returns False as the gamemaster is not contraolling a plyer
            return False



        
