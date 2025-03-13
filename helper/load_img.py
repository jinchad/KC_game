import pygame
from os import path
img_dir = path.abspath(path.join(path.dirname(__file__), '../resources'))
file_type = ".png"

# initializing the constants for the image names. Ensure that the images have a '.png' extension at the end of their file name.
PLAYER_IDLE_1 = "OnslaughtIdle1"
PLAYER_IDLE_2 = "OnslaughtIdle2"
PLAYER_LOSE = "OnslaughtDead"
PLAYER_ATTACK_1 = "OnslaughtAttack1"
PLAYER_ATTACK_2 = "OnslaughtAttack2"

ENEMY_IDLE_1 = "DKidle1"
ENEMY_IDLE_2 = "DKidle2"
ENEMY_LOSE = "DKdead"
ENEMY_ATTACK_1 = "DKattack1"
ENEMY_ATTACK_2 = "DKattack2"

LEFT_ARROW_PLAYER = "LeftArrowPlayer"
RIGHT_ARROW_PLAYER = "RightArrowPlayer"
DOWN_ARROW_PLAYER = "DownArrowPlayer"
UP_ARROW_PLAYER = "UpArrowPlayer"

LEFT_ARROW_ENEMY = "LeftArrowEnemy"
RIGHT_ARROW_ENEMY = "RightArrowEnemy"
DOWN_ARROW_ENEMY = "DownArrowEnemy"
UP_ARROW_ENEMY = "UpArrowEnemy"

LEFT_ARROW_BW = "LeftArrowBW"
RIGHT_ARROW_BW = "RightArrowBW"
DOWN_ARROW_BW = "DownArrowBW"
UP_ARROW_BW = "UpArrowBW"

LEFT_ARROW_HIT = "LeftArrowHit"
RIGHT_ARROW_HIT = "RightArrowHit"
DOWN_ARROW_HIT = "DownArrowHit"
UP_ARROW_HIT = "UpArrowHit"

LEFT_ARROW_MISS = "LeftArrowMiss"
RIGHT_ARROW_MISS= "RightArrowMiss"
DOWN_ARROW_MISS = "DownArrowMiss"
UP_ARROW_MISS = "UpArrowMiss"

