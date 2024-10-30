import pygame
from Button import Button
pygame.init()

#framerate
clock = pygame.time.Clock()
FPS = 80

pygame.display.set_caption('Trick or Treat' )
screen = pygame.display.set_mode((720, 400))
width, length = screen.get_size() #get the windows size
#print(width, length) to get 1536, 864
screen.fill((0, 0, 0))

#load images
background_start = pygame.image.load("Image/background_1.png").convert_alpha()
select_characters = pygame.image.load("Image/select_charecter.png").convert_alpha()
background_character_1 = pygame.image.load("Image/select_1.png").convert_alpha()
background_character_2 = pygame.image.load("Image/select_2.png").convert_alpha()
background_character_3 = pygame.image.load("Image/select_3.png").convert_alpha()

# set button
button_start = Button("Image/button_start.png" ,(300,320))  #Button เป็นการกำหนดว่ารูปนี้คือปุ่ม
button_howtoplay= Button("Image/button_howtoplay.png",(0,250))
character_1 = Button("Image/1_charecter.png",(60,133))
character_2 = Button("Image/2_charecter.png",(269,135))
character_3 = Button("Image/3_charecter.png",(479,135))
button_back = Button("Image/button_back.png",(252,327))
button_play = Button("Image/button_play.png",(365,327))


# variable
button_value = False
character_values = [False, False, False]
back_value = False
play_value = False

#game loop
run = True
while run:
    clock.tick(FPS)
    ##Startgame
    screen.blit(background_start,(0,0))
    button_start.draw(screen)
    #button start
    if button_start.is_pressed():
        button_value = True
    if button_value == True:
        screen.blit(select_characters,(0,0))
        characters = [character_1, character_2, character_3]
        for index, character in enumerate(characters):
            character.draw(screen)
            if character.is_pressed():
                character_values[index] = True
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
        print(111)
        break
  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    pygame.display.update()
pygame.quit()