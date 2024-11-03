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

class character(pygame.sprite.Sprite):
    def __init__(self,x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.char_1 = pygame.image.load("Image/character_1.png").convert_alpha()
        self.char_1_rect = self.char_1.get_rect()
        self.char_1_rect.center = (x, y)
        self.move_counter = 0
        
        # properties for jumping
        self.jumping = False
        self.vertical_velocity = 0
        self.gravity = 0.5
        self.jump_force = -12
        self.ground_y = 288  
        self.old_x = self.char_1_rect.x
        self.old_y = self.char_1_rect.y
    
    def move(self, movetothe_left, movetothe_right,dirt_blocks):
        
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
        
        for block in dirt_blocks: # Check for collisions with blocks
            if self.char_1_rect.colliderect(block.rect):
                self.char_1_rect.x = self.old_x
                break

        if self.char_1_rect.left < 0:  #dont go out of the left side
            self.char_1_rect.left = 0
        if self.char_1_rect.right > 720:  #dont go out of the right side
            self.char_1_rect.right = 720

    def update_jump(self,dirt_blocks):
        # update jumping
        if self.jumping or self.char_1_rect.centery < self.ground_y:
            self.char_1_rect.centery += self.vertical_velocity
            self.vertical_velocity += self.gravity
                
            for block in dirt_blocks: # Check for vertical collisions with blocks
                if self.char_1_rect.colliderect(block.rect):
                    if self.vertical_velocity > 0:
                        self.char_1_rect.bottom = block.rect.top
                        self.jumping = False
                        self.vertical_velocity = 0
                    elif self.vertical_velocity < 0:
                        self.char_1_rect.top = block.rect.bottom
                        self.vertical_velocity = 0
                        break
                if self.char_1_rect.centery >= self.ground_y:
                    self.char_1_rect.centery = self.ground_y
                    self.jumping = False
                    self.vertical_velocity = 0
    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.vertical_velocity = self.jump_force

    def draw(self):
        # false part is used for fliping to not be upside down
        screen.blit(pygame.transform.flip(self.char_1,self.flip, False), self.char_1_rect)

# sprite groups
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

player = character(55, 288, 5, 2)

# Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self,x, y, scale, speed):
        self.speed = speed
        self.direction = 1
        self.flip = False
        pygame.sprite.Sprite.__init__(self)
        self.enemy_1 = pygame.image.load("Image/ghost_2.png").convert_alpha()
        self.enemy_1_rect = self.enemy_1.get_rect()
        self.enemy_1_rect.center = (x, y)
    def draw(self):
        #false part is used for fliping to not be upside down
        screen.blit(pygame.transform.flip(self.enemy_1,self.flip, False), self.enemy_1_rect)

enemy_1 = Enemy(640, 275, 5, 2)
enemy_2 = Enemy(535, 275, 5, 2)
enemy_group.add(enemy_1)
enemy_group.add(enemy_2)

# The enemy walks around
def ai(self):
    if self.alive and player.alive:
        if self.direction == 1 :
            ai_movetothe_right = True
        else :
            ai_movetothe_right = False
        ai_movetothe_left = not ai_movetothe_right
        self.move(ai_movetothe_left,ai_movetothe_right)
        self.move_counter += 1
        if self.move_counter > block :
            self.direction *= -1
            self.move_counter *= -1


def load_and_scale_image(path, scale):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, (image.get_width() // scale, image.get_height() // scale))

background2 = load_and_scale_image("Image/background_2.png", 1)
'''background3 = load_and_scale_image("", 1)'''

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
create_floating_blocks(300, 300, 6)
create_floating_blocks(1000, 300, 10)
create_floating_blocks(1700, 300, 6)
create_floating_blocks(1950, 240, 9)
create_floating_blocks(2500, 300, 10)
create_floating_blocks(2900, 240, 8)
create_floating_blocks(3220, 180, 15)
create_floating_blocks(4000, 300, 10)
create_floating_blocks(4400, 240, 10)
create_floating_blocks(5000, 300, 6)
create_floating_blocks(5250, 240, 15)
create_floating_blocks(6000, 300, 8)
create_floating_blocks(6320, 220, 3)
create_floating_blocks(6450, 180, 15)
create_floating_blocks(7100, 240, 5)
create_floating_blocks(7350, 180, 8)
create_floating_blocks(7700, 240, 5)
create_floating_blocks(8000, 300, 15)

#moving objects
speed = 5
def move_objects_for_right(speed, move):
    if move:
        for block in dirt_blocks:
            block.rect.x -= speed

run = True
while run:
    clock.tick(FPS)
    screen.blit(background2, (0,0))
    '''screen.blit(background3, (9000,0))'''
    player.draw()
    for enemy in enemy_group :
        enemy.draw()
        '''enemy.ai()'''
    player.update_jump(dirt_blocks)
    player.move(movetothe_left, movetothe_right,dirt_blocks)
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