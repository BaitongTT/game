import pygame
pygame.init()

#framerate
clock = pygame.time.Clock()
FPS = 70

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
        
        # properties for jumping
        self.jumping = False
        self.vertical_velocity = 0
        self.gravity = 0.5
        self.jump_force = -12
        self.ground_y = 305  
        self.old_x = self.char_1_rect.x
        self.old_y = self.char_1_rect.y
        self.on_ground = False
    
    def move(self, movetothe_left, movetothe_right,dirt_blocks):
        self.old_x = self.char_1_rect.x
        self.old_y = self.char_1_rect.y
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
        self.on_ground = False
        self.vertical_velocity += self.gravity
        self.char_1_rect.y += self.vertical_velocity
        # update jumping
                
        for block in dirt_blocks: # Check for vertical collisions with blocks
                if self.char_1_rect.colliderect(block.rect):
                    if self.vertical_velocity > 0:
                        self.char_1_rect.bottom = block.rect.top
                        self.on_ground = True
                        self.jumping = False
                        self.vertical_velocity = 0
                    elif self.vertical_velocity < 0:
                        self.char_1_rect.top = block.rect.bottom
                        self.vertical_velocity = 0
                        
        if self.char_1_rect.centery >= self.ground_y:
                    self.char_1_rect.centery = self.ground_y
                    self.on_ground = True
                    self.jumping = False
                    self.vertical_velocity = 0
    def jump(self):
        if self.on_ground and not self.jumping:
            self.jumping = True
            self.vertical_velocity = self.jump_force
            self.on_ground = True

    def draw(self):
        # false part is used for fliping to not be upside down
        screen.blit(pygame.transform.flip(self.char_1,self.flip, False), self.char_1_rect)

# sprite groups
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

player = character(55, 305, 5, 2)

# Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self,x, y, scale, speed):
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.move_counter = 0
        self.alive = True
        pygame.sprite.Sprite.__init__(self)
        self.enemy_1 = pygame.image.load("Image/ghost_2.png").convert_alpha()
        self.enemy_1_rect = self.enemy_1.get_rect()
        self.enemy_1_rect.center = (x, y)
        
    def draw(self):
        #false part is used for fliping to not be upside down
        screen.blit(pygame.transform.flip(self.enemy_1,self.flip, False), self.enemy_1_rect)

    # The enemy walks around
    def ai(self):
        if self.alive and player.alive:
            if self.direction == 1 :
                ai_movetothe_right = True
            else :
                ai_movetothe_right = False
            ai_movetothe_left = not ai_movetothe_right
            self.move(ai_movetothe_left,ai_movetothe_right)
            self.update_action(1)
            self.move_counter += 1
            if self.move_counter > 40 :
                self.direction *= -1
                self.move_counter *= -1

enemy_1 = Enemy(640, 275, 5, 2)
enemy_2 = Enemy(535, 275, 5, 2)
enemy_group.add(enemy_1)
enemy_group.add(enemy_2)

