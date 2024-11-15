import pygame
import pygame_button
pygame.init()

#game loop
def game_loop(game,clock,screen):
    #load images
    background_start = pygame.image.load("Image/background_1.png").convert_alpha()
    select_characters = pygame.image.load("Image/select_charecter.png").convert_alpha()
    background_character_1 = pygame.image.load("Image/select_1.png").convert_alpha()
    background_character_2 = pygame.image.load("Image/select_2.png").convert_alpha()
    background_character_3 = pygame.image.load("Image/select_3.png").convert_alpha()

    class button:
            def __init__(self, image_path, position, scale = 1.0):
                self.image = pygame.image.load(image_path).convert_alpha()
                self.rect = self.image.get_rect(topleft = position)
            
            def draw(self, window):
                window.blit(self.image, self.rect)
                
            def is_pressed(self):
                mouse_pos = pygame.mouse.get_pos()
                mouse_pressed = pygame.mouse.get_pressed()[0]
                
                if self.rect.collidepoint(mouse_pos):
                    if mouse_pressed:
                        return True
                    
                return False

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
    
    run = True
    while run:
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
                    selected_character_index = index
                    
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
            game == 1
            break
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #closing game window with ESC
                        run = False

        pygame.display.update()
    return game