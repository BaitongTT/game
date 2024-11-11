import pygame
from game_page_2 import selected_character_index,character,HealthBar
pygame.init()

#framerate
clock = pygame.time.Clock()
FPS = 70

#define colours
RED = (255,0,0)
GREEN = (0,255,0)
BLACK =(0,0,0)
WHITE = (255,255,255)

#set display
pygame.display.set_caption('Trick or Treat' )
screen = pygame.display.set_mode((720, 400))
width, length = screen.get_size() #get the windows size
#print(width, length) to get 1536, 864

#keyboard control
movetothe_left = False
movetothe_right = False


class character(pygame.sprite.Sprite):
    def __init__(self,x, y,image_path , speed,ammo,enemy=None):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.char_1 = pygame.image.load(image_path).convert_alpha()
        self.char_1_rect = self.char_1.get_rect()
        self.char_1_rect.center = (x, y)
        self.health = 100
        self.max_health = 100
        self.reduce_blood = 0
        self.ammo = ammo
        self.start_ammo = ammo
        self.enemy = enemy
        self.start_enemy = enemy
        
        # properties for jumping
        self.jumping = False
        self.vertical_velocity = 0
        self.gravity = 0.5
        self.jump_force = -12
        self.ground_y = 305
        self.on_ground = False
        self.blocked = False
        self.on_platform = False
    
    def move(self, movetothe_left, movetothe_right,dirt_blocks):
        self.old_x = self.char_1_rect.x
        self.old_y = self.char_1_rect.y
        change_x = 0
        if not self.blocked or self.jumping:
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
        self.blocked = False

        
        for block in dirt_blocks: # Check for collisions with blocks
            if self.char_1_rect.colliderect(block.rect):
                if change_x > 0:  # Moving right
                    self.char_1_rect.right = block.rect.left
                elif change_x < 0:  # Moving left
                    self.char_1_rect.left = block.rect.right
                self.blocked = True
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
                        self.on_platform = True
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
            self.on_ground = False
            self.on_platform = False

    def draw(self):
        # false part is used for fliping to not be upside down
        screen.blit(pygame.transform.flip(self.char_1,self.flip, False), self.char_1_rect)

# sprite groups
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
item_boxs_group = pygame.sprite.Group()

'''''
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
'''''''''
#player
reduce_blood_value = 100  
character_images = ["Image/character_1.png","Image/character_2.png","Image/character_3.png"]
player = character(55, 305, character_images[selected_character_index], 2,reduce_blood_value)#,enemy)

# Boss class
class ghost_boss(pygame.sprite.Sprite):
    def __init__(self, x, y,move_range=200):
        super().__init__()
        self.image = pygame.image.load("Image/ghost_1.png")
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.rect = self.image.get_rect(center=(x, y))
        self.health = 1000  
        self.max_health = 1000
        self.shoot_timer = 0
        self.shoot_interval = 120
        
        # Walking properties
        self.move_direction = 1  
        self.move_speed = 2  
        self.start_x = x  
        self.move_range = move_range  

    def update(self):
       # Move the boss within the defined range
        self.rect.x += self.move_speed * self.move_direction
        if self.rect.x > self.start_x + self.move_range:
            self.move_direction = -1  # Move left
        elif self.rect.x < self.start_x - self.move_range:
            self.move_direction = 1  # Move right
            
        # Automatic shooting mechanism
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0
            self.shoot_bullet()
        
    def shoot_bullet(self):
        # Boss shoots a bullet towards the player
        direction = -1 if self.rect.centerx > player.char_1_rect.centerx else 1
        boss_bullet = Bullet(self.rect.centerx, self.rect.centery, direction)
        bullet_group.add(boss_bullet)

    def draw(self):
        screen.blit(self.image, self.rect)
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 10, 120, 10))
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 10, 120 * ratio, 10))

# Initialize boss
boss = ghost_boss(500, 250,move_range=200)  
all_sprites.add(boss)


# ITEMS
class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        super().__init__()  
        self.item_type = item_type
        self.x = x
        self.y = y
        item_images = {
            'Health': 'Image/item_3.png',
            'Reduce_blood': 'Image/item_4.png'
        }  
        if self.item_type in item_images:
            self.image = pygame.image.load(item_images[self.item_type])
        self.image = pygame.transform.scale(self.image, (40, 40))  
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
# temp - create item boxes
health_item  = ItemBox('Health',100, 322)
reduce_blood_item = ItemBox('Reduce_blood',400, 322)
item_boxs_group.add(health_item,reduce_blood_item)