class ItemBox(pygame.sprite.Sprite):
    def __init__(self,item_type,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + 40//2,y + (40-self.image.get_height()))






def load_and_scale_image(path, scale):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, (image.get_width() // scale, image.get_height() // scale))

background2 = load_and_scale_image("Image/background_2.png", 1).convert()
background3 = load_and_scale_image("Image/background_3.png", 1).convert()

#BLOCKS
class DirtBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        super().__init__()
        self.image = load_and_scale_image("Image/block.png", 1)
        self.rect = self.image.get_rect(topleft=(x, y))

class DirtBlock_2(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        super().__init__()
        self.image = load_and_scale_image("Image/block_2.png", 1)
        self.rect = self.image.get_rect(topleft=(x, y))

class LavaBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        super().__init__()
        self.image = load_and_scale_image("Image/lava.png", 1)  
        self.rect = self.image.get_rect(topleft=(x, y))
    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Image/candy.png")
        self.image = pygame.transform.scale(self.image, (25, 25)) #size of the bullets
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7  
        self.direction = direction  

    def update(self):
        # Move the bullet left or right depending on direction
        self.rect.x += self.speed * self.direction

        # Remove the bullet if it goes off the screen
        if self.rect.right < 0 or self.rect.left > 720:
            self.kill()

#ITEMS
class Item_1(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        super().__init__()
        self.image = load_and_scale_image("Image/item_1.png", 1)  
        self.rect = self.image.get_rect(topleft=(x, y))

class Item_2(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        super().__init__()
        self.image = load_and_scale_image("Image/item_2.png", 1)  
        self.rect = self.image.get_rect(topleft=(x, y))

class Item_3(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        super().__init__()
        self.image = load_and_scale_image("Image/item_3.png", 1)  
        self.rect = self.image.get_rect(topleft=(x, y))

class Item_4(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        super().__init__()
        self.image = load_and_scale_image("Image/item_4.png", 1)  
        self.rect = self.image.get_rect(topleft=(x, y))

#the floor section
dirt_blocks = pygame.sprite.Group()
for i in range(0, 18500, 71):  # start, how long, space (dirt = 40, lava = 71)
    #block = DirtBlock(i, 361, 9)
    block = LavaBlock(i, 361, 9)
    dirt_blocks.add(block)

#blocks for the frist session
def create_blocks_1(start_x, y_pos, count): 
    for step in range(count):
        x_position = start_x + (step * 40)
        block = DirtBlock(x_position, y_pos, 9)
        dirt_blocks.add(block)

#blocks for the second session
def create_blocks_2(start_x, y_pos, count): 
    for step in range(count):
        x_position = start_x + (step * 40)
        block = DirtBlock_2(x_position, y_pos, 9)
        dirt_blocks.add(block)
        
#items
def create_item_1(start_x, y_pos, count): 
    for step in range(count):
        x_position = start_x + (step * 40)
        item = Item_1(x_position, y_pos, 9)
        dirt_blocks.add(item)

def create_item_2(start_x, y_pos, count): 
    for step in range(count):
        x_position = start_x + (step * 40)
        item = Item_2(x_position, y_pos, 9)
        dirt_blocks.add(item)

def create_item_3(start_x, y_pos, count): 
    for step in range(count):
        x_position = start_x + (step * 40)
        item = Item_3(x_position, y_pos, 9)
        dirt_blocks.add(item)

def create_item_4(start_x, y_pos, count): 
    for step in range(count):
        x_position = start_x + (step * 40)
        item = Item_4(x_position, y_pos, 9)
        dirt_blocks.add(item)

#y = 361(first(floor)), 300(second), 240(third), 180(forth)
#the last number is number of blocks
#the first 9000 blocks is the first session
#the second 9000 blocks is the second session
#the last 500 blocks is the end
create_blocks_1(0, 361, 6)
create_blocks_1(300, 300, 6)
create_blocks_1(540, 240, 5)
create_blocks_1(780, 361, 12)
create_item_4(1140, 298, 1) #item_4
create_blocks_1(1300, 300, 10)
create_blocks_1(1840, 240, 14)
create_blocks_1(2500, 300, 10)
create_blocks_1(2900, 240, 8)
create_blocks_1(3220, 180, 15)
create_blocks_1(4000, 300, 10)
create_blocks_1(4400, 240, 9)
create_blocks_1(4800, 361, 6)
create_item_1(4960, 298, 1) #item_1
create_blocks_1(5040, 300, 5)
create_blocks_1(5240, 240, 15)
create_blocks_1(6000, 300, 8)
create_blocks_1(6320, 240, 3)
create_blocks_1(6440, 180, 15)
create_blocks_1(7040, 240, 8)
create_item_2(7300, 177, 1) #item_2
create_blocks_1(7360, 180, 8)
create_blocks_1(7680, 240, 6)
create_blocks_1(7920, 300, 15)
create_blocks_1(8520, 361, 12)
#end of first session

create_blocks_2(9000, 361, 5)
create_item_3(9120, 298, 1) #item_3
create_blocks_2(9200, 300, 6)
create_blocks_2(9440, 240, 4)
create_blocks_2(9600, 300, 8)
create_blocks_2(10000, 240, 8)
create_blocks_2(10320, 180, 6)
create_blocks_2(10560, 240, 10)
create_blocks_2(10960, 180, 14)
create_blocks_2(11560, 361, 5)
create_blocks_2(11760, 300, 5)
create_blocks_2(11960, 240, 15)
create_blocks_2(12560, 300, 5)
create_blocks_2(12760, 361, 10)
create_item_1(13080, 298, 1) #item_1
create_blocks_2(13200, 300, 8)
create_blocks_2(13520, 240, 8)
create_blocks_2(13840, 180, 15)
create_blocks_2(14440, 240, 5)
create_blocks_2(14640, 300, 10)
create_blocks_2(15040, 361, 15)
create_item_4(15440, 298, 1) #item_4
create_blocks_2(15680, 300, 8)
create_blocks_2(16000, 240, 8)
create_blocks_2(16320, 180, 20)
create_blocks_2(17120, 240, 6)
create_blocks_2(17480, 240, 6)
create_blocks_2(17720, 300, 9)
create_blocks_2(18080, 361, 30)

#moving objects
speed = 4
scroll_x = 0 
def move_objects_for_right(speed, move):
    if move:
        for block in dirt_blocks:
            block.rect.x -= speed

run = True
while run:
    clock.tick(FPS)
    screen.fill((0,0,0))
    if movetothe_right:
        move_objects_for_right(speed, movetothe_right)
        scroll_x += speed
    if player.char_1_rect.x < 9000:
        screen.blit(background2, (0, 0))
    else:
        screen.blit(background3, (0, 0))
    player.draw()
    for enemy in enemy_group :
        enemy.draw()
        '''enemy.ai()'''

    #BULLETS
    bullet_group.update()
    bullet_group.draw(screen)

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
            if event.key == pygame.K_SPACE:
                # Spawn bullet based on character's position and direction
                #.right (spawn at the right of the player)
                #.centery (spawn at the mid of the player)
                bullet = Bullet(player.char_1_rect.right, player.char_1_rect.centery, player.direction)
                bullet_group.add(bullet)

        #(released)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                movetothe_left = False
            if event.key == pygame.K_RIGHT:
                movetothe_right = False

    pygame.display.update() #update the screen

pygame.quit()