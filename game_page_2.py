import pygame
from game_page_1 import selected_character_index
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
        self.rect = self.char_1.get_rect() 
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
        if scroll_x < end_of_level_x - 720:
            if self.char_1_rect.right > 720: #dont go out of the right side
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
            self.on_ground = False
            self.on_platform = False

    def draw(self):
        # false part is used for fliping to not be upside down
        screen.blit(pygame.transform.flip(self.char_1,self.flip, False), self.char_1_rect)

    def shoot(self):
        # Spawn bullet based on character's position and direction
        #add the player size because i dont want the bullet to come out in the middle of player
        #.centery (spawn at the mid of the player)
        bullet = Bullet(self.char_1_rect.centerx + (0.6 * self.char_1_rect.size[0] * self.direction), 
        self.char_1_rect.centery, self.direction)
        bullet_group.add(bullet)

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False

    def update(self):
        self.check_alive()

# sprite groups
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()

# Enemy
enemy_image = pygame.image.load('Image/ghost_2.png')  
enemy_rect = enemy_image.get_rect()

'''class Enemy:
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
enemy = Enemy(100, 215)'''
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x_position, y_position,move_range=200):
        super().__init__()
        self.original_image = pygame.image.load("Image/ghost_2.png")
        self.original_image = pygame.transform.scale(self.original_image, (150, 150))
        self.image = self.original_image
        self.rect = self.image.get_rect()
       
       # Set initial position
        self.rect.x = x_position
        self.rect.y = y_position
        self.start_x = x_position
        self.start_y = y_position
        self.absolute_x = x_position
       
        self.move_range = move_range
        self.health = 100  
        self.max_health = 100
        self.shoot_timer = 0 
        self.shoot_interval = 120
        self.bullets = pygame.sprite.Group()  # Create a group of bullets inside
        self.bullet_speed = 7
        self.bullet_image = pygame.image.load("Image/action_ghost_2.png").convert_alpha()
        self.bullet_image = pygame.transform.scale(self.bullet_image, (25, 25))
        
        # Walking properties
        self.move_speed = 2
        self.facing_left = False

    def update(self, scroll_x):
        self.rect.x = self.absolute_x - scroll_x
        if -150 <= self.rect.x <= 720:
        # Move within the defined range
            if player.char_1_rect.centerx < self.rect.centerx:  
                if self.rect.x > self.start_x - self.move_range: 
                    self.rect.x -= self.move_speed
                if self.facing_left:
                    self.facing_left = True
                    self.image = pygame.transform.flip(self.original_image, True, False)
                    
            elif player.char_1_rect.centerx > self.rect.centerx:  
                if self.rect.x < self.start_x + self.move_range:
                    self.rect.x += self.move_speed
                if not self.facing_left:
                    self.facing_left = False
                    self.image = self.original_image
            
        # Automatic shooting mechanism
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0
            self.shoot_bullet()
            
        self.update_bullets()
        
    def shoot_bullet(self):
        # Create a new bullet sprite
        bullet = GhostBullet(
            self.rect.centerx,
            self.rect.centery,
            self.bullet_image,
            self.bullet_speed,
            player.char_1_rect.centerx)  
        self.bullets.add(bullet)
        
        # Flip bullet image if boss is facing left
        if self.facing_left:
            bullet.image = pygame.transform.flip(bullet.image, True, False)
        self.bullets.add(bullet)
        
    def update_bullets(self):
        self.bullets.update()
        # Remove bullets that are off screen
        for bullet in self.bullets:
            if bullet.rect.right < 0 or bullet.rect.left > 720:
                bullet.kill()
    
    def draw(self,screen):
        if -150 <= self.rect.x <= 720:
            screen.blit(self.image, self.rect)
            ratio = self.health / self.max_health
            pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 10, 120, 10))
            pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 10, 120 * ratio, 10))
            self.bullets.draw(screen)
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

    '''def move(self):
        # Move in the specified direction
        self.x += self.speed * self.direction
        self.rect.topleft = (self.x, self.y)

        if self.rect.left <= self.x_position:  
            self.direction = 1  
            self.rect.left = self.x_position 
        elif self.rect.right >= self.x_position + self.move_range:  
            self.direction = -1  
            self.rect.right = self.x_position + self.move_range'''
            
class GhostBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_image, speed, target_x):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect(center=(x, y))
        self.absolute_x = x 
        self.speed = speed
        # Calculate direction based on target position
        self.direction = -1 if x > target_x else 1

    def update(self):
        self.absolute_x += self.speed * self.direction
        self.rect.x += self.speed * self.direction

def create_ghost(x_position, y_position, move_range):
    #Create a ghost at the specified position
    #x_position: x coordinate in world space
    #y_position: y coordinate
    #move_range: how far the ghost can move left/right from its starting position

    enemy = Enemy(x_position, y_position, move_range)
    enemy_group.add(enemy)
    return enemy