class LoadImage:
    """
    This class is used as a helper class that loads in all sprite images from the resources folder.

    A LoadImage object should be created whenever an image sprite is needed from the resources folder.

    Parameters:
        None
    """
    def __init__(self):
        pass

    def load_images(self):
        """
        This method is used to load the images for all image sprites in the resources folder.

        For the sake of simplicity and to avoid unncessary repetition, the doc strings of this method are abbreviated and condensed into their respective categories.

        Player sprites (Surface): 
            2 idle player sprite images shown when player is idling
            2 attack player sprite images is attacking
            1 player sprite lose image when player has lost the game

        Enemy sprites (Surface): 
            2 idle enemy sprite images shown when enemy is idling
            2 attack enemy sprite images is attacking
            1 enemy sprite lose image when enemy has lost the game

        Arrow sprites (Surface):
            4 player arrow sprites, each representing 1 of the 4 arrow keys for arrows deployed in game for the player
            4 enemy arrow sprites, each representing 1 of the 4 arrows deployed in game for the enemy
            4 black and white arrow sprites, each representing 1 of the 4 black and white arrows in game
            4 hit arrow sprites, each representing 1 of the 4 black and white arrows when they change colour due to a successful hit
            4 miss arrow sprites, each representing 1 of the 4 black and white arrows when they change colour due to a miss        
        """
        player_dir = path.join(img_dir, "player sprites")
        self.player_idle_1 = pygame.image.load(path.join(player_dir, PLAYER_IDLE_1 + file_type)).convert_alpha()
        self.player_idle_2 = pygame.image.load(path.join(player_dir, PLAYER_IDLE_2 + file_type)).convert_alpha()
        self.player_attack_1 = pygame.image.load(path.join(player_dir, PLAYER_ATTACK_1 + file_type)).convert_alpha()
        self.player_attack_2 = pygame.image.load(path.join(player_dir, PLAYER_ATTACK_2 + file_type)).convert_alpha()
        self.player_lose = pygame.image.load(path.join(player_dir, PLAYER_LOSE + file_type)).convert_alpha()

        enemy_dir = path.join(img_dir, "enemy sprites")
        self.enemy_idle_1 = pygame.image.load(path.join(enemy_dir, ENEMY_IDLE_1 + file_type)).convert_alpha()
        self.enemy_idle_2 = pygame.image.load(path.join(enemy_dir, ENEMY_IDLE_2 + file_type)).convert_alpha()
        self.enemy_attack_1 = pygame.image.load(path.join(enemy_dir, ENEMY_ATTACK_1 + file_type)).convert_alpha()
        self.enemy_attack_2 = pygame.image.load(path.join(enemy_dir, ENEMY_ATTACK_2 + file_type)).convert_alpha()
        self.enemy_lose = pygame.image.load(path.join(enemy_dir, ENEMY_LOSE + file_type)).convert_alpha()

        arrow_dir = path.join(img_dir, "arrow sprites")
        self.left_arrow_player = pygame.image.load(path.join(arrow_dir, LEFT_ARROW_PLAYER + file_type)).convert_alpha()
        self.right_arrow_player = pygame.image.load(path.join(arrow_dir, RIGHT_ARROW_PLAYER + file_type)).convert_alpha()
        self.down_arrow_player = pygame.image.load(path.join(arrow_dir, DOWN_ARROW_PLAYER + file_type)).convert_alpha()
        self.up_arrow_player = pygame.image.load(path.join(arrow_dir, UP_ARROW_PLAYER + file_type)).convert_alpha()

        self.left_arrow_enemy = pygame.image.load(path.join(arrow_dir, LEFT_ARROW_ENEMY + file_type)).convert_alpha()
        self.right_arrow_enemy = pygame.image.load(path.join(arrow_dir, RIGHT_ARROW_ENEMY + file_type)).convert_alpha()
        self.down_arrow_enemy = pygame.image.load(path.join(arrow_dir, DOWN_ARROW_ENEMY + file_type)).convert_alpha()
        self.up_arrow_enemy = pygame.image.load(path.join(arrow_dir, UP_ARROW_ENEMY + file_type)).convert_alpha()

        self.left_arrow_bw = pygame.image.load(path.join(arrow_dir, LEFT_ARROW_BW +file_type)).convert_alpha()
        self.right_arrow_bw = pygame.image.load(path.join(arrow_dir, RIGHT_ARROW_BW + file_type)).convert_alpha()
        self.down_arrow_bw = pygame.image.load(path.join(arrow_dir, DOWN_ARROW_BW + file_type)).convert_alpha()
        self.up_arrow_bw = pygame.image.load(path.join(arrow_dir, UP_ARROW_BW + file_type)).convert_alpha()

        self.left_arrow_hit = pygame.image.load(path.join(arrow_dir, LEFT_ARROW_HIT +file_type)).convert_alpha()
        self.right_arrow_hit = pygame.image.load(path.join(arrow_dir, RIGHT_ARROW_HIT + file_type)).convert_alpha()
        self.down_arrow_hit = pygame.image.load(path.join(arrow_dir, DOWN_ARROW_HIT + file_type)).convert_alpha()
        self.up_arrow_hit = pygame.image.load(path.join(arrow_dir, UP_ARROW_HIT + file_type)).convert_alpha()

        self.left_arrow_miss = pygame.image.load(path.join(arrow_dir, LEFT_ARROW_MISS +file_type)).convert_alpha()
        self.right_arrow_miss = pygame.image.load(path.join(arrow_dir, RIGHT_ARROW_MISS + file_type)).convert_alpha()
        self.down_arrow_miss = pygame.image.load(path.join(arrow_dir, DOWN_ARROW_MISS + file_type)).convert_alpha()
        self.up_arrow_miss = pygame.image.load(path.join(arrow_dir, UP_ARROW_MISS + file_type)).convert_alpha()

# In main.py (after pygame.init())
images = LoadImage()
