import pygame, sys
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
GREEN = (0, 200, 0)
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
# Biến sử dụng trong hàm thông báo
size_font = 30
arialFont = pygame.font.SysFont("Arial", size_font)
font_color = BLACK # màu của font
msg = ""
"""mesg = arialFont.render(msg, True, font_color)
textRect = mesg.get_rect()
def show_message(m_x, m_y):
	textRect.center(m_x, m_y)
	pygame.blit(mesg, textRect)"""
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
class Message:
	def __init__(self, msg, color, x, y):
		self.msg = msg
		self.color = color
		self.x = x
		self.y = y
	# Xây dựng hàm thông báo	
	def show_messge(self):
		#for m in self.msg:
		mesg = arialFont.render(self.msg, True, self.color)
		textRect = mesg.get_rect()
		textRect.center = (self.x, self.y)
		"""self.w = textRect[2]
		self.h = textRect[3]"""
		screen.blit(mesg, textRect)
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
#game_close = False 
count_pause = 0
# Biến khi rắn săn mồi
finish_eat = False
level =1 

#m_x, m_y = 300, 50 # tọa độ xuất hiện
game_pause = False
game_close = True
while running:		
	clock.tick(12) # 12 hình trên giây
	screen.fill(Bg) # nhất định phải đưa vào, không sẽ tạo vết (bóng) của các ojb
	#pygame.mixer.Sound.play(bg_sound)
	#pygame.mixer.Sound.play(eat_sound)
	#pygame.draw.rect(screen, snake.color, (snake.x, snake.y, snake.size, snake.size))
	#print(message)
	mouse_x, mouse_y = pygame.mouse.get_pos()
	# Khởi tạo các đối tượng 
	#snake = Object(total_snk, color_snake, length_snk)
	#food = Object(food_total, color_food, amount_food)
	m_start = f"BeGin"
	msg_start = Message(m_start, font_color, 300, 270)
	m_continue = f"Continue"
	msg_continue = Message(m_continue, font_color, 300, 330)
	list_msg = [msg_start, msg_continue]
	# show các đối tượng trên màn hình
	#snake.show_object()
	#food.show_object()
	for msg in list_msg:
		
		#msg_continue.show_messge()
		if (msg.x-50<=mouse_x)&(mouse_x<=msg.x+50)\
			&(msg.y-10<=mouse_y)&(mouse_y<=msg.y+10):
			font_color = GREEN
			in_click = True
			pygame.draw.line(screen, font_color, (msg.x-msg.w/2, msg.y+msg.h/2+5),(msg.x+msg.w/2, msg.y+msg.h/2+5))
		else:
			font_color = BLACK
			in_click = False
		msg.show_messge()
	while game_close == False:
		clock.tick(12) # 12 hình trên giây
		screen.fill(Bg) # nhất định phải đưa vào, không sẽ tạo vết (bóng) của các ojb
		mouse_x, mouse_y = pygame.mouse.get_pos()# lấy tọa độ của chuột
		# Tạo các đối tượng của game
		snake = Object(total_snk, color_snake, length_snk)
		food = Object(food_total, color_food, amount_food)
		msg = f"hscore: {hscore}   " + f"score: {score}"
		message = Message(msg, font_color, 300, 50)
		
		# show các đối tượng trên màn hình
		snake.show_object()
		food.show_object()
		message.show_messge()
		# thay đổi màu chữ khi đưa chuột đến
		if (200<=mouse_x)&(mouse_x<=400)\
		&(40<=mouse_y)&(mouse_y<=60):
			font_color = GREEN
		# chơi game thôi nào
		# Bắt các sự kiện của người chơi
		for event in pygame.event.get():
			if event.type == pygame.QUIT: # Kết thúc trò chơi
				game_close = True
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN: # bấm chuột
				if event.button == 1: # bấm chuột trái
					# thay đổi màu sắc của rắn
					if (snk_x<=mouse_x) & (mouse_x<=snk_x+size)\
					& (snk_y<=mouse_y) & (mouse_y<=snk_y+size):
						color_snake = (r(0,255),r(0,255),r(0,255))
					# thay đổi màu màn hình
					else:
						Bg = (r(0,255),r(0,255),r(0,255))
			# bắt các sự kiện bấm các phím di chuyển -->; <--
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					left = False
					right = True
					count += 1
				if event.key == pygame.K_LEFT:
					right = False
					left = True
					count += 1
				if event.key == pygame.K_SPACE:
					if game_pause == True:
						score -= 1
						count_pause += 1
						game_pause = (3 - count_pause) <=0
						game_close = (4 - count_pause < 0) & (score < 0) 
		snake_head = [] # format list snake
		# Thuật toán di chuyển
		# luôn rẽ phải so với hướng di chuyển
		if right: 
			if count%2 == 1:
				snk_x += (1 - 2*((count//2)%2))*delta
			else:
				snk_y += (2*((count//2)%2) - 1)*delta
		# luôn rẽ trái so với hướng di chuyển
		elif left:
			if count%2 == 1:
				snk_x += (2*((count//2)%2) - 1)*delta
			else:
				snk_y += (2*((count//2)%2) - 1)*delta
		# cập nhật lại tọa độ sau di chuyển và gọi hàm đóng gói
		snake_head.append(snk_x)
		snake_head.append(snk_y)
		total_snk.append(snake_head)
		if len(total_snk)>length_snk:
				del total_snk[0]
		
		# rắn ăn thức ăn và cách tính điểm
		for food in food_total:
			if (food[0]-size<=snk_x)&(snk_x<=food[0]+size)\
				&(food[1]-size<=snk_y)&(snk_y<=food[1]+size):
				food_total.remove(food)
				#amount_food -= 1 # nghiên cứu thêm
				length_snk += 1
				score += 1
				if score > hscore:
					hscore = score
				finish_eat = True
			else:
				finish_eat = False
		if finish_eat == True:
			# cập nhật lại vị trí của thức ăn
			for i in range(amount_food):
				#for j in range(2):
				food[0] = 50*r(1, 11)
				food[1] = 80+ 40*r(0, 12)
				food_total.append([food[0], food[1]])
			#print("-"*10)
		#print(food_total)
		if len(food_total)>amount_food:
			del	food_total[-1]
		# cứ sau 5 lần ăn thức ăn thì số lượng thức ăn tăng lên
		if (score % 5 == 0) & (score > escape):# thoát khỏi vòng lặp khi score chia hết cho 5
			amount_food += 1
			level += 1
			escape = score +1 # gán lại escape để phủ định conditional
		#food_total.append(food_first)
		#print(food_total)    
		#print(total_snk) 
		# Trường hợp rắn chạm tường          
		for i in [0, 590]:
			for j in snake_head:
				if j == i:
					game_pause = True
		# Trường hợp cắn đuôi			
		if length_snk >=5:
			for snk in snake.total[1:]:
				if snk == snake.total[0]:
					game_pause = True
		# khi tạm dừng game			
		if game_pause:
			if count_pause < 3:
				msg_gclose = f"you lose! Please press space key to continue!"
			elif count_pause >=3 or (score < 0):
				msg_gpause= f"GameOver"
			message_gpause = Message(msg_gclose, RED, 300, 200)
			message_gpause.show_messge()
			#message.show_messge(msg, BLACK, 300, 200)
			#delta = 0
			snk_x, snk_y = 300, 300
			length_snk = 1
			amount_food = 1
			#total_snk = total_snk[-2]
		pygame.display.flip()
		
	for event in pygame.event.get():
		if event.type == pygame.QUIT: # Kết thúc trò chơi
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN: # bấm chuột
			if event.button == 1 & in_click: # bấm chuột trái
				game_close = False
							
	pygame.display.flip()

pygame.quit()
sys.exit()

    