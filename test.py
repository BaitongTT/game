import pygame
import pygame_button
pygame.init()

#framerate
clock = pygame.time.Clock()
FPS = 70

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


def load_and_scale_image(path, scale):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, (image.get_width() // scale, image.get_height() // scale))

#load images
background_start = pygame.image.load("Image/background_1.png").convert_alpha()
select_characters = pygame.image.load("Image/select_charecter.png").convert_alpha()
background_character_1 = pygame.image.load("Image/select_1.png").convert_alpha()
background_character_2 = pygame.image.load("Image/select_2.png").convert_alpha()
background_character_3 = pygame.image.load("Image/select_3.png").convert_alpha()
background2 = pygame.image.load("Image/background_2.png").convert()

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
button_howtoplay= button("Image/button_howtoplay.png",(0,250))
character_1 = button("Image/1_charecter.png",(60,133))
character_2 = button("Image/2_charecter.png",(269,135))
character_3 = button("Image/3_charecter.png",(479,135))
button_back = button("Image/button_back.png",(252,327))
button_play = button("Image/button_play.png",(365,327))    

# variable
button_value = False
character_values = [False, False, False]
back_value = False
play_value = False
selected_character_index = 0

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

# sprite groups
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
item_box_group_health_item = pygame.sprite.Group()
item_box_group_reduce_blood_item = pygame.sprite.Group()
lava_group = pygame.sprite.Group()

#enemy
enemy = ghost(x_position=100, y_position=200, image_ghost="Image/ghost_2.png", 
              image_bullet="Image/action_ghost_2.png", health=150)

#setting player
reduce_blood_value = 100   
character_images = ["Image/character_1.png","Image/character_2.png","Image/character_3.png"]
player_rect = pygame.Rect(100,100, 50, 50)
player = character(55, 305, character_images[selected_character_index], 2,reduce_blood_value,enemy)

#the floor section
dirt_blocks = pygame.sprite.Group()
for i in range(0, 9000, 71):  # start, how long, space (dirt = 40, lava = 71)
    block = LavaBlock(i, 361, 9)
    dirt_blocks.add(block)

# pick up boxes
health_box_img = pygame.image.load("Image/item_3.png").convert_alpha()
reduce_blood_box_img = pygame.image.load("Image/item_4.png").convert_alpha()
item_boxes = { 
    'Health': health_box_img,
    'Reduce_blood' : reduce_blood_box_img
}

#define font
font =pygame.font.SysFont('Futura',20)


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

#game loop
run = True
while run:
    clock.tick(FPS)
    ##Startgame
    screen.blit(background_start,(0,0))
    button_start.draw(screen)
    #button start
    if button_start.is_pressed():
        button_value = True
    if button_value == True:
        screen.blit(select_characters,(0,0))
        characters = [character_1, character_2, character_3]
        for index, CHARACTER in enumerate(characters):
            CHARACTER.draw(screen)
            if CHARACTER.is_pressed():
                character_values[index] = True
                selected_character_index = index
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
                    break
            
    if back_value:
        button_value = True
        character_values = [False, False, False]  
        back_value = False

    if play_value:
        screen.fill((0, 0, 0))
        screen.blit(background2, (0, 0))
        #the floor section
        dirt_blocks = pygame.sprite.Group()
        for i in range(0, 9000, 71):  # start, how long, space (dirt = 40, lava = 71)
            block = LavaBlock(i, 361, 9)
            dirt_blocks.add(block)
            #y = 361(first(floor)), 300(second), 240(third), 180(forth)
            #the last number is number of blocks
            #the first 9110 blocks is the first session
            #the last 500 blocks is the end
        create_blocks_1(0, 361, 6)
        create_blocks_1(300, 300, 6)
        create_blocks_1(540, 240, 5)
        create_blocks_1(780, 361, 12)
        create_ghost(780, 213, 480) # ghost
        create_blocks_1(1300, 300, 10)
        create_blocks_1(1840, 240, 14)
        create_ghost(1840, 92, 560) # ghost
        create_blocks_1(2500, 300, 10)
        create_item_health_item(3000,190) #Item
        create_blocks_1(2900, 240, 8)
        create_blocks_1(3220, 180, 15)
        create_ghost(3220, 31, 600) # ghost
        create_blocks_1(4000, 300, 10)
        create_ghost(4000, 151, 400)  # ghost
        create_blocks_1(4400, 240, 9)
        create_blocks_1(4800, 361, 6)
        create_item_health_item(4900,310) #Item
        create_blocks_1(5040, 300, 5)
        create_blocks_1(5240, 240, 15) 
        create_ghost(5240, 92, 600) # ghost
        create_blocks_1(6000, 300, 8)
        create_blocks_1(6320, 240, 3)
        create_blocks_1(6440, 180, 15)
        create_ghost(6440, 31, 600) # ghost
        create_blocks_1(7040, 240, 8)
        create_blocks_1(7360, 180, 8)
        create_item_health_item(7500,130) #Item
        create_blocks_1(7680, 240, 6)
        create_blocks_1(7920, 300, 15)
        create_ghost(7920, 151, 600) # ghost
        create_blocks_1(8520, 361, 20)
        create_ghost(8520, 213, 800) # ghost
        #end of first session
        
    
        enemy.draw(screen)
        player.draw()
        health_bar = HealthBar(10,10,player.health,player.health)
        item_box_group_health_item.update(scroll_x)
        item_box_group_health_item.draw(screen)
        item_box_group_reduce_blood_item.update(scroll_x)
        item_box_group_reduce_blood_item.draw(screen)
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

        for enemy in enemy_group:
            enemy.update(scroll_x,player)
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
        break
  
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

    pygame.display.update()
pygame.quit()