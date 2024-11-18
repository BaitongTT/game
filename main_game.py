import pygame
import pygame_button
from pygame import mixer
pygame.init()
mixer.init()

#framerate
clock = pygame.time.Clock()
FPS = 50

pygame.display.set_caption('Trick or Treat' )
screen = pygame.display.set_mode((720, 400))
width, length = screen.get_size() #get the windows size
#print(width, length) to get 1536, 864
screen.fill((0, 0, 0))

#define colours
RED = (255,0,0)
GREEN = (0,255,0)
BLACK =(0,0,0)
WHITE = (255,255,255)

# sprite groups
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemy_group_2 = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
bullet_group_2 = pygame.sprite.Group()
item_box_group_health_item = pygame.sprite.Group()
item_box_group_health_item_2 = pygame.sprite.Group()
item_box_group_reduce_blood_item_2 = pygame.sprite.Group()
boss_group = pygame.sprite.Group()

#load images
background_start = pygame.image.load("Image/background_1.png")
select_characters = pygame.image.load("Image/select_charecter.png")
background_character_1 = pygame.image.load("Image/select_1.png")
background_character_2 = pygame.image.load("Image/select_2.png")
background_character_3 = pygame.image.load("Image/select_3.png")
background2 = pygame.image.load("Image/background_2.png")
background3 = pygame.image.load("Image/background_3.png")
howtoplay = pygame.image.load("Image/howtoplay.png")
gameover = pygame.image.load("Image/gameover.png").convert_alpha()