#position of ghosts
create_ghost(780, 213, 480)
create_ghost(1840, 92, 560)
create_ghost(3220, 31, 600)
create_ghost(4000, 151, 400)
create_ghost(5240, 92, 600)
create_ghost(6440, 31, 600)
create_ghost(7920, 151, 600)
create_ghost(8520, 213, 800)

enemy = Enemy(100, 215)

#player
reduce_blood_value = 100   
character_images = ["Image/character_1.png","Image/character_2.png","Image/character_3.png"]
player = character(55, 305, character_images[selected_character_index], 2,reduce_blood_value,enemy)


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
    ''' 
    def update(self):
    #check if the player has picked up the box
        if pygame.sprite.collide_rect(self,player):
            #check what kind of box it was
            if self.item_type == 'Health' :
                player.health += 25
                if player.health > player.max_health :
                    player.health = player.max_health
            elif self.item_type == 'Reduce_blood' :
                player.reduce_blood += 15
            self.kill()
   '''
'''
# pick up boxes
health_box_img = pygame.image.load("Image/item_3.png").convert_alpha()
reduce_blood_box_img = pygame.image.load("Image/item_4.png").convert_alpha()
item_boxes = { 
    'Health': health_box_img,
    'Reduce_blood' : reduce_blood_box_img
}
'''
# temp - create item boxes
health_item1  = ItemBox('Health',200, 320)
health_item2  = ItemBox('Health',300, 320)
reduce_blood_item1 = ItemBox('Reduce_blood',400, 320)
reduce_blood_item2 = ItemBox('Reduce_blood',500, 320)
item_box_group.add(health_item1,health_item2,reduce_blood_item1,reduce_blood_item2)

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

background2 = load_and_scale_image("Image/background_2.png", 1).convert()

#BLOCKS
class DirtBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        super().__init__()
        self.image = load_and_scale_image("Image/block.png", 1)
        self.rect = self.image.get_rect(topleft=(x, y))

class LavaBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        super().__init__()
        self.image = load_and_scale_image("Image/lava.png", 1)  
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect.x = x
        self.rect.y = y
    
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

        #check collision with the ghost
        '''if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                print("hits!")
                self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 50
                    self.kill()'''

#create sprite groups
bullet_group = pygame.sprite.Group()

#ITEMS
'''
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
'''
#the floor section
dirt_blocks = pygame.sprite.Group()
for i in range(0, 9000, 71):  # start, how long, space (dirt = 40, lava = 71)
    #block = DirtBlock(i, 361, 9)
    block = LavaBlock(i, 361, 9)
    dirt_blocks.add(block)

#blocks for the frist session
def create_blocks_1(start_x, y_pos, count): 
    for step in range(count):
        x_position = start_x + (step * 40)
        block = DirtBlock(x_position, y_pos, 9)
        dirt_blocks.add(block)

#items
'''
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
create_blocks_1(0, 361, 6)
create_blocks_1(300, 300, 6)
create_blocks_1(540, 240, 5)
create_blocks_1(780, 361, 12)
#create_item_4(1140, 298, 1) #item_4
create_blocks_1(1300, 300, 10)
create_blocks_1(1840, 240, 14)
create_blocks_1(2500, 300, 10)
create_blocks_1(2900, 240, 8)
create_blocks_1(3220, 180, 15)
create_blocks_1(4000, 300, 10)
create_blocks_1(4400, 240, 9)
create_blocks_1(4800, 361, 6)
create_blocks_1(5040, 300, 5)
create_blocks_1(5240, 240, 15)
create_blocks_1(6000, 300, 8)
create_blocks_1(6320, 240, 3)
create_blocks_1(6440, 180, 15)
create_blocks_1(7040, 240, 8)
#create_item_2(7300, 177, 1) #item_2
create_blocks_1(7360, 180, 8)
create_blocks_1(7680, 240, 6)
create_blocks_1(7920, 300, 15)
create_blocks_1(8520, 361, 20)
#end of first session

#moving objects
speed = 4
scroll_x = 0 
end_of_level_x = 9110   
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
    screen.blit(background2, (0, 0))
    player.draw()
    #enemy.move()
    enemy.draw(screen)
    item_box_group.update()
    item_box_group.draw(screen)
    #show player health
    health_bar.draw(player.health)
    #show enemy
    draw_text(f"ENEMY :",font,WHITE,10,35)
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
    player.update()

    if level_next == True:
        break
    for enemy in enemy_group:
        enemy.update(scroll_x)
        enemy.draw(screen)
        if -150 <= enemy.rect.x <= 720:
            for bullet in bullet_group:
                if enemy.rect.colliderect(bullet.rect):
                    enemy.take_damage(10)
                    bullet.kill()
            
            # Check for collisions between boss bullets and players.
            for bullet in enemy.bullets:
                if bullet.rect.colliderect(player.char_1_rect):
                    player.health -= 10  
                    bullet.kill()
        # End game if boss health reaches 0
        if enemy.health <= 0:
            enemy.kill()
    
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
                player.shoot()

        #(released)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                movetothe_left = False
            if event.key == pygame.K_RIGHT:
                movetothe_right = False

    pygame.display.update() #update the screen

pygame.quit()