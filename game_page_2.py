import pygame
import Button
pygame.init()

#framerate
clock = pygame.time.Clock()
FPS = 80

pygame.display.set_caption('Trick or Treat' )
screen = pygame.display.set_mode((720, 400))
width, length = screen.get_size() #get the windows size
#print(width, length) to get 1536, 864
screen.fill((0, 0, 0))

#button function
class Button:
    def __init__(self, image_path, position, scale=1.0):
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            if scale != 1.0:
                original_size = self.image.get_size()
                new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
                self.image = pygame.transform.scale(self.image, new_size)
            self.rect = self.image.get_rect(topleft=position)
        except pygame.error as e:
            print(f"Error loading image {image_path}: {e}")
            # Create a default surface if image loading fails
            self.image = pygame.Surface((100, 50))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(topleft=position)

    def draw(self, window):
        window.blit(self.image, self.rect)
    
    def is_pressed(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        return self.rect.collidepoint(mouse_pos) and mouse_pressed

# Load images with error handling
def load_image(path):
    try:
        return pygame.image.load(path).convert_alpha()
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")
        # Create a colored surface as placeholder
        surface = pygame.Surface((720, 400))
        surface.fill((100, 100, 100))
        return surface

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
button_back = Button("Image/button_back.png",(300,300 ))

# variable
button_value = False
selected_character = None
character_1_value = False
character_2_value = False
character_3_value = False
game_state = False


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

    elif button_value == True:
        screen.blit(select_characters, (0, 0))
        character_1.draw(screen)
        character_2.draw(screen)
        character_3.draw(screen)
        
        if character_1.is_pressed():
            selected_character = 1
            game_state = True
        elif character_2.is_pressed():
            selected_character = 2
            game_state = True
        elif character_3.is_pressed():
            selected_character = 3
            game_state = True
    
    elif game_state == True:
        if selected_character == 1:
            screen.blit(background_character_1, (0, 0))
        elif selected_character == 2:
            screen.blit(background_character_2, (0, 0))
        elif selected_character == 3:
            screen.blit(background_character_3, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    pygame.display.flip()
pygame.quit()