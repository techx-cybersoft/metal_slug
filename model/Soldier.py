import pygame, random
from settings import Status_Soldier, Direction
from model.SmallBullet import SmallBullet

class Soldier:
    def __init__(self):
        self.image = pygame.image.load('./images/left/soldier/freeze/0.png')
        self.rect = self.image.get_rect()
        self.rect.x = 1180
        self.rect.y = 550
        self.frame = 0
        self.status = Status_Soldier.FREEZE
        self.direction = Direction.LEFT
        self.speed = 2
        self.time_status_start = 0
        self.time_random_status_start = 0
        self.time_move_start = 0
        self.time_bullet_start = 0
        self.lst_bullet:list[SmallBullet] = []
        self.max_pos = random.randint(780, 1180)
    
    def update_status(self):
        #Xử lý folder hướng
        folder_name_direct = 'left'
        #Xử lý folder status
        folder_status_name = ''
        #Frame theo status
        frame_count = 0
        if self.status == Status_Soldier.MOVE:
            folder_status_name = 'move'
            frame_count = 7
        elif self.status == Status_Soldier.ATTACK:
            folder_status_name = 'attack'
            frame_count = 5
        elif self.status == Status_Soldier.DIE: 
            folder_status_name = 'die'
            frame_count = 15
        else:
            folder_status_name = 'freeze'
            frame_count = 4
        

        image_src =  f'./images/{folder_name_direct}/soldier/{folder_status_name}/{self.frame % frame_count}.png'
        
        self.image = pygame.image.load(image_src)
    
    def move(self):
        if self.rect.x <= self.max_pos:
            self.status = Status_Soldier.FREEZE
        else:
            self.status = Status_Soldier.MOVE
            self.rect.x -= self.speed
            
    def attack(self):
        self.status = Status_Soldier.ATTACK
        x_bullet = self.rect.x + self.rect.width 
        y_bullet = self.rect.y + self.rect.height // 2
        new_bullet = SmallBullet(x_bullet,y_bullet)
        self.lst_bullet.append(new_bullet)
    
    # def draw(self,screen):
    #     self.move()
        
    #     current_status_time = pygame.time.get_ticks()
    #     if self.rect.x <= self.max_pos:
    #         if current_status_time - self.time_bullet_start >= 2000:
    #             self.attack()
    #             self.time_bullet_start = current_status_time
        
    #     for small in self.lst_bullet:
    #         small.move()
    #         small.draw(screen)
    #         if small.rect.x < 0:
    #             self.lst_bullet.remove(small)
        
    #     screen.blit(self.image,self.rect)
    #     if current_status_time - self.time_status_start >= 300:
    #         self.frame += 1
    #         self.time_status_start = current_status_time
            
    #     self.update_status()
    
    def draw(self,screen):
        screen.blit(self.image,self.rect)
        #Update status cập nhật frame
        current_status_time = pygame.time.get_ticks()
        if current_status_time - self.time_status_start >= 300:
            self.frame += 1
            self.time_status_start = current_status_time
            
        # Chuyển đổi trạng thái
        current_change_status = pygame.time.get_ticks()
        if current_change_status - self.time_random_status_start > 5000:
            #Chuyển enum -> list
            lst_enum = list(Status_Soldier)
            #Tiến hành random enum
            status_random = random.choice(lst_enum)
            while status_random == Status_Soldier.DIE:
                status_random = random.choice(lst_enum)     
            self.status = status_random
            self.time_random_status_start = current_change_status
        #Xử lý từng trạng thái sau khi random
        if self.status == Status_Soldier.MOVE:
            current_move = pygame.time.get_ticks()
            if current_move - self.time_move_start >= 300:
                self.move()
                self.time_move_start = current_move
        elif self.status == Status_Soldier.ATTACK:
            current_attack = pygame.time.get_ticks()
            if current_attack - self.time_bullet_start > 2500:
                self.attack()
                self.time_bullet_start = current_attack
            
        #Vẽ lại đạn
        for bullet in self.lst_bullet:
            bullet.move()
            bullet.draw(screen)
        self.update_status()