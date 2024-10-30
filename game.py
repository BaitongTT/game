import pygame
pygame.init()

#framerate
clock = pygame.time.Clock()
FPS = 80

#set display
pygame.display.set_caption('Trick or Treat' )
screen = pygame.display.set_mode((720, 400))
width, length = screen.get_size() #get the windows size
#print(width, length) to get 1536, 864

#keyboard control
movetothe_left = False
movetothe_right = False

class character1(pygame.sprite.Sprite):
    def __init__(self,x, y, scale, speed):
        self.speed = speed
        self.direction = 1
        self.flip = False
        pygame.sprite.Sprite.__init__(self)
        self.char_1 = pygame.image.load("Image/character_1.png").convert_alpha()
        self.char_1_rect = self.char_1.get_rect()
        self.char_1_rect.center = (x, y)
        
        # properties for jumping
        self.jumping = False
        self.vertical_velocity = 0
        self.gravity = 0.5
        self.jump_force = -12
        self.ground_y = 288  
    
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
        self.char_1_rect.x += change_x

        if self.char_1_rect.left < 0:  #dont go out of the left side
            self.char_1_rect.left = 0
        if self.char_1_rect.right > 720:  #dont go out of the right side
            self.char_1_rect.right = 720

    def update_jump(self):
        # update jumping
        if self.jumping or self.char_1_rect.centery < self.ground_y:
            self.char_1_rect.centery += self.vertical_velocity
            self.vertical_velocity += self.gravity
            
            if self.char_1_rect.centery >= self.ground_y:
                self.char_1_rect.centery = self.ground_y
                self.jumping = False
                self.vertical_velocity = 0
                
    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.vertical_velocity = self.jump_force

    def draw(self):
        #false part is used for fliping to not be upside down
        screen.blit(pygame.transform.flip(self.char_1,self.flip, False), self.char_1_rect)

player = character1(55, 288, 5, 2)
enemy = character1(55, 288, 5, 2)

def load_and_scale_image(path, scale):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, (image.get_width() // scale, image.get_height() // scale))

background = load_and_scale_image("Image/background_2.png", 1)

class DirtBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        super().__init__()
        self.image = load_and_scale_image("Image/block.png", 1)
        self.rect = self.image.get_rect(topleft=(x, y))

'''class LavaBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_and_scale_image(" ", 1)  
        self.rect = self.image.get_rect(topleft=(x, y))'''

# Create a group for dirt blocks
dirt_blocks = pygame.sprite.Group()

# Add multiple dirt blocks to the group
for i in range(0, 9000, 40):  # start, how long, space
    '''if random.random() < 0.2:  #assign percent for create lave blocks
        block = LavaBlock(i, 361)
    else:
        block = DirtBlock(i, 361)
    blocks.add(block)'''
    block = DirtBlock(i, 361, 9)
    dirt_blocks.add(block)

#floating blocks
def create_floating_blocks(start_x, y_pos, count): #y = 290 is the second floor, y = 220 is the third floor
    for step in range(count):
        x_position = start_x + (step * 40)
        block = DirtBlock(x_position, y_pos, 9)
        dirt_blocks.add(block)
create_floating_blocks(300, 290, 6)
create_floating_blocks(1000, 290, 10)
create_floating_blocks(1700, 290, 6)
create_floating_blocks(1950, 220, 9)
create_floating_blocks(2500, 290, 10)
create_floating_blocks(2900, 220, 8)
create_floating_blocks(3220, 150, 15)
create_floating_blocks(4000, 290, 10)
create_floating_blocks(4400, 220, 10)
create_floating_blocks(5000, 290, 6)
create_floating_blocks(5250, 220, 15)
create_floating_blocks(6000, 290, 8)
create_floating_blocks(6320, 220, 3)
create_floating_blocks(6450, 150, 15)
create_floating_blocks(7100, 220, 5)
create_floating_blocks(7350, 150, 8)
create_floating_blocks(7700, 220, 5)
create_floating_blocks(8000, 290, 15)

#moving objects
speed = 5
def move_objects_for_right(speed, move):
    if move:
        for block in dirt_blocks:
            block.rect.x -= speed

run = True
while run:
    clock.tick(FPS)
    screen.blit(background, (0,0))
    player.draw()
    enemy.draw()
    player.update_jump()
    player.move(movetothe_left, movetothe_right)
    dirt_blocks.draw(screen)
    move_objects_for_right(speed, movetothe_right)

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

        #(released)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                movetothe_left = False
            if event.key == pygame.K_RIGHT:
                movetothe_right = False

    pygame.display.update() #update the screen

pygame.quit()