#load music and sounds
pygame.mixer.music.load("Image/halloween_sound.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer_music.play(-1,0.0,5000)


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

# set button
button_start = button("Image/button_start.png" ,(300,320))  #Button
button_howtoplay= button("Image/button_howtoplay.png",(650,20))
character_1 = button("Image/1_charecter.png",(60,133))
character_2 = button("Image/2_charecter.png",(269,135))
character_3 = button("Image/3_charecter.png",(479,135))
button_back = button("Image/button_back.png",(252,327))
button_play = button("Image/button_play.png",(365,327))
button_play_howtoplay = button("Image/button_play.png",(590,340))
button_newgame = button("Image/newgame.png",(294,280))

# variable
button_value = False
howtoplay_button_value = 0
character_values = [False, False, False]
back_value = False
play_value = False
selected_character_index = 0
gameover_value = False
start = False

#keyboard control
movetothe_left = False
movetothe_right = False
movetothe_left_2 = False
movetothe_right_2 = False

#moving objects
speed = 10
scroll_x = 0 
scroll_x_2 = 0
end_of_level_x = 12400
end_of_level_x_2 = 11000
level_next = False
def move_objects_for_right(speed, move):
    global scroll_x,level_next, player, end_of_level_x
    if scroll_x >= end_of_level_x - width:
        if player.char_1_rect.left >= 580:
            level_next = True
            player.char_1_rect.left = 0
            return True
    if move and scroll_x < end_of_level_x - width:
        #if the player isn't stuck, then the object is moving
        if player.health > 0:
            if player.char_1_rect.x >= 21:  
                scroll_x += speed 

        #condition of dirt blocks
            for block in dirt_blocks:
                if player.char_1_rect.x < 21: #21 is the rect.x starting point of the player
                    pass
                else:
                    block.rect.x -= speed #the objects move to the left
        
        #condition of lava blocks
            for lava in lava_blocks:
                if player.char_1_rect.x < 21: #21 is the rect.x starting point of the player
                    pass
                else:
                    lava.rect.x -= speed
        return False


class character(pygame.sprite.Sprite):
    def __init__(self,x, y,image_path , speed,ammo,enemy=None):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.image_path = pygame.image.load(image_path).convert_alpha()
        self.char_1 = self.image_path 
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
        self.y = y
        self.x = x
        self.enemy_defeated = 0
       
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
        self.change_x = 0
        if not self.blocked or self.jumping:
            if (movetothe_left):
                self.change_x = -self.speed
                self.flip = True
                self.direction = -1
            if (movetothe_right):
                self.change_x = self.speed
                self.flip = False
                self.direction = 1

        #update position
        self.char_1_rect.x += self.change_x
        self.blocked = False

        for block in dirt_blocks: # Check for collisions with blocks
            if self.char_1_rect.colliderect(block.rect):
                if self.change_x > 0:  # Moving right
                    self.char_1_rect.right = block.rect.left
                elif self.change_x < 0:  # Moving left
                    self.char_1_rect.left = block.rect.right
                self.blocked = True
                break

        if self.char_1_rect.left < 0:  #dont go out of the left side
            self.char_1_rect.left = 0
        #240 is the x's position that the player is set.
        #14 is last enemy of first session, then the player can walk off screen
        
        if self.enemy_defeated == 18:
            pass
        else: 
            if self.char_1_rect.right > 240: #dont go out of the left mid
                 self.char_1_rect.right = 240
                 
        for block in dirt_blocks:
            if self.char_1_rect.colliderect(block.rect):
                if self.old_y + self.char_1_rect.height <= block.rect.top:  # Character was above the block
                    self.char_1_rect.bottom = block.rect.top
                    self.on_ground = True
                    self.jumping = False
                    self.vertical_velocity = 0

    def move_2(self, movetothe_left, movetothe_right,dirt_blocks_2):
        self.old_x = self.char_1_rect.x
        self.old_y = self.char_1_rect.y
        self.change_x = 0
        if not self.blocked or self.jumping:
            if (movetothe_left):
                self.change_x = -self.speed
                self.flip = True
                self.direction = -1
            if (movetothe_right):
                self.change_x = self.speed
                self.flip = False
                self.direction = 1

        #update position
        self.char_1_rect.x += self.change_x
        self.blocked = False

        for block in dirt_blocks_2: # Check for collisions with blocks
            if self.char_1_rect.colliderect(block.rect):
                if self.change_x > 0:  # Moving right
                    self.char_1_rect.right = block.rect.left
                elif self.change_x < 0:  # Moving left
                    self.char_1_rect.left = block.rect.right
                self.blocked = True
                break

        if self.char_1_rect.left < 0:  #dont go out of the left side
            self.char_1_rect.left = 0
        #240 is the x's position that the player is set.
        #14 is last enemy of first session, then the player can walk off screen
        if self.enemy_defeated == 18: 
                pass
        else: 
            if self.char_1_rect.right > 240: #dont go out of the left mid
                 self.char_1_rect.right = 240
                 
        for block in dirt_blocks_2:
            if self.char_1_rect.colliderect(block.rect):
                if self.old_y + self.char_1_rect.height <= block.rect.top:  # Character was above the block
                    self.char_1_rect.bottom = block.rect.top
                    self.on_ground = True
                    self.jumping = False
                    self.vertical_velocity = 0
        

    def update_jump(self, dirt_blocks_2):
        self.on_ground = False
        self.vertical_velocity += self.gravity
        self.char_1_rect.y += self.vertical_velocity
        # update jumping
                
        for block in dirt_blocks_2: # Check for vertical collisions with blocks
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
        
class character_next(pygame.sprite.Sprite):
    def __init__(self,x, y,image_path , speed,ammo,enemy=None):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.image_path = pygame.image.load(image_path).convert_alpha()
        self.char_2 = self.image_path 
        self.char_2_rect = self.char_2.get_rect()
        self.rect = self.char_2.get_rect() 
        self.char_2_rect.center = (x, y)
        self.health = 100
        self.max_health = 100
        self.reduce_blood = 0
        self.ammo = ammo
        self.start_ammo = ammo
        self.enemy = enemy
        self.start_enemy = enemy
        self.y = y
        self.x = x
        self.enemy_defeated = 0
       
        # properties for jumping
        self.jumping = False
        self.vertical_velocity = 0
        self.gravity = 0.5
        self.jump_force = -12
        self.ground_y = 305
        self.on_ground = False
        self.blocked = False
        self.on_platform = False
        self.change_x = 0
    
    def move_next_2(self, movetothe_left_2, movetothe_right_2,dirt_blocks_2):
        self.old_x = self.char_2_rect.x
        self.old_y = self.char_2_rect.y
        self.change_x = 0
        if not self.blocked or self.jumping:
            if (movetothe_left_2):
                self.change_x = -self.speed
                self.flip = True
                self.direction = -1
            if (movetothe_right_2):
                self.change_x = self.speed
                self.flip = False
                self.direction = 1

        #update position
        self.char_2_rect.x += self.change_x
        self.blocked = False

        for block in dirt_blocks_2: # Check for collisions with blocks
            if self.char_2_rect.colliderect(block.rect):
                if self.change_x > 0:  # Moving right
                    self.char_2_rect.right = block.rect.left
                elif self.change_x < 0:  # Moving left
                    self.char_2_rect.left = block.rect.right
                self.blocked = True
                break

        if self.char_2_rect.left < 0:  #dont go out of the left side
            self.char_2_rect.left = 0
        #240 is the x's position that the player is set.
        else: 
            if self.char_2_rect.right > 240: #dont go out of the left mid
                 self.char_2_rect.right = 240
                 
        for block in dirt_blocks_2:
            if self.char_2_rect.colliderect(block.rect):
                if self.old_y + self.char_2_rect.height <= block.rect.top:  # Character was above the block
                    self.char_2_rect.bottom = block.rect.top
                    self.on_ground = True
                    self.jumping = False
                    self.vertical_velocity = 0
        

    def update_jump_2(self,dirt_blocks_2):
        self.on_ground = False
        self.vertical_velocity += self.gravity
        self.char_2_rect.y += self.vertical_velocity
        # update jumping
                
        for block in dirt_blocks_2: # Check for vertical collisions with blocks
                if self.char_2_rect.colliderect(block.rect):
                    if self.vertical_velocity > 0:
                        self.char_2_rect.bottom = block.rect.top
                        self.on_ground = True
                        self.jumping = False
                        self.vertical_velocity = 0
                    elif self.vertical_velocity < 0:
                        self.char_2_rect.top = block.rect.bottom
                        self.vertical_velocity = 0
                        
        if self.char_2_rect.centery >= self.ground_y:
                    self.char_2_rect.centery = self.ground_y
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
        screen.blit(pygame.transform.flip(self.char_2,self.flip, False), self.char_2_rect)

    def shoot(self):
        # Spawn bullet based on character's position and direction
        #add the player size because i dont want the bullet to come out in the middle of player
        #.centery (spawn at the mid of the player)
        bullet = Bullet(self.char_2_rect.centerx + (0.6 * self.char_2_rect.size[0] * self.direction), 
        self.char_2_rect.centery, self.direction)
        bullet_group_2.add(bullet)
        
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False

    def update(self,scroll_x_2):
        self.check_alive()
        self.scroll_x_2 = scroll_x_2
        
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x_position, y_position, move_range=400):
        super().__init__()
        self.original_image = pygame.image.load("Image/ghost_2.png")
        self.original_image = pygame.transform.scale(self.original_image, (150, 150))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.speed = 2
        self.direction = 1
       
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
        self.move()
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
    
    def move(self):
        # Move the enemy within the allowed range
        if self.direction == 1:  # Moving right
            self.absolute_x += self.speed
            if self.absolute_x >= (self.start_x + self.move_range):  # Check if it has moved too far right
                self.direction = -1  # Change direction to left
        elif self.direction == -1:  # Moving left
            self.absolute_x -= self.speed
            if self.absolute_x <= (self.start_x - self.move_range):  # Check if it has moved too far left
                self.direction = 1  # Change direction to right
    
    def reset(self):
        self.rect.x = self.initial_x 
        self.rect.y = self.initial_y 
        self.health = self.max_health
        self.bullets.empty()

