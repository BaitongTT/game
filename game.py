import pygame
pygame.init()

#framerate
clock = pygame.time.Clock()
FPS = 140

screen = pygame.display.set_mode((720, 400))
width, length = screen.get_size() #get the windows size
#print(width, length) to get 1536, 864
pygame.display.set_caption('Lawbreakers\' hunters')

screen.fill((0, 0, 0))

#background
scale = 8
background = pygame.image.load("C:\\Users\\ASUS\\Downloads\\background.jpg")
background = pygame.transform.scale(background,(background.get_width() / scale, 
    background.get_height() / scale))
background_rect = background.get_rect()
background_rect.center = ((350, 200))

#dirt
scale = 9
dirt_block = pygame.image.load("C:\\Users\\ASUS\\Downloads\\dirt_block.jpg")
dirt_block = pygame.transform.scale(dirt_block,(dirt_block.get_width() / scale, 
    dirt_block.get_height() / scale))
dirt_block_rect = dirt_block.get_rect()
dirt_block_rect.bottomleft = ((0, 400))

#keyboard control
movetothe_left = False
movetothe_right = False

class character1(pygame.sprite.Sprite):
    def __init__(self,x, y, scale, speed):
        self.speed = speed
        self.direction = 1
        self.flip = False
        pygame.sprite.Sprite.__init__(self)
        char1 = pygame.image.load("C:\\Users\\ASUS\\Downloads\\char1_1.png")
        self.char1 = pygame.transform.scale(char1, (char1.get_width() / scale, 
        char1.get_height() / scale))
        self.char1_rect = self.char1.get_rect()
        self.char1_rect.center = (x, y)

    def move(self, movetothe_left, movetothe_right):
        change_x = 0
        if (movetothe_left):
            change_x = -self.speed
            self.flip = True
            self.direction = -1
        if (movetothe_right):
            change_x = self.speed
            self.flip = False
            self.direction = 1

        #update position
        self.char1_rect.x += change_x

    def draw(self):
        #false part is used for fliping to not be upside down
        screen.blit(pygame.transform.flip(self.char1,self.flip, False), self.char1_rect)

player = character1(60, 277, 5, 2)

run = True
while run:
    clock.tick(FPS)
    screen.blit(background, background_rect)
    screen.blit(dirt_block, dirt_block_rect)
    player.draw()
    player.move(movetothe_left, movetothe_right)

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

        #(released)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                movetothe_left = False
            if event.key == pygame.K_RIGHT:
                movetothe_right = False

    pygame.display.update() #update the screen
pygame.quit()