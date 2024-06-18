import pygame
from random import randint as r
from tkinter import *
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Snake_Game")
screen.fill([100, 100, 100]) # màu nền ban đầu
# Tạo các biến màu
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
Bg = GREY
# Tạo tần số quét mành
clock = pygame.time.Clock()
# Khởi tạo ban đầu cho các đối tượng	
snk_x, snk_y = 300, 300	# tọa độ x, y của rắn
#snake_head = [snk_x, snk_y] # đầu rắn
total_snk = []
length_snk = 1	# độ dài rắn
food_x, food_y = 100, 100 # tọa độ của thức ăn
food_first = [food_x, food_y] # thức ăn 
food_total = [food_first]
amount_food = 1
color_snake = BLACK	# màu sắc
color_food = GREEN
size = 10	# kích thước

# Tạo các đối tượng
class Object:
	def __init__(self, object_total, color, length):
		self.total = object_total
		self.color = color
		self.len = length
	def show_object(self):
		for obj in self.total:
			pygame.draw.rect(screen, self.color, (obj[0], obj[1], size, size))	
# Tạo đối tượng Message
in_click = False
class Message:
	def __init__(self, msg, x, y, in_click):
		self.msg = msg
		#self.color = color
		self.x = x
		self.y = y
		self.in_click = in_click
	# Xây dựng hàm thông báo	
	def show_messge(self):
		global font_color
		mouse_x, mouse_y = pygame.mouse.get_pos()
		mesg = arialFont.render(self.msg, True, font_color)
		textRect = mesg.get_rect()
		textRect.center = (self.x, self.y)
		if (self.x-textRect[2]/2<=mouse_x)&(mouse_x<=self.x+textRect[2]/2)\
			&(self.y-textRect[3]/2<=mouse_y)&(mouse_y<=self.y+textRect[3]/2):
			font_color = GREEN
			self.in_click = True
		else:
			font_color = BLACK
			self.in_click = False
		screen.blit(mesg, textRect)
		print(font_color)
# xây dựng hàm đóng gói đối tượng
# nghiên cứu thêm để xây dựng hàm (nếu còn thời gian)
"""def total_obj(total, object, x, y, length):
	object = []
	total = [object]
	object.append(x)
	object.append(y)
	total.append(object)
	if len(total)>length:
		del total[0]
	return total"""
# Tạo các biến khác
bg_sound = pygame.mixer.Sound("sound_game/bg_1.mp3")
eat_sound = pygame.mixer.Sound("sound_game/eat_1.mp3")
right = False # Biến rẽ phải
left = False  # Biến rẽ phải
running = True # chạy chương trình

count = 0	# đếm chuyển động 
delta = 10	# tốc độ di chuyển
score, hscore = 0, 0 # điểm số và mức điểm cao nhất
escape = 0 # biến cố định khối lượng thức ăn
# Biến khi người chơi thua
game_close = False 
count_close = 0
# Biến khi rắn săn mồi
finish_eat = False
level =1 
# Biến sử dụng trong hàm thông báo
size_font = 30
arialFont = pygame.font.SysFont("Arial", size_font)
font_color = BLACK # màu của font
m_x, m_y = 300, 50 # tọa độ xuất hiện
msg = f"hscore: {hscore}   " + f"score: {score}"
game_close = True
while running:		
	clock.tick(12) # 12 hình trên giây
	screen.fill(Bg) # nhất định phải đưa vào, không sẽ tạo vết (bóng) của các ojb
	#pygame.mixer.Sound.play(bg_sound)
	#pygame.mixer.Sound.play(eat_sound)
	#pygame.draw.rect(screen, snake.color, (snake.x, snake.y, snake.size, snake.size))
	#print(message)
	#mouse_x, mouse_y = pygame.mouse.get_pos()
	# Khởi tạo các đối tượng 
	snake = Object(total_snk, color_snake, length_snk)
	food = Object(food_total, color_food, amount_food)
	message = Message(msg, m_x, m_y, in_click)
    
	# show các đối tượng trên màn hình
	snake.show_object()
	food.show_object()
	message.show_messge()
	#font_color = message.color
	#print(message.x)
	"""if (200<=mouse_x)&(mouse_x<=400)\
		&(40<=mouse_y)&(mouse_y<=60):
		font_color = GREEN
		in_click = True
	else:
		font_color = BLACK
		in_click = False"""
	while game_close == False:
		clock.tick(12)
		screen.fill(Bg)
		#mouse_x, mouse_y = pygame.mouse.get_pos()
		# Khởi tạo các đối tượng 
		snake = Object(total_snk, color_snake, length_snk)
		food = Object(food_total, color_food, amount_food)
		message = Message(msg, m_x, m_y)
		snake.show_object()
		food.show_object()
		message.show_messge()

		for event in pygame.event.get():
			if event.type == pygame.QUIT: # Kết thúc trò chơi
				running = False
				game_close = True
		pygame.display.flip()
	#pygame.quit()
	# chơi game thôi nào
	# Bắt các sự kiện của người chơi
	for event in pygame.event.get():
		if event.type == pygame.QUIT: # Kết thúc trò chơi
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN: # bấm chuột
			if event.button == 1 & in_click: # bấm chuột trái
				game_close = False
	#print(game_close)			
	
	pygame.display.flip()
	#pygame.display.update()
pygame.quit()
    