import pygame

screen = pygame.display.set_mode((720, 400))
width, length = screen.get_size()

#define colours
RED = (255,0,0)
GREEN = (0,255,0)
BLACK =(0,0,0)
WHITE = (255,255,255)

speed = 4
scroll_x = 0 
end_of_level_x = 9110   
level_next = False

health_box_img = pygame.image.load("Image/item_3.png").convert_alpha()
reduce_blood_box_img = pygame.image.load("Image/item_4.png").convert_alpha()
item_boxes = { 
    'Health': health_box_img,
    'Reduce_blood' : reduce_blood_box_img
}

# sprite groups
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
item_box_group_health_item = pygame.sprite.Group()
item_box_group_reduce_blood_item = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
dirt_blocks = pygame.sprite.Group()

class button:
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

            
def load_and_scale_image(path, scale):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, (image.get_width() // scale, image.get_height() // scale))

class character(pygame.sprite.Sprite):
    def __init__(self,x, y,image_path,speed,ammo,enemy=None):
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
        self.x_vel = 0
       
        # properties for jumping
        self.jumping = False
        self.vertical_velocity = 0
        self.gravity = 0.5
        self.jump_force = -12
        self.ground_y = 305
        self.on_ground = False
        self.blocked = False
        self.on_platform = False
    
    def move(self, movetothe_left, movetothe_right,dirt_blocks,scroll_x, end_of_level_x):
        self.old_x = self.char_1_rect.x
        self.old_y = self.char_1_rect.y
        self.x_vel = 0
        if not self.blocked or self.jumping:
            if (movetothe_left):
                self.x_vel = -self.speed
                self.flip = True
                self.direction = -1
            if (movetothe_right):
                self.x_vel = self.speed
                self.flip = False
                self.direction = 1
            else:
                self.x_vel = 0
                self.rect.x += self.x_vel

        #update position
        self.char_1_rect.x += self.x_vel
        self.blocked = False


        for block in dirt_blocks: # Check for collisions with blocks
            if self.char_1_rect.colliderect(block.rect):
                if self.x_vel > 0:  # Moving right
                    self.char_1_rect.right = block.rect.left
                elif self.x_vel < 0:  # Moving left
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

    def draw(self,screen):
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
        
class ghost(pygame.sprite.Sprite):
    def __init__(self, x_position, y_position, move_range=400,image_ghost="Image/ghost_2.png"
                 ,image_bullet="Image/action_ghost_2.png",health=150):
        super().__init__()
        self.original_image = pygame.image.load(image_ghost).convert_alpha()
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
        self.health = health  
        self.max_health = health
        self.shoot_timer = 0 
        self.shoot_interval = 120
        self.bullets = pygame.sprite.Group()  # Create a group of bullets inside
        self.bullet_speed = 7
        self.bullet_image = pygame.image.load(image_bullet).convert_alpha()
        self.bullet_image = pygame.transform.scale(self.bullet_image, (25, 25))
        
        # Walking properties
        self.move_speed = 2
        self.facing_left = False

    def update(self, scroll_x,player):
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
            character.char_1_rect.centerx)  
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

    enemy = ghost(x_position, y_position, move_range)
    enemy_group.add(enemy)
    return enemy

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
            
#blocks for the frist session
def create_blocks_1(start_x, y_pos, count): 
    for step in range(count):
        x_position = start_x + (step * 40)
        block = DirtBlock(x_position, y_pos, 9)
        dirt_blocks.add(block)
        
# ITEMS
class ItemBox(pygame.sprite.Sprite):
    def __init__(self,item_type,x,y,PLAYER):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.PLAYER = PLAYER
        self.world_x = x
        self.world_y = y
        self.rect.topleft = (self.world_x, self.world_y)

    def update(self,scroll_x):
        self.rect.x = self.world_x-scroll_x
    #check if the player has picked up the box
        if self.rect.colliderect(self.PLAYER.char_1_rect):
            #check what kind of box it was
            if self.item_type == 'Health' :
                self.PLAYER.health += 25
                if self.PLAYER.health > self.PLAYER.max_health :
                    self.PLAYER.health = self.PLAYER.max_health
            elif self.item_type == 'Reduce_blood' :
                self.PLAYER.health -=15
                if self.PLAYER.health < 0:
                    self.PLAYER.health = 0 
            self.kill()

def create_item_health_item(x, y):
    health_item  = ItemBox('Health',x,y)
    item_box_group_health_item.add(health_item)    
    return health_item

def create_item_reduce_blood_item(x, y):
    reduce_blood_item  = ItemBox('Reduce_blood',x,y)
    item_box_group_reduce_blood_item.add(reduce_blood_item)    
    return reduce_blood_item


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

def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))
    
def move_objects_for_right1(speed, move):
    global scroll_x,level_next
    if scroll_x >= end_of_level_x - width:
        if character.char_1_rect.left > width:
            level_next = True
            return True
    if move and scroll_x < end_of_level_x - width:
        scroll_x += speed 
        for block in dirt_blocks:
            block.rect.x -= speed
        return False

def move_objects_for_right(player, offset_x, width, end_of_level_x):
    scroll_area_width = 200
    
    if offset_x >= end_of_level_x - width:
        if player.rect.left > width:
            return True, True  # return (should_scroll, level_complete)
            
    if ((player.rect.right - offset_x >= width - scroll_area_width) and player.x_vel > 0) or (
            (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
        return True, False
        
    return False, False