class Enemy_2(pygame.sprite.Sprite):
    def __init__(self, x_position, y_position, move_range=400):
        super().__init__()
        self.original_image = pygame.image.load("Image/ghost_2.png")
        self.original_image = pygame.transform.scale(self.original_image, (150, 150))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.speed = 2
        self.direction = 1
       
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

    def update(self, scroll_x_2):
        self.rect.x = self.absolute_x - scroll_x_2
        if -150 <= self.rect.x <= 720:
        # Move within the defined range
            if player_2.char_2_rect.centerx < self.rect.centerx:  
                if self.rect.x > self.start_x - self.move_range: 
                    self.rect.x -= self.move_speed
                if self.facing_left:
                    self.facing_left = True
                    self.image = pygame.transform.flip(self.original_image, True, False)
                    
            elif player_2.char_2_rect.centerx > self.rect.centerx:  
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
            player_2.char_2_rect.centerx)  
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
    
    def reset(self):
        self.rect.x = self.initial_x 
        self.rect.y = self.initial_y 
        self.health = self.max_health
        self.bullets.empty()

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

def create_ghost_2(x_position, y_position, move_range):
    #Create a ghost at the specified position
    #x_position: x coordinate in world space
    #y_position: y coordinate
    #move_range: how far the ghost can move left/right from its starting position

    enemy_2 = Enemy_2(x_position, y_position, move_range)
    enemy_group_2.add(enemy_2)
    return enemy_2

# Boss class
class ghost_boss(pygame.sprite.Sprite):
    def __init__(self, x_position, y_position,move_range=200):
        super().__init__()
        self.original_image = pygame.image.load("Image/ghost_1.png")
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
        self.health = 500
        self.max_health = 500
        self.shoot_timer = 0 
        self.shoot_interval = 120
        self.bullets = pygame.sprite.Group()  # Create a group of bullets inside
        self.bullet_speed = 7
        self.bullet_image = pygame.image.load("Image/action_ghost_1.png").convert_alpha()
        self.bullet_image = pygame.transform.scale(self.bullet_image, (25, 25))
        
        # Walking properties
        self.move_speed = 2
        self.facing_left = False

    def update(self, scroll_x_2):
        self.rect.x = self.absolute_x - scroll_x_2
        if -150 <= self.rect.x <= 720:
        # Move within the defined range
            if player_2.char_2_rect.centerx < self.rect.centerx:  
                if self.rect.x > self.start_x - self.move_range: 
                    self.rect.x -= self.move_speed
                if self.facing_left:
                    self.facing_left = True
                    self.image = pygame.transform.flip(self.original_image, True, False)
                    
            elif player_2.char_2_rect.centerx > self.rect.centerx:  
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
        bullet = BossBullet(
            self.rect.centerx,
            self.rect.centery,
            self.bullet_image,
            self.bullet_speed,
            player_2.char_2_rect.centerx)  
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
            
