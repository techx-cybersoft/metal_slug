import pygame
from settings import Direction, Status_Hero
from model.Bullet import Bullet

class Hero:
    def __init__(self):
        self.image = pygame.image.load("./images/right/hero/freeze/0.png")
        self.rect = self.image.get_rect()
        self.rect.y = 550
        self.frame = 0
        self.status = Status_Hero.FREEZE
        self.direction = Direction.RIGHT
        self.speed = 2
        self.hero_status_start = 0
        self.lst_bullet:list[Bullet] = []
    
    def update_status(self):
        folder_name_direct = ''
        if self.direction == Direction.LEFT:
            folder_name_direct = 'left'
        else:
            folder_name_direct = 'right'
        #Xử lý folder status
        folder_status_name = ''
        #Frame theo status
        frame_count = 0
        if self.status == Status_Hero.MOVE:
            folder_status_name = 'move'
            frame_count = 4
        elif self.status == Status_Hero.ATTACK:
            folder_status_name = 'attack'
            frame_count = 4
        elif self.status == Status_Hero.DIE: 
            folder_status_name = 'die'
            frame_count = 19
        else:
            folder_status_name = 'freeze'
            frame_count = 3
        

        image_src =  f'./images/{folder_name_direct}/hero/{folder_status_name}/{self.frame % frame_count}.png'
        
        self.image = pygame.image.load(image_src)
    
    def attack(self): # Tạo phương thức
        self.status = Status_Hero.ATTACK
        #Tạo ra 1 viên đạn mới nạp vào self.list_bullet
        if self.direction == Direction.RIGHT:
            x_bullet = self.rect.x + self.rect.width 
            y_bullet = self.rect.y + self.rect.height // 2
            new_bullet = Bullet(x_bullet,y_bullet,Direction.RIGHT)
            self.lst_bullet.append(new_bullet)
        else:
            x_bullet = self.rect.x
            y_bullet = self.rect.y + self.rect.height // 2
            new_bullet = Bullet(x_bullet,y_bullet,Direction.LEFT)
            self.lst_bullet.append(new_bullet)
    
    def move(self,direction):
        self.direction = direction
        self.status = Status_Hero.MOVE
        if self.direction == Direction.LEFT:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
    
    
    def draw(self, screen):
        for bullet in self.lst_bullet:
            bullet.move()
            bullet.draw(screen)
            if bullet.rect.x > screen.get_width() and bullet.direction == Direction.RIGHT:
                self.lst_bullet.remove(bullet)
            elif bullet.rect.x < 0 and bullet.direction == Direction.LEFT:
                self.lst_bullet.remove(bullet)
        screen.blit(self.image, self.rect)
        hero_status_current = pygame.time.get_ticks()
        if hero_status_current - self.hero_status_start >= 300:
            self.frame += 1
            self.hero_status_start = hero_status_current
        self.update_status()