import pygame, sys
import  pygame_widgets as pw
from random import randint
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Flappy Bird')
running = True
GREY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
clock = pygame.time.Clock()


BK = GREY
COLOR = RED
right = False
left = False

delta = 0
count = 0
count_2 = 0

snake_edge = 10
snake_x, snake_y = 300, 300
snake = [snake_x, snake_y]
list_snake = [snake]
length = 1
food_x, food_y = 100, 300
food = [food_x, food_y]
safe_x, safe_y = 10, 200
safe =[safe_x, safe_y]
list_food = [food]
length_list_food = 1
score, hscore = 0, 0
x = 0
game_close = False
count_close = 0
arialFont = pygame.font.SysFont("Arial", 30)
def message(msg, color, x, y):
    mesg = arialFont.render(msg, True, color)
    textRect = mesg.get_rect()
    textRect.center = (x, y)
    screen.blit(mesg, textRect)
while running:
    clock.tick(10)
    screen.fill(BK)		
    
    message(f"hscore: {hscore}   " + f"score: {score}", GREEN, 300, 50)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    delta = 10
    for snake in list_snake:
        pygame.draw.rect(screen, COLOR, (snake[0], snake[1], snake_edge, snake_edge))
    for food in list_food:	
        pygame.draw.rect(screen, GREEN, (food[0], food[1], snake_edge, snake_edge))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if (snake_x<=mouse_x) &(mouse_x<=snake_x+snake_edge) \
                & (snake_y<=mouse_y) & (mouse_y<=snake_y+snake_edge):
                    COLOR = (randint(0,255),randint(0,255),randint(0,255))
                else:
                    BK = (randint(0,255),randint(0,255),randint(0,255))
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_RIGHT:
                right = True
                left = False
                count += 1
            elif event.key == pygame.K_LEFT:
                left = True
                right = False
                count += 1
            elif event.key == pygame.K_SPACE:
                score -= 1
                count_close += 1
                game_close = (3 - count_close) <=0
                running = (4 - count_close > 0) & (score >= 0) 
            else:
                pass
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
    snake = []
    if right:
        if count%2 == 1:
            snake_x += (1 - 2*((count//2)%2))*delta
        else:
            snake_y -= (1 - 2*((count//2)%2))*delta
    elif left:
        if count%2 == 1:
            snake_x -= (1 - 2*((count//2)%2))*delta
            
        else:
            snake_y += (1 - 2*((count//2)%2))*delta
    
    snake.append(snake_x)
    snake.append(snake_y)
    
    list_snake.append(snake)
    #list_snake.append(food)
    #print(list_snake)
    if len(list_snake)>length:
        del list_snake[0]
        #list_snake = list_snake[1:]
    #print(snake)
    for food in list_food:
        if (snake[0]<= food[0]+snake_edge) & (snake[0]>=food[0]-snake_edge)\
            & (snake[1]<=food[1]+snake_edge) & (snake[1]>= food[1]-snake_edge):
            food[0] = 50*randint(1, 11)
            food[1] = 50*randint(1, 11)
            list_food.append([food[0], food[1]])
            length += 1
            score += 1
            if score > hscore:
                hscore = score
    if len(list_food)>length_list_food:
        del list_food[0]
    if (score % 5 == 0) & (score > x):# thoát khỏi vòng lặp khi score chia hết cho 5
        length_list_food += 1
        list_food.append(safe)
        x = score +1                  # gán lại x để phủ định conditional
    for i in [0, 590]:
        for j in snake:
            if j == i:
                game_close = True
                
    if length >=5:
        for i in range(1, len(list_snake)):
            if list_snake[i] == list_snake[0]:
                game_close = True
                
    if game_close:
        
        if count_close < 3:
            mes_gclose = "you lose! Please press space key to continue!"
        elif count_close >=3 or (score < 0):
            mes_gclose = "GameOver"
            
        message(f"{mes_gclose}", BLACK, 300, 200)
        delta_x = 0
        delta_y = 0
        snake_x, snake_y = 300, 300
        #snake = [300, 300]
     
    #print(length_list_food)
    
    #print(list_food)
    
    """if snake_x == 600:
        snake_x = 0
    elif snake_x == 0:
        snake_x == 600
    if snake_y == 600:
        snake_y = 0
    elif snake_y == 0:
        snake_y = 600"""
    pygame.display.update()
    pygame.display.flip()
pygame.quit()