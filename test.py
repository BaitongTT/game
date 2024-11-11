import pygame

clock = pygame.time.Clock()
FPS = 70

pygame.display.set_caption('Trick or Treat' )
screen = pygame.display.set_mode((720, 400))
width, length = screen.get_size()


run = True
while run:
    clock.tick(FPS)
    screen.fill((0,0,0))
    
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            run = False
            
    pygame.display.update() #update the screen

pygame.quit()