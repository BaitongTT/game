import pygame
from game_page_1 import selected_character_index
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
    def __init__(self,x, y,image_path , speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.char_1 = pygame.image.load(image_path).convert_alpha()
        self.char_1_rect = self.char_1.get_rect()
        self.char_1_rect.center = (x, y)
        
        # properties for jumping
        self.jumping = False
        self.vertical_velocity = 0
        self.gravity = 0.5
        self.jump_force = -12
        self.ground_y = 305  
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
    
character_images = ["Image/character_1.png","Image/character_2.png","Image/character_3.png"]
player = character(55, 305, character_images[selected_character_index], 2)

# sprite groups
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
item_boxs_group = pygame.sprite.Group()

# Enemy
enemy_image = pygame.image.load('Image/ghost_2.png')  
enemy_rect = enemy_image.get_rect()

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = enemy_image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.speed = 2  # Movement speed
        self.direction = 1  # Direction (1 is right, -1 is left)

    def move(self):
        # Move in the specified direction
        self.x += self.speed * self.direction
        self.rect.topleft = (self.x, self.y)

        if self.rect.left <= 0:  
            self.direction = 1  
            self.rect.left = 0  
        elif self.rect.right >= 720:  
            self.direction = -1  
            self.rect.right = 720
    def draw(self, screen):
        screen.blit(self.image, self.rect)
enemy = Enemy(100, 215) 

'''
class ItemBox(pygame.sprite.Sprite):
    def __init__(self,item_type,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxs[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + 40//2,y + (40-self.image.get_height()))
    def update(self):
        #check if the player has picked up the box
        if pygame.sprite.collide_rect(self,player):
            #check what kind of box it was
            if self.item_type == 'Paint_bucket' :
                player.Paint_bucket += 25
            elif self.item_type == 'Ice' :
                player.Ice += 15
            elif self.item_type == 'Health' :
                player.Health += 3
            elif self.item_type == 'Reduce_blood' :
                player.Reduce_blood += 3
            self.kill()
# pick up boxes
paint_bucket_box_img = pygame.image.load("Image/item_1.png").convert_alpha()
ice_box_img = pygame.image.load("Image/item_2.png").convert_alpha()
health_box_img = pygame.image.load("Image/item_3.png").convert_alpha()
reduce_blood_box_img = pygame.image.load("Image/item_4.png").convert_alpha()
item_boxs = { 
    'Paint_bucket': paint_bucket_box_img,
    'Ice': ice_box_img,
    'Health': health_box_img,
    'Reduce_blood' : reduce_blood_box_img
}

# temp - create item boxes
item_boxs = ItemBox('Paint_bucket',4960, 298,1)
item_boxs_group.add(item_boxs)
item_boxs = ItemBox('Paint_bucket',13080, 298,1)
item_boxs_group.add(item_boxs)
item_boxs = ItemBox('Ice',7300, 177,1)
item_boxs_group.add(item_boxs)
item_boxs = ItemBox('Health',9120, 298,1)
item_boxs_group.add(item_boxs)
item_boxs = ItemBox('Reduce_blood',1140, 298,1)
item_boxs_group.add(item_boxs)
item_boxs = ItemBox('Reduce_blood',15440, 298,1)
item_boxs_group.add(item_boxs)
'''
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
    enemy.move()
    enemy.draw(screen)
    item_boxs_group.update()
    item_boxs_group.draw(screen)

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