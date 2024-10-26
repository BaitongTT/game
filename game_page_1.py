import pygame
import Button
pygame.init()

#framerate
clock = pygame.time.Clock()
FPS = 140

pygame.display.set_caption('Trick or Treat' )
screen = pygame.display.set_mode((720, 400))
width, length = screen.get_size() #get the windows size
#print(width, length) to get 1536, 864
screen.fill((0, 0, 0))

# สร้างฟังค์ชันการกด
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
button_start = Button("Image/button_start.png" ,(300,300))  #Button เป็นการกำหนดว่ารูปนี้คือปุ่ม
button_howtoplay= Button("Image/button_howtoplay.png",(0,250))


#game loop
run = True
while run:
    clock.tick(FPS)
    ##Startgame
    screen.blit(background_start,(0,0))
    button_start.draw(screen)
    #button start
    if button_start.is_pressed():
        print("111")
        
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    pygame.display.update()
pygame.quit()
