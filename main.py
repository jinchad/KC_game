import pygame
from helper.load_img import LoadImage
import os
from dotenv import load_dotenv

# Loading .env file
load_dotenv()

WIDTH = int(os.getenv("WIDTH", 400))
HEIGHT = int(os.getenv("HEIGHT", 600))
FPS = int(os.getenv("FPS", 60))

BLACK = (0,0,0)
RED = (255,0,0)

"""Initialise pygame and create window"""
pygame.init()

"""Enable sound effects in game"""
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

from agents.arrows import ArrowBW
from agents.gamemaster import GameMaster
from agents.healthbar import HealthBar, GreenHealthBar
from agents.player import Player, Enemy

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

# variable storing the player's turn
player_turn = False

# variable storing the enemy turn
enemy_turn = False

# number of ticks before next character's turn
turn_break = 5000

if __name__ == "__main__":
    # creating a pygame sprite Group that will contain the healthbar sprites, player and enemy sprites for the game
    base_game_sprites = pygame.sprite.Group()

    # creating the player object
    player = Player()

    # creating the enemy object
    enemy = Enemy()

    # creating the "lost" healthbar object
    healthbar = HealthBar()

    # creating the player healthbar object
    player_healthbar = GreenHealthBar()

    # adding the player, healthbar and player_healthbar into the base_game_sprites
    base_game_sprites.add(player)
    base_game_sprites.add(healthbar)
    base_game_sprites.add(player_healthbar)
    base_game_sprites.add(enemy)

    # creating respective sprite groups for all 4 directions. These groups are necessary to control their responses to certain collisions in later parts
    player_left_arrow_sprites = pygame.sprite.Group()
    player_right_arrow_sprites = pygame.sprite.Group()
    player_up_arrow_sprites = pygame.sprite.Group()
    player_down_arrow_sprites = pygame.sprite.Group()

    # creating the arrow_sprites sprite group and adding all 4 arrow sprite groups. This group is used for easier control of all arrow sprites.
    player_arrow_sprites = pygame.sprite.Group()
    player_arrow_sprites.add(
        player_left_arrow_sprites, 
        player_right_arrow_sprites, 
        player_up_arrow_sprites, 
        player_down_arrow_sprites
        )
    
    # creating respective sprite groups for all 4 directions. These groups are necessary to control their responses to certain collisions in later parts
    enemy_left_arrow_sprites = pygame.sprite.Group()
    enemy_right_arrow_sprites = pygame.sprite.Group()
    enemy_up_arrow_sprites = pygame.sprite.Group()
    enemy_down_arrow_sprites = pygame.sprite.Group()

    # creating the arrow_sprites sprite group and adding all 4 arrow sprite groups. This group is used for easier control of all arrow sprites.
    enemy_arrow_sprites = pygame.sprite.Group()
    enemy_arrow_sprites.add(
        enemy_left_arrow_sprites, 
        enemy_right_arrow_sprites, 
        enemy_up_arrow_sprites, 
        enemy_down_arrow_sprites
        )

    # creating the GameMaster objects for player and enemy
    player_game_master = GameMaster()
    enemy_game_master = GameMaster()
    

    # creating a ArrowBW object for the left arrow 
    left_arrow_bw = ArrowBW(centerx = arrow_dict[images.left_arrow], 
                            image = images.left_arrow_bw, 
                            hit_image=images.left_arrow_hit, 
                            miss_image=images.left_arrow_miss)

    # creating a ArrowBW object for the right arrow
    right_arrow_bw = ArrowBW(centerx = arrow_dict[images.right_arrow], 
                            image = images.right_arrow_bw,
                            hit_image=images.right_arrow_hit, 
                            miss_image=images.right_arrow_miss)

    # creating a ArrowBW object for the up arrow
    up_arrow_bw = ArrowBW(centerx = arrow_dict[images.up_arrow], 
                        image = images.up_arrow_bw, 
                        hit_image=images.up_arrow_hit, 
                        miss_image=images.up_arrow_miss)

    # creating a ArrowBW object for the down arrow
    down_arrow_bw = ArrowBW(centerx = arrow_dict[images.down_arrow], 
                            image = images.down_arrow_bw, 
                            hit_image=images.down_arrow_hit, 
                            miss_image=images.down_arrow_miss)

    # creating a Sprite group and adding the bw arrow sprites
    bw_arrows = [left_arrow_bw, right_arrow_bw, up_arrow_bw, down_arrow_bw]
    bw_arrow_sprites = pygame.sprite.Group(bw_arrows)
    for bw_arrow in bw_arrows:
        bw_arrow_sprites.add(bw_arrow)

    # boolean value indicating that the game is running 
    running = True

    # boolean value indicating if the player has lost
    game_over = False

    # while loop the runs indefinitely until the game is stopped
    while running:
        
        # run the loop at the declared FPS
        clock.tick(FPS)
        
        # obtaining a dict of all collisions between arrow sprites and their corresponding bw arrow sprites. 
        # Note that the coloured player sprites are not killed upon immediate contact with the BW arrow sprites.
        collisions = pygame.sprite.groupcollide(player_arrow_sprites, bw_arrow_sprites, False, False)

        # for loop iterating through each event in this instance of pygame
        for event in pygame.event.get():
            # if statement checking if the event type is quitting the game
            if event.type == pygame.QUIT:
                running = False
            
            # if statement checking if the event type is pushing any keys down
            if event.type == pygame.KEYDOWN:
                
                # if statement checking if the detected keydown is the button "1"
                if event.key == pygame.K_1:
                    # if so, the game_master starts
                    player_game_master.start = True

                    # setting the round start timestamp
                    player_game_master.round_start = pygame.time.get_ticks()

                    # player no longer in idle mode
                    player.idle = False

                    player_turn = True

                if event.key == pygame.K_2:
                    player_game_master.start = False

                if event.key == pygame.K_UP:
                    player.attack()
                    up_fail = True
                    if player_turn:
                        for arrow in player_up_arrow_sprites.sprites():
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
                    if player_turn:
                        for arrow in player_down_arrow_sprites.sprites():
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
                    if player_turn:
                        for arrow in player_left_arrow_sprites.sprites():
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
                    if player_turn:
                        for arrow in player_right_arrow_sprites.sprites():
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
        for arrow in player_right_arrow_sprites:
            if arrow.rect.bottom <= HEIGHT/2:
                right_arrow_bw.fail()
                player_healthbar.lose_health()
        
        for arrow in player_left_arrow_sprites:
            if arrow.rect.bottom <= HEIGHT/2:
                left_arrow_bw.fail()
                player_healthbar.lose_health()
        
        for arrow in player_up_arrow_sprites:
            if arrow.rect.bottom <= HEIGHT/2:
                up_arrow_bw.fail()
                player_healthbar.lose_health()
    
        for arrow in player_down_arrow_sprites:
            if arrow.rect.bottom <= HEIGHT/2:
                down_arrow_bw.fail()
                player_healthbar.lose_health()
        
        ## Game logic for enemy arrow sprites

        enemy_success = enemy_game_master.enemy_success()

        for arrow in enemy_right_arrow_sprites:
            if arrow.rect.bottom <= HEIGHT/2:
                if enemy_success:
                    right_arrow_bw.score()
                else:
                    right_arrow_bw.fail()
                    player_healthbar.gain_health()
        
        for arrow in enemy_left_arrow_sprites:
            if arrow.rect.bottom <= HEIGHT/2:
                if enemy_success:
                    left_arrow_bw.score()
                else:
                    left_arrow_bw.fail()
                    player_healthbar.gain_health()
        
        for arrow in enemy_up_arrow_sprites:
            if arrow.rect.bottom <= HEIGHT/2:
                if enemy_success:
                    up_arrow_bw.score()
                else:
                    up_arrow_bw.fail()
                    player_healthbar.gain_health()
    
        for arrow in enemy_down_arrow_sprites:
            if arrow.rect.bottom <= HEIGHT/2:
                if enemy_success:
                    down_arrow_bw.score()
                else:
                    down_arrow_bw.fail()
                    player_healthbar.gain_health()

                 
        if not enemy_turn:
            enemy_turn = player_game_master.switch_player()
            
            if enemy_turn:
                enemy_game_master.start = True
                enemy_game_master.round_start = pygame.time.get_ticks()

        if not player_turn:
            player_turn = enemy_game_master.switch_player()

            if player_turn:
                player_game_master.start = True
                player_game_master.round_start = pygame.time.get_ticks()
        
        if player_turn:
            # choosing arrows
            arrow = player_game_master.choose_next_arrow()
            
            # adding arrow to the respective sprite groups
            if arrow != None:
                arrow_direction = arrow.arrow_dir.lower()
                match arrow_direction:
                    case "up":
                        player_up_arrow_sprites.add(arrow)
                    case "down":
                        player_down_arrow_sprites.add(arrow)
                    case "left":
                        player_left_arrow_sprites.add(arrow)
                    case "right":
                        player_right_arrow_sprites.add(arrow)
                player_arrow_sprites.add(arrow)
                    
        if enemy_turn:
            arrow = enemy_game_master.choose_next_arrow()
            
            if arrow != None:
                arrow_direction = arrow.arrow_dir.lower()
                match arrow_direction:
                    case "up":
                        enemy_up_arrow_sprites.add(arrow)
                    case "down":
                        enemy_down_arrow_sprites.add(arrow)
                    case "left":
                        enemy_left_arrow_sprites.add(arrow)
                    case "right":
                        enemy_right_arrow_sprites.add(arrow)
                enemy_arrow_sprites.add(arrow)
           

        if len(player_arrow_sprites.sprites()) > 0:
            player_turn = True
        else:
            player_turn = False
        
        if player_healthbar.width <= 0:
            player.lose()
            game_over = True

        if len(enemy_arrow_sprites.sprites()) > 0:
            enemy_turn = True
        else:
            enemy_turn = False
        
        if player_healthbar.width <= 0:
            player.lose()
            game_over = True

        """Update"""
        if game_over == False:
            base_game_sprites.update()
            player_arrow_sprites.update()
            enemy_arrow_sprites.update()
        bw_arrow_sprites.update()

        """Drawing/Rendering"""
        screen.fill(BLACK)

        #screen.blit(background, background_rect)

        """Blit the sprites images"""
        base_game_sprites.draw(screen)
        bw_arrow_sprites.draw(screen)
        player_arrow_sprites.draw(screen)
        enemy_arrow_sprites.draw(screen)

        if game_over:
            font = pygame.font.SysFont(None, 72)
            text_surface = font.render("GAME OVER", True, RED)
            text_rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 4))
            screen.blit(text_surface, text_rect)
        pygame.display.flip()

    """Close the game"""
    pygame.quit()
            