class BossBullet(pygame.sprite.Sprite):
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

def create_ghost_boss(x_position, y_position, move_range=200):
    #Create a ghost boss at the specified position
    #x_position: x coordinate in world space
    #y_position: y coordinate
    #move_range: how far the boss can move left/right from its starting position

    boss = ghost_boss(x_position, y_position, move_range)
    boss_group.add(boss)
    return boss

enemy = Enemy(100, 215)
enemy_2 = Enemy_2(100, 215)

#player
reduce_blood_value = 100   
character_images = ["Image/character_1.png","Image/character_2.png","Image/character_3.png"]
player = None
player_rect = pygame.Rect(100,100, 50, 50)

# ITEMS
class ItemBox(pygame.sprite.Sprite):
    def __init__(self,item_type,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.world_x = x
        self.world_y = y
        self.rect.topleft = (self.world_x, self.world_y)

    def update(self,scroll_x):
        self.rect.x = self.world_x-scroll_x
    #check if the player has picked up the box
        if self.rect.colliderect(player.char_1_rect):
            #check what kind of box it was
            if self.item_type == 'Health' :
                player.health += 25
                if player.health > player.max_health :
                    player.health = player.max_health
            elif self.item_type == 'Reduce_blood' :
                player.health -=15
                if player.health < 0:
                    player.health = 0 
            self.kill()

class ItemBox_2(pygame.sprite.Sprite):
    def __init__(self,item_type,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.world_x = x
        self.world_y = y
        self.rect.topleft = (self.world_x, self.world_y)

    def update(self,scroll_x_2):
        self.rect.x = self.world_x-scroll_x_2
    #check if the player has picked up the box
        if self.rect.colliderect(player_2.char_2_rect):
            #check what kind of box it was
            if self.item_type == 'Health' :
                player.health += 25
                if player.health > player.max_health :
                    player.health = player.max_health
            elif self.item_type == 'Reduce_blood' :
                player.health -=15
                if player.health < 0:
                    player.health = 0 
            self.kill()
        

# pick up boxes
health_box_img = pygame.image.load("Image/item_3.png").convert_alpha()
reduce_blood_box_img = pygame.image.load("Image/item_4.png").convert_alpha()
item_boxes = { 
    'Health': health_box_img,
    'Reduce_blood' : reduce_blood_box_img
}

def create_item_health_item(x, y):
    health_item  = ItemBox('Health',x,y)
    item_box_group_health_item.add(health_item)    
    return health_item

def create_item_health_item_2(x, y):
    health_item_2  = ItemBox_2('Health',x,y)
    item_box_group_health_item_2.add(health_item_2)    
    return health_item_2

def create_item_reduce_blood_item_2(x, y):
    reduce_blood_item_2  = ItemBox_2('Reduce_blood',x,y)
    item_box_group_reduce_blood_item_2.add(reduce_blood_item_2)    
    return reduce_blood_item_2

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

#define font
font =pygame.font.SysFont('Futura',20)

def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))


