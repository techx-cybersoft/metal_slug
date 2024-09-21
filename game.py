import pygame, random
import sys
from model.Hero import Hero
from model.Soldier import Soldier
from settings import Direction, Status_Hero, Status_Soldier

pygame.init()

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 820

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Metal Slug")

bg_game = pygame.image.load("./images/bkgd.png")
bg_game_rect = bg_game.get_rect()
bg_game = pygame.transform.scale(bg_game, (bg_game_rect.width, SCREEN_HEIGHT))

scroll_bg = bg_game_rect.x

hero = Hero()
x_hero_start = hero.rect.x

first_soldier = Soldier()

lst_soldier:list[Soldier] = []
# lst_soldier.append(first_soldier)

#Setup thời gian tạo lính
time_create_soldier = 0

#Đồng hồ xử lý chết
time_die_soldier = 0

font_game = pygame.font.Font('./graphics/f_game.otf', 32)
score = 300
score_title = font_game.render(f'Score: {score}', True, 'Orange')

live = 5
live_title = font_game.render(f"Live: {live}", True, "Orange")
live_rect = live_title.get_rect()
live_rect.x = 0
live_rect.y = score_title.get_height() + 2

game_over = "GAME OVER"
game_over_title = font_game.render(game_over, True, "Red")
game_over_rect = game_over_title.get_rect()
game_over_rect.x = SCREEN_WIDTH // 2 - game_over_title.get_width() // 2
game_over_rect.y = SCREEN_HEIGHT // 2 - game_over_title.get_height() //2

running = True

while running:
    x_current_hero = hero.rect.x
    
    if live < 0:
        screen.blit(game_over_title, game_over_rect)
        pygame.display.flip()
        pygame.time.wait(3000) 
        running = False
        
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN: #Sự kiện nhấp phím
            if event.key == pygame.K_j:
                hero.attack()
        
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_d:
        #         scroll_bg -= 20
        #     if event.key == pygame.K_a:
        #         scroll_bg += 20
    
    # Xử lý sự chuyển động của nhân vật hero
    key = pygame.key.get_pressed() # Sư kiện đè phím
    if key[pygame.K_a] and hero.rect.x > 0:
        hero.move(Direction.LEFT)
    elif key[pygame.K_d] and hero.rect.x <= SCREEN_WIDTH - hero.rect.width:
        hero.move(Direction.RIGHT)
    else:
        hero.status = Status_Hero.FREEZE
    
    # Xử lý sự chuyển động của Background Game (phụ thuộc vào sự chuyển động của Hero)
    if hero.direction == Direction.RIGHT and x_current_hero != x_hero_start:
        scroll_bg -= hero.speed
        x_hero_start = x_current_hero
    elif hero.direction == Direction.LEFT and x_current_hero != x_hero_start:
        scroll_bg += hero.speed
        x_hero_start = x_current_hero
    
    screen.blit(bg_game, (scroll_bg, bg_game_rect.y))
    
    current_time_soldier = pygame.time.get_ticks()
    #Tạo ra 1 lính sau mỗi 5s
    if current_time_soldier - time_create_soldier >= 2000:
        new_soldier = Soldier()
        # new_soldier.rect.x = random.randint(500,1000)
        # new_soldier.direction = Direction.LEFT
        lst_soldier.append(new_soldier)
        time_create_soldier = current_time_soldier
    
    #Xử lý bắn
    for bullet in hero.lst_bullet:
        for soldier_item in lst_soldier:
            if bullet.rect.colliderect(soldier_item.rect) and soldier_item.status != Status_Soldier.DIE:
                soldier_item.status = Status_Soldier.DIE
                hero.lst_bullet.remove(bullet)
                # lst_soldier.remove(soldier_item)
                score += 100
                break
    
    for soldier_item in lst_soldier:
        #Vẽ soldier
        soldier_item.draw(screen)
        for bullet in soldier_item.lst_bullet:
            if bullet.rect.colliderect(hero.rect):
                soldier_item.lst_bullet.remove(bullet)
                live -= 1
    
    #xử lý chết cho tất cả lst_soldier
    current_time_die_soldier = pygame.time.get_ticks()
    if current_time_die_soldier - time_die_soldier > 2000:
        for soldier_item in lst_soldier:
            if soldier_item.status == Status_Soldier.DIE:
                lst_soldier.remove(soldier_item)
        time_die_soldier = current_time_die_soldier
    
    score_title = font_game.render(f'Score: {score}', True, 'Orange')
    screen.blit(score_title, (0,0))
    live_title = font_game.render(f"Live: {live}", True, "Orange")
    screen.blit(live_title, (live_rect.x, live_rect.y))
    
    if live <= 0:
        # screen.fill((0, 0, 0))  # Clear the screen
        hero.status = Status_Hero.DIE

    hero.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()