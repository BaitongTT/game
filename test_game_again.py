import pygame
import pygame_button
from test_game_again_2  import button,character,ItemBox,item_boxes,item_box_group_health_item,item_box_group_reduce_blood_item
from test_game_again_2  import DirtBlock,LavaBlock,lava_group,Bullet,dirt_blocks,create_blocks_1,move_objects_for_right,HealthBar
pygame.init()

#framerate
clock = pygame.time.Clock()
FPS = 70

#define colours
RED = (255,0,0)
GREEN = (0,255,0)
BLACK =(0,0,0)
WHITE = (255,255,255)

pygame.display.set_caption('Trick or Treat' )
screen = pygame.display.set_mode((720, 400))
width, length = screen.get_size() #get the windows size
#print(width, length) to get 1536, 864

#load images
background_start = pygame.image.load("Image/background_1.png").convert_alpha()
select_characters = pygame.image.load("Image/select_charecter.png").convert_alpha()
background_character_1 = pygame.image.load("Image/select_1.png").convert_alpha()
background_character_2 = pygame.image.load("Image/select_2.png").convert_alpha()
background_character_3 = pygame.image.load("Image/select_3.png").convert_alpha()
background2 = pygame.image.load("Image/background_2.png").convert()

# set button
button_start = button("Image/button_start.png" ,(300,320))  #Button
button_howtoplay= button("Image/button_howtoplay.png",(0,250))
character_1 = button("Image/1_charecter.png",(60,133))
character_2 = button("Image/2_charecter.png",(269,135))
character_3 = button("Image/3_charecter.png",(479,135))
button_back = button("Image/button_back.png",(252,327))
button_play = button("Image/button_play.png",(365,327))


# variable
button_value = False
character_values = [False, False, False]
back_value = False
play_value = False
selected_character_index = 0

#keyboard control
movetothe_left = False
movetothe_right = False

reduce_blood_value = 100   
character_images = ["Image/character_1.png","Image/character_2.png","Image/character_3.png"]
player_rect = pygame.Rect(100,100, 50, 50)
player = None
player_created = False 

'''''
# pick up boxes
health_box_img = pygame.image.load("Image/item_3.png").convert_alpha()
reduce_blood_box_img = pygame.image.load("Image/item_4.png").convert_alpha()
item_boxes = { 
    'Health': health_box_img,
    'Reduce_blood' : reduce_blood_box_img
}
health_item = ItemBox(100, 300, 'Health', player)  
item_box_group_health_item.add(health_item)
damage_item = ItemBox(200, 300, 'Reduce_blood', player)
item_box_group_reduce_blood_item.add(damage_item)
'''

create_blocks_1(0, 361, 6)
create_blocks_1(300, 300, 6)
create_blocks_1(540, 240, 5)
create_blocks_1(780, 361, 12)
#create_ghost(780, 213, 480) # ghost
create_blocks_1(1300, 300, 10)
create_blocks_1(1840, 240, 14)
#create_ghost(1840, 92, 560) # ghost
create_blocks_1(2500, 300, 10)
#create_item_health_item(3000,190) #Item
create_blocks_1(2900, 240, 8)
create_blocks_1(3220, 180, 15)
#create_ghost(3220, 31, 600) # ghost
create_blocks_1(4000, 300, 10)
#create_ghost(4000, 151, 400)  # ghost
create_blocks_1(4400, 240, 9)
create_blocks_1(4800, 361, 6)
#create_item_health_item(4900,310) #Item
create_blocks_1(5040, 300, 5)
create_blocks_1(5240, 240, 15) 
#create_ghost(5240, 92, 600) # ghost
create_blocks_1(6000, 300, 8)
create_blocks_1(6320, 240, 3)
create_blocks_1(6440, 180, 15)
#create_ghost(6440, 31, 600) # ghost
create_blocks_1(7040, 240, 8)
create_blocks_1(7360, 180, 8)
#create_item_health_item(7500,130) #Item
create_blocks_1(7680, 240, 6)
create_blocks_1(7920, 300, 15)
#create_ghost(7920, 151, 600) # ghost
create_blocks_1(8520, 361, 20)
#create_ghost(8520, 213, 800) # ghost
#end of first session

speed = 1
offset_x = 0 
scroll_x = 0
end_of_level_x = 9110   
level_next = False

#game loop
run = True
while run:
    clock.tick(FPS)
    ##Startgame
    screen.fill((0, 0, 0))
    screen.blit(background_start,(0,0))
    button_start.draw(screen)
    #button start
    if button_start.is_pressed():
        button_value = True
    if button_value == True:
        screen.blit(select_characters,(0,0))
        characters = [character_1, character_2, character_3]
        for index, CHARECTER in enumerate(characters):
            CHARECTER.draw(screen)
            if CHARECTER.is_pressed():
                character_values[index] = True
                selected_character_index = index
                break
                
        for index, character_value in enumerate(character_values):
            if character_value:
                screen.blit(eval(f'background_character_{index + 1}'), (0, 0))
                button_play.draw(screen)
                button_back.draw(screen)

                if button_back.is_pressed():
                    back_value = True
                    break
                elif button_play.is_pressed():
                    play_value = True
                    break
            
    if back_value:
        button_value = True
        character_values = [False, False, False]  
        back_value = False

    if play_value:
        screen.fill((0, 0, 0))
        screen.blit(background2,(0,0))
        if not player_created:
            player = character(55, 305, character_images[selected_character_index], 2,reduce_blood_value)
            player_created = True
        if player:
            player.draw(screen)
            health_bar = HealthBar(10,10,player.health,player.health)
            health_bar.draw(player.health)
            player.update_jump(dirt_blocks)
            dirt_blocks.draw(screen)
            should_scroll = move_objects_for_right(player, offset_x, width,end_of_level_x)
            if should_scroll:
                offset_x += player.x_vel
            player.move(movetothe_left, movetothe_right,dirt_blocks,scroll_x, end_of_level_x)
            player.update()
            
        '''''
        item_box_group_health_item.update(scroll_x)
        item_box_group_health_item.draw(screen)
        item_box_group_reduce_blood_item.update(scroll_x)
        item_box_group_reduce_blood_item.draw(screen)
        '''
    
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            run = False
        #keyboard control (pressed)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                movetothe_left = True
            if event.key == pygame.K_RIGHT:
                movetothe_right = True
            if event.key == pygame.K_ESCAPE: #closing game window with ESC
                run = False
            if event.key == pygame.K_UP: 
                player.jump()
            if event.key == pygame.K_SPACE:
                player.shoot()

        #(released)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                movetothe_left = False
            if event.key == pygame.K_RIGHT:
                movetothe_right = False

    pygame.display.update() #update the screen

pygame.quit()