def load_and_scale_image(path, scale):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, (image.get_width() // scale, image.get_height() // scale))

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

#the floor section
dirt_blocks = pygame.sprite.Group()
lava_blocks = pygame.sprite.Group()
for i in range(0, 15000, 71):  # start, how long, space (dirt = 40, lava = 71)
    lava = LavaBlock(i, 361, 9)
    lava_blocks.add(lava)

#blocks for the frist session
def create_blocks_1(start_x, y_pos, count): 
    for step in range(count):
        x_position = start_x + (step * 40)
        block = DirtBlock(x_position, y_pos, 9)
        dirt_blocks.add(block)
        
#y = 361(first(floor)), 300(second), 240(third), 180(forth)
#the last number is number of blocks
#the first 9110 blocks is the first session
#the last 500 blocks is the end
create_blocks_1(0, 361, 6)
create_blocks_1(300, 300, 6)
create_ghost(360, 151, 72) #ghost1
create_blocks_1(540, 240, 5)
create_blocks_1(780, 361, 12)
create_ghost(954, 213, 200) # ghost2
create_blocks_1(1300, 300, 10)
create_ghost(1400, 151, 100) #ghost3
create_blocks_1(1840, 240, 14)
create_ghost(2050, 92, 230) # ghost4
create_blocks_1(2500, 300, 10)
create_item_health_item(3000,190) #Item
create_blocks_1(2900, 240, 8)
create_ghost(3000, 92, 100) #ghost5
create_blocks_1(3220, 180, 15)
create_ghost(3452, 31, 251) # ghost6
create_blocks_1(4000, 300, 10)
create_ghost(4131, 151, 151)  # ghost7
create_blocks_1(4400, 240, 9)
create_ghost(4550, 92, 100) #ghost8
create_blocks_1(4800, 361, 6)
create_item_health_item(4900,310) #Item
create_blocks_1(5040, 300, 5)
create_blocks_1(5240, 240, 15) 
create_ghost(5470, 92, 251) # ghost9
create_blocks_1(6000, 300, 8)
create_blocks_1(6320, 240, 3)
create_blocks_1(6440, 180, 15)
create_ghost(6670, 31, 251) # ghost10
create_blocks_1(7040, 240, 8)
create_ghost(7100, 92, 80) #ghost11
create_blocks_1(7360, 180, 8)
create_ghost(7440, 31, 100) #ghost12
create_item_health_item(7500,130) #Item
create_blocks_1(7680, 240, 6)
create_blocks_1(7920, 300, 15)
create_ghost(8150, 151, 251) # ghost13
create_blocks_1(8520, 361, 20)
create_item_health_item(9000,310) #Item
create_ghost(8750, 213, 251) # ghost14
create_blocks_1(9320, 300, 8)
create_ghost(9440, 151, 80) # ghost15
create_blocks_1(9640, 240, 5)
create_blocks_1(9840, 300, 10)
create_ghost(9960, 151, 140) #ghost16
create_blocks_1(10240, 361, 15)
create_ghost(10500, 213, 200) #ghost17
create_blocks_1(10840, 300, 8)
create_blocks_1(11200, 240, 8)
create_blocks_1(11560, 180, 26)
create_ghost(11700, 31, 150) #ghost18
#end of first session

#the floor section
dirt_blocks_2 = pygame.sprite.Group()
lava_blocks_2 = pygame.sprite.Group()
for i in range(0, 11000, 71):  # start, how long, space (dirt = 40, lava = 71)
    lava_2 = LavaBlock(i, 361, 9)
    lava_blocks_2.add(lava_2)

#blocks for the second session
def create_blocks_2(start_x, y_pos, count): 
    for step in range(count):
        x_position = start_x + (step * 40)
        block = DirtBlock_2(x_position, y_pos, 9)
        dirt_blocks_2.add(block)
        
#y = 361(first(floor)), 300(second), 240(third), 180(forth)
#the last number is number of blocks
#the second 10500 blocks is the second session
#the last 500 blocks is the end

create_blocks_2(0, 361, 15   )
create_item_health_item_2(400,310) #Item
create_blocks_2(650 , 300, 5)
create_blocks_2(900, 240, 6)
create_item_reduce_blood_item_2(1000,190) #Item
create_blocks_2(1200, 180, 15)
create_ghost_2(1500, 31, 480) #ghost
create_blocks_2(1850, 300, 4)
create_blocks_2(2100, 361, 6)
create_blocks_2(2400, 300, 5)
create_blocks_2(2700, 240, 6)
create_item_reduce_blood_item_2(2800,190) #Item
create_blocks_2(3000, 180, 6)
create_blocks_2(3350, 180, 7)
create_ghost_2(3400, 31, 480) #ghost
create_blocks_2(3700, 300, 6)
create_blocks_2(4000, 240, 5)
create_blocks_2(4300, 300, 6)
create_blocks_2(4600, 361, 13)
create_item_health_item_2(5000,310) #Item
create_blocks_2(5240, 300, 7)
create_blocks_2(5600, 240, 8)
create_blocks_2(6000, 180, 5)
create_ghost_2(6500, 31, 480) #ghost
create_blocks_2(6320, 180, 12)
create_blocks_2(6900, 240, 6)
create_blocks_2(7300, 300, 10)
create_item_reduce_blood_item_2(7500,240) #Item 
create_blocks_2(7780, 361, 8)
create_blocks_2(8200, 300, 8)
create_blocks_2(8620, 240, 8)
create_item_health_item_2(8800,190) #Item
create_ghost_2(9500, 31, 480) #ghost
create_blocks_2(9000, 180, 15)
create_blocks_2(9700, 361, 50)
create_item_health_item_2(9800,310) #Item
create_ghost_boss(10000, 200)  #ghost boss      

  
def reset_game():    
    global button_value, howtoplay_button_value, character_values, back_value, play_value
    global gameover_value, speed, scroll_x, end_of_level_x, level_next
    global player, health_bar, enemy_group, bullet_group, dirt_blocks, item_box_group_health_item,dirt_blocks_2
    # reset game
    all_sprites.empty()
    obstacles.empty()
    enemy_group.empty()
    enemy_group_2.empty()
    bullet_group.empty()
    bullet_group_2.empty()
    item_box_group_health_item.empty()
    item_box_group_health_item_2.empty()
    item_box_group_reduce_blood_item_2.empty()
    boss_group.empty()
    dirt_blocks.empty()
    dirt_blocks_2.empty()
    lava_blocks.empty()
    lava_blocks_2.empty()
    
    button_value = False
    howtoplay_button_value = 0
    character_values = [False, False, False]
    back_value = False
    play_value = False
    selected_character_index = 0
    speed = 10
    scroll_x = 0 
    scroll_x_2 = 0
    end_of_level_x = 9110   
    end_of_level_x_2 = 11000
    level_next = False
    
    # Create again
    enemy = Enemy(100, 215)
    enemy_2 = Enemy_2(100, 215)
    reduce_blood_value = 100   
    character_images = ["Image/character_1.png","Image/character_2.png","Image/character_3.png"]
    player = character(55, 305, character_images[selected_character_index], 2,reduce_blood_value,enemy)
    player_rect = pygame.Rect(100,100, 50, 50)
    
    for i in range(0, 9000, 71):  # start, how long, space (dirt = 40, lava = 71)
        lava = LavaBlock(i, 361, 9)
        lava_blocks.add(lava)

    create_blocks_1(0, 361, 6)
    create_blocks_1(300, 300, 6)
    create_ghost(360, 151, 72) #ghost1
    create_blocks_1(540, 240, 5)
    create_blocks_1(780, 361, 12)
    create_ghost(954, 213, 200) # ghost2
    create_blocks_1(1300, 300, 10)
    create_ghost(1400, 151, 100) #ghost3
    create_blocks_1(1840, 240, 14)
    create_ghost(2050, 92, 230) # ghost4
    create_blocks_1(2500, 300, 10)
    create_item_health_item(3000,190) #Item
    create_blocks_1(2900, 240, 8)
    create_ghost(3000, 92, 100) #ghost5
    create_blocks_1(3220, 180, 15)
    create_ghost(3452, 31, 251) # ghost6
    create_blocks_1(4000, 300, 10)
    create_ghost(4131, 151, 151)  # ghost7
    create_blocks_1(4400, 240, 9)
    create_ghost(4550, 92, 100) #ghost8
    create_blocks_1(4800, 361, 6)
    create_item_health_item(4900,310) #Item
    create_blocks_1(5040, 300, 5)
    create_blocks_1(5240, 240, 15) 
    create_ghost(5470, 92, 251) # ghost9
    create_blocks_1(6000, 300, 8)
    create_blocks_1(6320, 240, 3)
    create_blocks_1(6440, 180, 15)
    create_ghost(6670, 31, 251) # ghost10
    create_blocks_1(7040, 240, 8)
    create_ghost(7100, 92, 80) #ghost11
    create_blocks_1(7360, 180, 8)
    create_ghost(7440, 31, 100) #ghost12
    create_item_health_item(7500,130) #Item
    create_blocks_1(7680, 240, 6)
    create_blocks_1(7920, 300, 15)
    create_ghost(8150, 151, 251) # ghost13
    create_blocks_1(8520, 361, 20)
    create_item_health_item(9000,310) #Item
    create_ghost(8750, 213, 251) # ghost14
    create_blocks_1(9320, 300, 8)
    create_ghost(9440, 151, 80) # ghost15
    create_blocks_1(9640, 240, 5)
    create_blocks_1(9840, 300, 10)
    create_ghost(9960, 151, 140) #ghost16
    create_blocks_1(10240, 361, 15)
    create_ghost(10500, 213, 200) #ghost17
    create_blocks_1(10840, 300, 8)
    create_blocks_1(11200, 240, 8)
    create_blocks_1(11560, 180, 26)
    create_ghost(11700, 31, 150) #ghost18
    #end of first session
        
    for i in range(0, 11000, 71):  # start, how long, space (dirt = 40, lava = 71)
        block = LavaBlock(i, 361, 9)
        dirt_blocks_2.add(block)
    create_blocks_2(0, 361, 15   )
    create_item_health_item_2(400,310) #Item
    create_blocks_2(650 , 300, 5)
    create_blocks_2(900, 240, 6)
    create_item_reduce_blood_item_2(1000,190) #Item
    create_blocks_2(1200, 180, 15)
    create_ghost_2(1500, 31, 480) #ghost
    create_blocks_2(1850, 300, 4)
    create_blocks_2(2100, 361, 6)
    create_blocks_2(2400, 300, 5)
    create_blocks_2(2700, 240, 6)
    create_item_reduce_blood_item_2(2800,190) #Item
    create_blocks_2(3000, 180, 6)
    create_blocks_2(3350, 180, 7)
    create_ghost_2(3400, 31, 480) #ghost
    create_blocks_2(3700, 300, 6)
    create_blocks_2(4000, 240, 5)
    create_blocks_2(4300, 300, 6)
    create_blocks_2(4600, 361, 13)
    create_item_health_item_2(5000,310) #Item
    create_blocks_2(5240, 300, 7)
    create_blocks_2(5600, 240, 8)
    create_blocks_2(6000, 180, 5)
    create_ghost_2(6500, 31, 480) #ghost
    create_blocks_2(6320, 180, 12)
    create_blocks_2(6900, 240, 6)
    create_blocks_2(7300, 300, 10)
    create_item_reduce_blood_item_2(7500,240) #Item 
    create_blocks_2(7780, 361, 8)
    create_blocks_2(8200, 300, 8)
    create_blocks_2(8620, 240, 8)
    create_item_health_item_2(8800,190) #Item
    create_ghost_2(9500, 31, 480) #ghost
    create_blocks_2(9000, 180, 15)
    create_blocks_2(9700, 361, 50)
    create_item_health_item_2(9800,310) #Item
    create_ghost_boss(10000, 200)  #ghost boss 

def reset_gamefornextlevel():    
    global speed, scroll_x, end_of_level_x, level_next,player,movetothe_right_2,movetothe_left_2,movetothe_left,movetothe_right
    global  enemy_group, bullet_group, dirt_blocks, item_box_group_health_item,reduce_blood_value,start
    # reset game
    all_sprites.empty()
    obstacles.empty()
    enemy_group.empty()
    bullet_group.empty()
    item_box_group_health_item.empty()
    boss_group.empty()
    dirt_blocks.empty()
    reduce_blood_value = 100

    
    #keyboard control
    movetothe_left = False
    movetothe_right = False
    movetothe_left_2  = False
    movetothe_right_2 = False
    
    speed = 10
    scroll_x = 0    
    start = False
    level_next = True
    
#game loop
run = True
while run:
    clock.tick(FPS)
    screen.blit(background_start,(0,0))
    button_start.draw(screen)
    button_howtoplay.draw(screen)
    #button start
    if button_howtoplay.is_pressed():
        howtoplay_button_value = 1
    if howtoplay_button_value == 1:
        screen.fill((0,0,0))
        screen.blit(howtoplay,(0,0))
        button_play_howtoplay.draw(screen)
        if button_play_howtoplay.is_pressed() :
            button_value = True
        
    if button_start.is_pressed():
        button_value = True
    if button_value == True:
        screen.blit(select_characters,(0,0))
        characters = [character_1, character_2, character_3]
        for index, characterr in enumerate(characters):
            characterr.draw(screen)
            if characterr.is_pressed():
                character_values[index] = True
                break
                
        for index, character_value in enumerate(character_values):
            if character_value:
                screen.blit(eval(f'background_character_{index + 1}'), (0, 0))
                button_play.draw(screen)
                button_back.draw(screen)

                if button_back.is_pressed():
                    back_value = True
                    break
                elif button_play.is_pressed():
                    play_value = True
                    selected_character_index = index
                    player = character(55, 305, character_images[selected_character_index], 2,reduce_blood_value,enemy)
                    health_bar = HealthBar(10,10,player.health,player.health) 
                    player_2_rect = pygame.Rect(100,100, 50, 50)
                    player_2 = character_next(55, 305, character_images[selected_character_index], 2,reduce_blood_value,enemy_2)
                    break
     
    if back_value:
        button_value = True
        character_values = [False, False, False]  
        back_value = False

    if play_value:
        start = True
        if start :
            screen.fill((0,0,0))
            screen.blit(background2, (0, 0))
            lava_blocks.draw(screen)
            dirt_blocks.draw(screen)
            move_objects_for_right(speed, movetothe_right)
            
            if player.health > 0:
                player.draw()
                health_bar.draw(player.health)
                player.update_jump(dirt_blocks)
                player.move(movetothe_left, movetothe_right,dirt_blocks)
                player.move_2(movetothe_left, movetothe_right,dirt_blocks_2)
                player.update()
                
                for lava in lava_blocks:
                    if player.char_1_rect.colliderect(lava.rect):
                        player.health = 0
            else:
                    player.kill()
                    screen.blit(gameover, (0, 0))
                    button_newgame.draw(screen)
                    if button_newgame.is_pressed():
                        reset_game()
                    
                    
            item_box_group_health_item.update(scroll_x)
            item_box_group_health_item.draw(screen)
            #show player health
            draw_text(f"HEART :",font,WHITE,10,35)
            #BULLETS
            bullet_group.update()
            bullet_group.draw(screen)

            for enemy in enemy_group:
                enemy.update(scroll_x)
                enemy.draw(screen)
                if -150 <= enemy.rect.x <= 720:
                    for bullet in bullet_group:
                        if enemy.rect.colliderect(bullet.rect):
                            enemy.take_damage(100) #กำหนดเพื่อให้ง่ายต่อการรัน เดี๋ยวมาเปลี่ยน
                            bullet.kill()
                    
                    # Check for collisions between boss bullets and players.
                    for bullet in enemy.bullets:
                        if bullet.rect.colliderect(player.char_1_rect):
                            player.health -= 10  
                            bullet.kill()
                # End game if boss health reaches 0
                if enemy.health <= 0:
                    enemy.kill()
                    player.enemy_defeated += 1
                #if the player touch the enemy, the health bar will get deducted
                #it's because of hitboxs, so putting +100 making it looks more real (collide)
                if enemy.rect.x +100 < player.y:
                    player.health -= 50
                    enemy.kill()
                    player.enemy_defeated += 1

        if level_next :
            reset_gamefornextlevel()
            screen.fill((0,0,0))
            start = False
            scroll_x_2 = 0
        if not start and level_next:
            screen.blit(background3, (0, 0))
            lava_blocks_2.draw(screen)
            dirt_blocks_2.draw(screen)
            
            def move_objects_for_right_levelnext(speed, move):
                global scroll_x_2, player_2
                print(scroll_x_2)
                if move and scroll_x_2 < end_of_level_x_2 - width: 
                    if player_2.char_2_rect.x >= 0:  #21 is the rect.x starting point of the player
                        player_2.char_2_rect.left += speed
                        scroll_x_2 += speed 
                    for block in dirt_blocks_2:
                        if player_2.char_2_rect.x < 0: 
                            pass #the objects don't move
                        else:
                            block.rect.x -= speed #the objects move to the left
                    return False
            move_objects_for_right_levelnext(speed, movetothe_right_2)
            
            if player_2.health > 0:
                print(f"Player 2 Position: {player_2.char_2_rect.x}, Health: {player_2.health}")
                print(f"Change X: {player_2.change_x}, Position: {player_2.char_2_rect.x}")
                player_2.draw(screen)
                move_objects_for_right_levelnext(speed, movetothe_right_2)
                player_2.update_jump_2(dirt_blocks_2)
                player_2.move_next_2(movetothe_left_2, movetothe_right_2,dirt_blocks_2)
                player_2.update(scroll_x_2)
                for lava_2 in lava_blocks_2:
                    if player_2.char_2_rect.colliderect(lava_2.rect):
                        player_2.health = 0

            else:
                player_2.kill()
                screen.blit(gameover, (0, 0))
                button_newgame.draw(screen)
                if button_newgame.is_pressed():
                    reset_game()
            
            item_box_group_health_item_2.update(scroll_x_2)
            item_box_group_health_item_2.draw(screen)
            item_box_group_reduce_blood_item_2.update(scroll_x_2)
            item_box_group_reduce_blood_item_2.draw(screen)
            #show player health
            health_bar.draw(player_2.health)
            draw_text(f"HEART :",font,WHITE,10,35)

            #BULLETS
            bullet_group_2.update()
            bullet_group_2.draw(screen)

            for enemy_2 in enemy_group_2:
                enemy_2.update(scroll_x_2)
                enemy_2.draw(screen)
                if -150 <= enemy_2.rect.x <= 720:
                    for bullet in bullet_group_2:
                        if enemy_2.rect.colliderect(bullet.rect):
                            enemy_2.take_damage(10)
                            bullet.kill()
                    
                    # Check for collisions between boss bullets and players.
                    for bullet in enemy_2.bullets:
                        if bullet.rect.colliderect(player_2.char_2_rect):
                            player_2.health -= 10  
                            bullet.kill()
                # End game if boss health reaches 0
                if enemy_2.health <= 0:
                    enemy_2.kill()
                #if the player touch the enemy, the health bar will get deducted
                if enemy_2.rect.x < player_2.y:
                    player_2.health -= 50
                    enemy_2.kill()
            

            for boss in boss_group:
                boss.update(scroll_x_2)
                boss.draw(screen)
                if -150 <= boss.rect.x <= 720:
                    for bullet in bullet_group_2:
                        if boss.rect.colliderect(bullet.rect):
                            boss.take_damage(10)
                            bullet.kill()
                    
                    # Check for collisions between boss bullets and players.
                    for bullet in boss.bullets:
                        if bullet.rect.colliderect(player_2.char_2_rect):
                            player_2.health -= 15  
                            bullet.kill()
                # End game if boss health reaches 0
                if boss.health <= 0:
                    boss.kill()
                #if the player touch the enemy, the health bar will get deducted
                if boss.rect.x < player_2.y:
                    player_2.health -= 50
                    boss.kill()
            
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            run = False
        #keyboard control (pressed)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                    movetothe_left = True
                    #print("Player 1 left")
                    movetothe_left_2 = True
                    #print("Player 2 left")
                    if player.health == 0:
                        movetothe_left = False

            if event.key == pygame.K_RIGHT:
                    movetothe_right = True
                    #print("Player 1 right")
                    movetothe_right_2 = True
                    #print("Player 2 right")
                    if player.health == 0:
                        movetothe_right = False

            if event.key == pygame.K_ESCAPE:  # Closing game window with ESC
                run = False

            if event.key == pygame.K_UP:  # Jump for Player 1
                    player.jump()
                    #print("Player 1 jump")
                    player_2.jump()
                    #print("Player 2 jump")

            if event.key == pygame.K_SPACE:
                    player.shoot()
                    #print("Player 1 shoots")
                    player_2.shoot()
                    #print("Player 2 shoots")

        #(released)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                    movetothe_left = False
                    movetothe_left_2 = False
            if event.key == pygame.K_RIGHT:
                    movetothe_right = False
                    movetothe_right_2 = False
    pygame.display.update() #update the screen

pygame.quit()