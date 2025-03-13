import pygame
from helper.load_img import LoadImage
import os
from dotenv import load_dotenv

# Loading .env file to obtain the width and height of the pygame display and the FPS of the game
load_dotenv()
WIDTH = int(os.getenv("WIDTH", 400))
HEIGHT = int(os.getenv("HEIGHT", 600))
FPS = int(os.getenv("FPS", 60))

# constant variable for the maximum with of the hp bar
MAX_HP_BAR_LENGTH = WIDTH * 2/3

# tuple representing the RGB values of black and red
BLACK = (0,0,0)
RED = (255,0,0)

# initializing pygame
pygame.init()

# enabling sound effects in game (though not implemented)
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# importing rest of the classes. Note that the classes are imported here as the pygame display needs to be created first for the sprites to spawn on or an error will occur.
from agents.arrows import ArrowBW
from agents.gamemaster import GameMaster
from agents.healthbar import HealthBar, GreenHealthBar
from agents.player import Player, Enemy

# loading in sprite images
images = LoadImage()
images.load_images()

# arrow dictionary containing the x coordinate for all arrow sprites
arrow_dict = {
    "left" : WIDTH/5,
    "right" : 4*WIDTH/5,
    "up" : 2*WIDTH/5,
    "down" : 3*WIDTH/5
}

