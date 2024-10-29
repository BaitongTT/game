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

# button function
class Button:
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

#load images
background_start = pygame.image.load("Image/background_1.png").convert_alpha()
select_charecters = pygame.image.load("Image/select_charecters.png").convert_alpha()
background_charecter_1 = pygame.image.load("Image/select_1.png").convert_alpha()
background_charecter_2 = pygame.image.load("Image/select_2.png").convert_alpha()
background_charecter_3 = pygame.image.load("Image/select_3.png").convert_alpha()

# set button
button_start = Button("Image/button_start.png" ,(300,300))  #Button เป็นการกำหนดว่ารูปนี้คือปุ่ม
button_howtoplay= Button("Image/button_howtoplay.png",(0,250))

# variable
button_value = False
select_charecters_value = False


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
        screen.blit(select_charecters,(0,0))
        select_charecters_value = True

        
    
        
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    pygame.display.update()
pygame.quit()
