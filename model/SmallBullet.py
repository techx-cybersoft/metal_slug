import pygame

class SmallBullet:
    def __init__(self, x, y):
        self.image = pygame.image.load("./images/bullet/1.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
    
    def move(self):
        self.rect.x -= self.speed
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)