# creating pygame clock object for controlling game speed
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
    player_game_master = GameMaster(is_player=True)
    enemy_game_master = GameMaster(is_player=False)
    

    # creating a ArrowBW object for the left arrow 
    left_arrow_bw = ArrowBW(centerx = arrow_dict["left"], 
                            image = images.left_arrow_bw, 
                            hit_image=images.left_arrow_hit, 
                            miss_image=images.left_arrow_miss)

    # creating a ArrowBW object for the right arrow
    right_arrow_bw = ArrowBW(centerx = arrow_dict["right"], 
                            image = images.right_arrow_bw,
                            hit_image=images.right_arrow_hit, 
                            miss_image=images.right_arrow_miss)

    # creating a ArrowBW object for the up arrow
    up_arrow_bw = ArrowBW(centerx = arrow_dict["up"], 
                        image = images.up_arrow_bw, 
                        hit_image=images.up_arrow_hit, 
                        miss_image=images.up_arrow_miss)

    # creating a ArrowBW object for the down arrow
    down_arrow_bw = ArrowBW(centerx = arrow_dict["down"], 
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

    # boolean value indicating if the game is over
    game_over = False

    # boolean value indicating if the player has lost
    player_lost = False

    # while loop the runs indefinitely until the game is stopped
    while running:
        
        # run the loop at the declared FPS
        clock.tick(FPS)
        
        # obtaining a dict of all collisions between arrow sprites and their corresponding bw arrow sprites. 
        # Note that the coloured player sprites are not killed upon immediate contact with the BW arrow sprites.
        collisions = pygame.sprite.groupcollide(player_arrow_sprites, bw_arrow_sprites, False, False)
        
        ## Game logic for handling keyboard inputs from the player
        # for loop iterating through each event in this instance of pygame
        for event in pygame.event.get():
            # if statement checking if the event type is quitting the game
            if event.type == pygame.QUIT:
                running = False
            
            # if statement checking if the event type is pushing any keys down
            if event.type == pygame.KEYDOWN:
                
                # if statement checking if the detected keydown is the button "1"
                if event.key == pygame.K_1 and not game_over:
                    # if so, the game_master starts
                    player_game_master.start = True

                    # setting the round start timestamp
                    player_game_master.round_start = pygame.time.get_ticks()

                    # player no longer in idle mode
                    player.idle = False

                    # player has started playing
                    player_turn = True

                # if statement checking if the player has pressed on the up arrow key
                if event.key == pygame.K_UP:
                    # displaying the player attack animation
                    player.attack()

                    # boolean value storing if the player has failed to time the up arrow key successfully.
                    # if it's not player's turn, this is set to false so player hp is not lost when up arrow key is pressed during bot's turn
                    up_fail = True if player_turn else False

                    # for loop iterating through all player arrow sprites
                    for arrow in player_up_arrow_sprites.sprites():
                        # if arrow has collide with BW arrow
                        if arrow in collisions:
                            # change BW up arrow to score arrow sprite
                            up_arrow_bw.score()

                            # kill the player arrow sprite
                            arrow.kill()

                            # player gains health
                            player_healthbar.gain_health()

                            # player did not fail to press the up key correctly
                            up_fail = False

                            # break the loop
                            break
                    # if loop checking if the user has failed to time the arrow (missed the arrow)
                    if up_fail:
                        # changeBW up arrow to fail arrow sprite
                        up_arrow_bw.fail()
                        
                        # player loses health
                        player_healthbar.lose_health()

                # if statement checking if the player has pressed the down arrow key
                if event.key == pygame.K_DOWN:
                    # changing player sprite to attack player sprite
                    player.attack()

                    # tracks if the user has failed to time the arrow
                    down_fail = True if player_turn else False

                    # for loop iterating through each player down arrow sprite
                    for arrow in player_down_arrow_sprites.sprites():
                        # if statement checking if the down arrow has collided with a BW arrow
                        if arrow in collisions:
                            # changing the BW down arrow to the score arrow sprite
                            down_arrow_bw.score()

                            # killing the player arrow
                            arrow.kill()

                            # player gains health
                            player_healthbar.gain_health()

                            # setting down_fail to false as player has timed the arrow properly
                            down_fail = False

                            # breaking the loop 
                            break
                    # if player has failed to time the arrow properly (missed the arrow)
                    if down_fail:
                        # change BW down arrow to fail arrow sprite
                        down_arrow_bw.fail()

                        # player loses health
                        player_healthbar.lose_health()

                # if statement checking if the user has pressed the left arrow key
                if event.key == pygame.K_LEFT:
                    # changing the player sprite to attack
                    player.attack()

                    # left_fail tracks if user has failed to press the left key properly
                    left_fail = True if player_turn else False

                    # for loop iterating through each player left arrow sprites
                    for arrow in player_left_arrow_sprites.sprites():
                        # if statement checking if arrow has collided with a BW arrow
                        if arrow in collisions:
                            # changing the BW left arrow to score arrow sprite
                            left_arrow_bw.score()

                            # killing the arrow
                            arrow.kill()

                            # player gains health
                            player_healthbar.gain_health()

                            # left_fail set to false as player has time it properly 
                            left_fail = False

                            # break the loop
                            break

                    # if player has failed to time the arrow properly (missed the arrow)
                    if left_fail:
                        # change the bw left arrow to fail arrow sprite
                        left_arrow_bw.fail()

                        # player loses healths
                        player_healthbar.lose_health()

                # if statement checking if the user has pressed the right arrow key
                if event.key == pygame.K_RIGHT:
                    # changing player sprite to attack player sprite
                    player.attack()

                    # right_fail tracks if user has failed to press the right key properly
                    right_fail = True if player_turn else False

                    # for loop iterating through each player right arrow sprite
                    for arrow in player_right_arrow_sprites.sprites():
                        # if player arrow has collided with a BW arrow
                        if arrow in collisions:
                            # change BW arrow to score arrow sprite
                            right_arrow_bw.score()

                            # kill player arrow
                            arrow.kill()

                            # player gains health
                            player_healthbar.gain_health()
                            
                            # right_fail set to False as player has timed the arrow properly
                            right_fail = False

                            # breaking the for loop
                            break
                    # if player has failed to time the arrow properly (missed the arrow)
                    if right_fail:
                        # change bw right arrow to fail
                        right_arrow_bw.fail()

                        # player loses health
                        player_healthbar.lose_health()


        ## Game logic for when a player's arrow sprite has aligned completely with the arrow bw but has not been pressed by the player (aka player has missed the arrow sprite)
        # for loop iterating through each player right arrows
        for arrow in player_right_arrow_sprites:
            # if statement checking if the bottom y coordinate has reached that of the BW right arrow
            if arrow.rect.bottom <= HEIGHT/2:
                # change BW arrow sprite to fail sprite
                right_arrow_bw.fail()

                # player loses health
                player_healthbar.lose_health()
        # for loop iterating through each player left arrows
        for arrow in player_left_arrow_sprites:
            # if statement checking if the bottom y coordinate has reached that of the BW left arrow
            if arrow.rect.bottom <= HEIGHT/2:
                # change BW arrow sprite to fail sprite
                left_arrow_bw.fail()
                
                # player loses health
                player_healthbar.lose_health()
        
        # for loop iterating through each player up arrows
        for arrow in player_up_arrow_sprites:
            # if statement checking if the bottom y coordinate has reached that of the BW up arrow
            if arrow.rect.bottom <= HEIGHT/2:
                # change BW arrow sprite to fail sprite
                up_arrow_bw.fail()

                # player loses health
                player_healthbar.lose_health()

        # for loop iterating through each player down arrows
        for arrow in player_down_arrow_sprites:
            # if statement checking if the bottom y coordinate has reached that of the BW down arrow
            if arrow.rect.bottom <= HEIGHT/2:
                # change BW arrow sprite to fail sprite
                down_arrow_bw.fail()

                # player loses health
                player_healthbar.lose_health()
        
        ## Game logic for handling enemy arrow sprites
        # obtaining boolean value determing if the enemy has succeeded in timing the arrow
        enemy_success = enemy_game_master.enemy_success()

        # for loop iterating through each right enemy arrow sprite
        for arrow in enemy_right_arrow_sprites:
            # if statement checking if the arrow's y coordinate has reached the BW arrow 
            if arrow.rect.bottom <= HEIGHT/2:
                # changing current enemy sprite to attack enemy sprite
                enemy.attack()

                # if statement checking if enemy has succeeded
                if enemy_success:
                    # changing right bw arrow to score right arrow
                    right_arrow_bw.score()

                    # player loses some health
                    player_healthbar.enemy_score()
                else:
                    # changing right bw arrow to fail right arrow
                    right_arrow_bw.fail()

        # for loop iterating through each right enemy arrow sprite
        for arrow in enemy_left_arrow_sprites:
            if arrow.rect.bottom <= HEIGHT/2:
                enemy.attack()
                if enemy_success:
                    left_arrow_bw.score()
                    player_healthbar.enemy_score()
                else:
                    left_arrow_bw.fail()
                    
        # for loop iterating through each right enemy arrow sprite
        for arrow in enemy_up_arrow_sprites:
            if arrow.rect.bottom <= HEIGHT/2:
                enemy.attack()
                if enemy_success:
                    up_arrow_bw.score()
                    player_healthbar.enemy_score()
                else:
                    up_arrow_bw.fail()

        # for loop iterating through each right enemy arrow sprite
        for arrow in enemy_down_arrow_sprites:
            if arrow.rect.bottom <= HEIGHT/2:
                enemy.attack()
                if enemy_success:
                    down_arrow_bw.score()
                    player_healthbar.enemy_score()
                else:
                    down_arrow_bw.fail()

        ## Game logic for checking if it's time for the enemy/player to start their turn
        # if statement checking if it's not the enemy's turn and if the game is not yet over
        if not enemy_turn and not game_over:
            # obtaining boolean value determining if it's time to switch the player
            enemy_turn = player_game_master.switch_player()
            
            # if statement checking if it's the enemy's turn
            if enemy_turn:
                # starting up the enemy's gamemaster
                enemy_game_master.start = True
                enemy_game_master.round_start = pygame.time.get_ticks()

        # if statement checking if it's the enemy's turn
        if enemy_turn:
            # obtaining the next arrow for the enemy, if any
            arrow = enemy_game_master.choose_next_arrow()
            
            # if statement checking if any arrow has been sent out
            if arrow != None:
                # obtaining string value of the arrow's direction
                arrow_direction = arrow.arrow_dir.lower()

                # match case for arrow's direction that adds the arrow to the correct enemy arrow sprite group
                match arrow_direction:
                    case "up":
                        enemy_up_arrow_sprites.add(arrow)
                    case "down":
                        enemy_down_arrow_sprites.add(arrow)
                    case "left":
                        enemy_left_arrow_sprites.add(arrow)
                    case "right":
                        enemy_right_arrow_sprites.add(arrow)

                # adding the enemy arrow sprite into the general enemy arrow sprite group
                enemy_arrow_sprites.add(arrow)

        # if statement checking if it's not the player's turn and if the game is not yet over
        if not player_turn and not game_over:
            # obtaining boolean value determining if it's time to switch the player
            player_turn = enemy_game_master.switch_player()

            # if statement checking if it's the player's turm
            if player_turn:
                # starting up player's gamemaster
                player_game_master.start = True
                player_game_master.round_start = pygame.time.get_ticks()
        
        if player_turn:
            # choosing arrows 
            arrow = player_game_master.choose_next_arrow()
            
            # adding arrow to the respective sprite groups
            if arrow != None:
                # obtaining the string value indicating the arrow's direction
                arrow_direction = arrow.arrow_dir.lower()

                # match case for arrow's direction that adds the arrow to the correct player arrow sprite group
                match arrow_direction:
                    case "up":
                        player_up_arrow_sprites.add(arrow)
                    case "down":
                        player_down_arrow_sprites.add(arrow)
                    case "left":
                        player_left_arrow_sprites.add(arrow)
                    case "right":
                        player_right_arrow_sprites.add(arrow)
                # adding the arrow sprite to the general player arrow sprite group
                player_arrow_sprites.add(arrow)
           
        ## Game logic for additional checks. This ensures that as long as there are any player/enemy arrow sprites still existing in game, it will always be the correct turn.
        # if statement checking if there are any player arrow sprites
        if len(player_arrow_sprites.sprites()) > 0:
            # setting player_turn to true if so
            player_turn = True
        else:
            # setting player_turn to false since no player arrow sprites
            player_turn = False

        # if statement checking if there are any enemy arrow sprites
        if len(enemy_arrow_sprites.sprites()) > 0:
            # setting enemy_turn to true if so
            enemy_turn = True
        else:
            enemy_turn = False

        ## Game logic for checking if player has won/lost the game through the width of the player's healthbar
        # if statement checking if the player's healthbar width is less than or equals to 0
        if player_healthbar.width <= 0:
            # changing player's sprite to a lose player sprite
            player.lose()
            
            # setting game_over to true as the game has concluded with the player's loss
            game_over = True

            # setting player_lost to true as player has lost
            player_lost = True

        # elif statement checking if the player's healthbar has exceeded that of the maximum healthbar length
        elif player_healthbar.width >= MAX_HP_BAR_LENGTH:
            # if statement checking it's not the enemy's turn and it's the players turn
            # this ensures that the player cannot win due to the enemy's mistake. In other words, player only wins in the following round even if player's hp bar is full.
            if not enemy_turn and player_turn:
                # changing enemy current sprite to the enemy lose sprite
                enemy.lose()

                # setting game_over to True as game has concluded with the player's victory
                game_over = True

                # setting player_lost to false as player has won
                player_lost = False
            

        ## Game logic for sprite updates
        # if statement checking if the game has concluded
        if game_over == False:
            # updating all necessary sprite groups
            base_game_sprites.update()
            player_arrow_sprites.update()
            enemy_arrow_sprites.update()
            bw_arrow_sprites.update()

        # filling screen with black background
        screen.fill(BLACK)

        #screen.blit(background, background_rect)

        # drawing all necessary sprites on screen. This is placed here to ensure that all sprites are still drawn even upon the game's conclusion
        base_game_sprites.draw(screen)
        bw_arrow_sprites.draw(screen)
        player_arrow_sprites.draw(screen)
        enemy_arrow_sprites.draw(screen)
        
        # if statement checking if the game has concluded
        if game_over:
            # setting the pygame font to size 64
            font = pygame.font.SysFont(None, 64)
            
            # if statement checking if the player has lost to display the appropriate game over text
            if player_lost:
                text_surface = font.render("YOU LOSE", True, RED)
            else:
                text_surface = font.render("YOU WIN", True, RED)

            # setting the text rect
            text_rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 4))

            # adding the game over text to the screen
            screen.blit(text_surface, text_rect)

            # stopping all gamemasters
            enemy_game_master.start = False
            player_game_master.start = False
    
        pygame.display.flip()

    """Close the game"""
    pygame.quit()
            