# HealthBar
class HealthBar():
    def __init__(self,x,y,health,max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
    def draw(self,health):
        self.health = health
        ratio = self.health/self.max_health
        pygame.draw.rect(screen,BLACK,(self.x-2,self.y-2,150,20))
        pygame.draw.rect(screen,RED,(self.x,self.y,150,20))
        pygame.draw.rect(screen,GREEN,(self.x,self.y,150*ratio,20))
health_bar = HealthBar(10,10,player.health,player.health)        

#define font
font =pygame.font.SysFont('Futura',20)

def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))


def load_and_scale_image(path, scale):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, (image.get_width() // scale, image.get_height() // scale))

background3 = load_and_scale_image("Image/background_3.png", 1).convert()

#BLOCKS  
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
'''''
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
'''''

#the floor section
dirt_blocks = pygame.sprite.Group()
for i in range(0, 11000, 71):  # start, how long, space (dirt = 40, lava = 71)
    #block = DirtBlock(i, 361, 9)
    block = LavaBlock(i, 361, 9)
    dirt_blocks.add(block)

#blocks for the second session
def create_blocks_2(start_x, y_pos, count): 
    for step in range(count):
        x_position = start_x + (step * 40)
        block = DirtBlock_2(x_position, y_pos, 9)
        dirt_blocks.add(block)
        
#items
'''''
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
'''
#y = 361(first(floor)), 300(second), 240(third), 180(forth)
#the last number is number of blocks
#the first 9000 blocks is the first session
#the second 9000 blocks is the second session
#the last 500 blocks is the end

create_blocks_2(0, 361, 15   )
#create_item_3(300, 298, 1) #item_3  
create_blocks_2(650 , 300, 5)
create_blocks_2(900, 240, 6)
create_blocks_2(1200, 180, 15)
create_blocks_2(1850, 300, 4)
create_blocks_2(2100, 361, 6)
create_blocks_2(2400, 300, 5)
create_blocks_2(2700, 240, 6)
create_blocks_2(3000, 180, 6)
create_blocks_2(3350, 180, 7)
create_blocks_2(3700, 300, 6)
create_blocks_2(4000, 240, 5)
create_blocks_2(4300, 300, 6)
create_blocks_2(4600, 361, 13)
#create_item_4(4900, 298, 1) #item_4
create_blocks_2(5240, 300, 7)
create_blocks_2(5600, 240, 8)
create_blocks_2(6000, 180, 5)
create_blocks_2(6320, 180, 12)
create_blocks_2(6900, 240, 6)
create_blocks_2(7300, 300, 10)
create_blocks_2(7780, 361, 8)
#create_item_4(7880, 298, 1) #item_4
create_blocks_2(8200, 300, 8)
create_blocks_2(8620, 240, 8)
create_blocks_2(9000, 180, 15)
create_blocks_2(9700, 361, 50)
  
#moving objects
speed = 4
scroll_x = 0 
end_of_level_x = 11000 
level_next = False
def move_objects_for_right(speed, move):
    global scroll_x,level_next
    if scroll_x >= end_of_level_x - width:
        if player.char_1_rect.left > width:
            level_next = True
            return True
    if move and scroll_x < end_of_level_x - width:
        scroll_x += speed 
        for block in dirt_blocks:
            block.rect.x -= speed
        return False

run = True
while run:
    clock.tick(FPS)
    screen.fill((0,0,0))
    screen.blit(background3, (0, 0))
    player.draw()
    #enemy.move()
    #enemy.draw(screen)
    item_boxs_group.update()
    item_boxs_group.draw(screen)
    #show player health
    health_bar.draw(player.health)
    #show ammo
    draw_text(f"AMMO :",font,WHITE,10,35)
    #show enemy
    draw_text(f"ENEMY :",font,WHITE,10,50)
    '''
    for x in range(player.ammo):
        screen.blit((90+(x*10),40))
    '''

    #BULLETS
    bullet_group.update()
    bullet_group.draw(screen)

    player.update_jump(dirt_blocks)
    player.move(movetothe_left, movetothe_right,dirt_blocks)
    dirt_blocks.draw(screen)
    move_objects_for_right(speed, movetothe_right)
    
    # Check for collision between player bullets and boss
    for bullet in bullet_group:
        if boss.rect.colliderect(bullet.rect):
            boss.health -= 10  # Decrease boss health when hit by a bullet
            bullet.kill()  # Remove bullet upon collision
            
    # End game if boss health reaches 0
    if boss.health <= 0:
        level_next = True  # Trigger level end or boss defeated state

    # Draw boss
    boss.update()
    boss.draw()
    
    if level_next == True:
        pass

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