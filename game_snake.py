import pygame, sys
from random import randint as r
from tkinter import *
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Project_Codgym - Snake_Game")
screen.fill([100, 100, 100]) # màu nền ban đầu
# Tạo các biến màu
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
BROWN = (100, 0, 0)
PINK = (255, 100, 255)
ORANGE = (255, 100, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
color_Bg = GREY
# Tạo tần số quét mành
clock = pygame.time.Clock()
# Tạo các lớp đối tượng
# Lớp rắn, thức ăn, vật cản 
# Khởi tạo ban đầu cho các đối tượng	
# Rắn
snk_x, snk_y = 300, 300
snk_total = [] # toàn bộ con rắn lúc đầu
length_snk = 1	# độ dài rắn
color_snake = BLACK
# Thức ăn
food_x, food_y = 100, 100 # tọa độ của thức ăn
food_first = [food_x, food_y] # thức ăn ban đầu
food_total = [food_first]
color_food = GREEN # màu thức ăn luôn thay đổi
amount_food = 1
# vật cản
global trap_x
global trap_y
trap_x, trap_y = 500, 500
trap_total = [[trap_x, trap_y], [trap_x+10, trap_y+10]]
color_trap = ORANGE
amount_trap = 2
speed = 10	# tốc độ di chuyển
size = 10	# kích thước (dùng chung cho lớp)
# định nghĩa lớp
class Object:
	def __init__(self, object_total, color):
		self.total = object_total
		self.color = color
	def show_object(self):
		for obj in self.total:
			pygame.draw.rect(screen, self.color, (obj[0], obj[1], size, size))	
# Tạo lớp Message
# khởi tạo ban đầu 
font_color_begin = BLACK # màu của font
font_color_continue = BLACK
font_color_level = BLACK
font_color_escape = BLACK
in_click_begin = False
in_click_continue = False
in_click_escape = False
# định nghĩa lớp Message
class Message:
	def __init__(self, msg, size_font, font_color, x, y):
		self.msg = msg
		self.size_font = size_font
		self.color = font_color
		self.x = x
		self.y = y
	# Xây dựng hàm thông báo	
	def show_messge(self):
		arialFont = pygame.font.SysFont("Arial", self.size_font)
		mesg = arialFont.render(self.msg, True, self.color)
		self.textRect = mesg.get_rect()
		self.textRect.center = (self.x, self.y)
		screen.blit(mesg, self.textRect)
# Tạo các biến âm thanh
bg_sound = pygame.mixer.Sound("sound_game/background.mp3")
food_sound = pygame.mixer.Sound("sound_game/food.mp3")
eat_sound = pygame.mixer.Sound("sound_game/eat.mp3")
win_sound = pygame.mixer.Sound("sound_game/win.mp3")
g_pause_sound = pygame.mixer.Sound("sound_game/game_pause.mp3")
GameOver_sound = pygame.mixer.Sound("sound_game/gameover.mp3")
# Biến chương trình chơi
running = True # chạy chương trình chính
game_close = True # chạy chương trình chơi
right = False # Biến rẽ phải
left = False  # Biến rẽ phải
R = True # Biến rẽ phải
L = True # Biến rẽ trái
# Biến khi người chơi thua
game_pause = False
count = 0	# đếm chuyển động 
count_pause = 0 # đếm số lần ứng mạng
score, hscore = 0, 0 # điểm và điểm cao
level = 1 # cấp độ game
escape = 0 # biến thoát khỏi vòng lặp
# Biến khi rắn săn mồi
finish_eat = False

while running:		
	clock.tick(12) # 12 hình trên giây
	screen.fill(color_Bg) # nhất định phải đưa vào, không sẽ tạo vết (bóng) của các ojb
	m_escape = "Click here or click X to quit game, please!"
	msg_escape = Message(m_escape, 30, font_color_escape, 300, 350)
	mouse_x, mouse_y = pygame.mouse.get_pos()
	# kiểm tra khi kết thúc game
	if (3 - count_pause < 0) or (score < 0):
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN: 
				if event.button == 1 & in_click_escape:
					running = False
		m_end = "GameOver"
		msg_end = Message(m_end, 80, RED, 280, 300)
		msg_end.show_messge()
		msg_escape.show_messge()
		if (msg_escape.x-msg_escape.textRect[2]/2<=mouse_x)&(mouse_x<=msg_escape.x+msg_escape.textRect[2]/2)\
		&(msg_escape.y-msg_escape.textRect[3]/2<=mouse_y)&(mouse_y<=msg_escape.y+msg_escape.textRect[3]/2):
			# thay đổi màu và gạch chân
			font_color_escape = GREEN
			in_click_escape = True
			pygame.draw.line(screen, GREEN, (msg_escape.textRect[0],msg_escape.textRect[1]+msg_escape.textRect[3]-1),\
					(msg_escape.textRect[0]+msg_escape.textRect[2],msg_escape.textRect[1]+msg_escape.textRect[3]-1), 2)
		else:
			font_color_escape = BLACK
			in_click_escape = False
		pygame.mixer.Sound.play(GameOver_sound)
		
	# khi thắng cuộc
	elif score >= 50:
		m_win = "You Win!"
		msg_win = Message(m_win, 80, PINK, 300, 300)
		msg_win.show_messge()
		pygame.mixer.Sound.play(win_sound)
	# khi bắt đầu khởi động
	else:
		m_start = f"BeGin"
		msg_start = Message(m_start, 50, font_color_begin, 300, 270)
		msg_start.show_messge()
		m_continue = f"Continue"
		msg_continue = Message(m_continue, 50, font_color_continue, 300, 330)
		msg_continue.show_messge()
		# kiểm tra khi chuột ở vị trí của các lựa chọn
		# kiểm tra chuột ở Begin
		if (msg_start.x-msg_start.textRect[2]/2<=mouse_x)&(mouse_x<=msg_start.x+msg_start.textRect[2]/2)\
		&(msg_start.y-msg_start.textRect[3]/2<=mouse_y)&(mouse_y<=msg_start.y+msg_start.textRect[3]/2):
			# thay đổi màu và gạch chân
			font_color_begin = BLUE
			in_click_begin = True
			pygame.draw.line(screen, BLUE, (msg_start.textRect[0],msg_start.textRect[1]+msg_start.textRect[3]-3),\
					(msg_start.textRect[0]+msg_start.textRect[2],msg_start.textRect[1]+msg_start.textRect[3]-3), 3)
		else:
			font_color_begin = BLACK
			in_click_begin = False
		# kiểm tra chuột ở vị trí contunue
		if (msg_continue.x-msg_continue.textRect[2]/2<=mouse_x)&(mouse_x<=msg_continue.x+msg_continue.textRect[2]/2)\
			&(msg_continue.y-msg_continue.textRect[3]/2<=mouse_y)&(mouse_y<=msg_continue.y+msg_continue.textRect[3]/2):
				# thay đổi màu và gạch chân
				font_color_continue = BLUE
				in_click_continue = True
				pygame.draw.line(screen, BLUE, (msg_continue.textRect[0],msg_continue.textRect[1]+msg_continue.textRect[3]-3),\
						(msg_continue.textRect[0]+msg_continue.textRect[2],msg_continue.textRect[1]+msg_continue.textRect[3]-3), 3)
		else:
			font_color_continue = BLACK
			in_click_continue = False
	
	while game_close == False:
		# luôn kiểm tra xem có thua không
		game_close = (3 - count_pause < 0) or (score < 0) 
		clock.tick(15) # 12 hình trên giây
		screen.fill(color_Bg) # nhất định phải đưa vào, không sẽ tạo vết (bóng) của các ojb
		#pygame.mixer.Sound.play(bg_sound) - do chất lượng nhạc thấp nên chưa muốn đưa vào
		mouse_x, mouse_y = pygame.mouse.get_pos()# lấy tọa độ của chuột
		# Tạo các đối tượng của game
		snake = Object(snk_total, color_snake)
		color_food = (r(0,255), 255, r(0,255))
		food = Object(food_total, color_food)
		trap = Object(trap_total, color_trap)
		msg_score = f"hscore: {hscore}   " + f"score: {score}"
		msg_level = f"Level {level}"
		messg_score = Message(msg_score, 30, YELLOW, 300, 50)
		messg_level = Message(msg_level, 30, BROWN, 300, 100)
		# show các đối tượng trên màn hình
		snake.show_object()
		food.show_object()
		trap.show_object()
		messg_score.show_messge()
		messg_level.show_messge()
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
						color_Bg = (r(0,255),r(0,255),r(0,255))
			# sự kiện bấm các phím di chuyển --> ; <--
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					left = False
					right = True
					R = not R
					count += 1
				if event.key == pygame.K_LEFT:
					right = False
					left = True
					L = not L
					count += 1
				if event.key == pygame.K_SPACE:
					if game_pause == True:
						score -= 1
						count_pause += 1
						game_pause = ((2 - count_pause) < 0) or (score < 0)
						
		snake_head = [] # format list snake
		# Thuật toán di chuyển
		# luôn rẽ phải so với hướng di chuyển
		if right: 
			if count%2 == 1:
				if R == True:
					snk_x += (2*((count//2)%2) - 1)*speed
				else:
					snk_x += (1 - 2*((count//2)%2))*speed
			else:
				if R == True:
					snk_y += (2*((count//2)%2) - 1)*speed
				else: 
					snk_y += (1 - 2*((count//2)%2))*speed
		# luôn rẽ trái so với hướng di chuyển
		elif left:
			if count%2 == 1:
				if L == True:
					snk_x += (1 - 2*((count//2)%2))*speed
				else: 
					snk_x += (2*((count//2)%2) - 1)*speed
			else:
				if L == True:
					snk_y += (2*((count//2)%2) - 1)*speed
				else:
					snk_y += (1 - 2*((count//2)%2))*speed
		# cập nhật lại tọa độ sau di chuyển và đóng gói đối tượng
		snake_head.append(snk_x)
		snake_head.append(snk_y)
		snk_total.append(snake_head)
		# luôn duy trì độ dài rắn
		if len(snk_total)>length_snk:
			del snk_total[0]
		# rắn ăn thức ăn và cách tính điểm
		for food in food_total:
			if (food[0]-size<=snk_x)&(snk_x<=food[0]+size)\
				&(food[1]-size<=snk_y)&(snk_y<=food[1]+size):
				food_total.remove(food)
				length_snk += 1
				score += 1
				pygame.mixer.Sound.stop(bg_sound)
				pygame.mixer.Sound.play(eat_sound)
				if score > hscore:
					hscore = score
				finish_eat = True
			else:
				finish_eat = False
		if finish_eat == True:
			# cập nhật lại vị trí của thức ăn
			for i in range(amount_food):
				food[0] = 50*r(1, 11)
				food[1] = 80+ 40*r(0, 12)
				food_total.append([food[0], food[1]])
		# Luôn duy trì số lượng thức ăn cố định
		if len(food_total)>amount_food:
			del	food_total[-1]
		# cứ sau 10 lần ăn thức ăn thì load âm thanh mới và thoát ngay sau đó
		if (score % 10 == 0) & (score > escape):# thoát khỏi vòng lặp khi score chia hết cho 10
			pygame.mixer.Sound.stop(bg_sound)
			pygame.mixer.Sound.play(food_sound)
			color_trap = (255, r(100, 255), r(100, 255))
			escape = score +1 # gán lại escape để phủ định conditional
		# cập nhật giá trị của các biến so với điểm số			
		amount_food = 1 + score//10
		amount_trap = 2*(1 + (score//10))
		if score >= 0:
			level = 1 + score//10 
			speed = 10 + 5*((score//10)//4 + (score//10)//3)
			size = 10 + 5*((score//10)//4 + (score//10)//3)
		else:
			level = 1
			speed = 10
			size = 10
		# Từ level 2 trở đi sẽ thay đổi vị trí của vật cản sau mỗi lẫn ăn		
		if (level >= 2) & finish_eat:
			# luôn đảm bảo rằng vật cản xuất hiện với khoảng cách so với rắn = một số nguyên lần của tốc độ
			trap_x = snk_x + speed*r((-snk_x)//speed, (600 - 2*speed - snk_x)//speed)
			trap_y = snk_y + speed*r(((80 - snk_y)//speed), (600 - 2*speed - snk_y)//speed)
			trap_total.append([trap_x, trap_y])
			trap_total.append([trap_x+size, trap_y+size])
		# Luôn duy trì số lượng vật cản 
		if len(trap_total) > amount_trap:
			trap_total = trap_total[2:]
		
		if score >= 50:
			game_close = True
		# Trường hợp rắn chạm tường 
		for snk in snake.total: 
			for j in snk:        
				if ((j > - speed) & (j < speed)) or ((j > 600 - speed) & (j < 600 +speed)):
					game_pause = True
		# Trường hợp cắn đuôi			
		if length_snk >=5:
			for snk in snake.total[1:]:
				if snk == snake.total[0]:
					game_pause = True
		# Trường hợp rắn chạm vào vật cản
		for tr in trap.total:
			for snk in snake.total:
				if (tr[0]-size<snk[0])&(snk[0]<tr[0]+size)&\
				   (tr[1]-size<snk[1])&(snk[1]<tr[1]+ size):
					game_pause = True
		# khi tạm dừng game			
		if game_pause == True:
			snk_x, snk_y = trap_x + speed*((300-trap_x)//speed), trap_y + speed*((300-trap_y)//speed)
			snk_total = []	
			amount_food = 1
			if (count_pause >= 3) or (score < 0):
				break
			else:	
				pygame.mixer.Sound.stop(bg_sound)
				pygame.mixer.Sound.play(g_pause_sound)			
				m_gpause= "You lose! Press space key to continue!"
			msg_gpause = Message(m_gpause, 40, BLACK, 300, 200)
			msg_gpause.show_messge()
		else: 
			pygame.mixer.Sound.stop(g_pause_sound)
		# ghi hscore, score, snk_x, snk_y vào một file
		with open("parameters.txt", "w") as f:
			for i in [score, hscore, snk_x, snk_y]:
				f.write(f"{i}" + "\n")				
		pygame.display.flip()
	for event in pygame.event.get():
		if event.type == pygame.QUIT: # Kết thúc trò chơi
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN: # bấm chuột
			# Khi chọn begin
			if event.button == 1 & in_click_begin:
				game_close = False
			# Khi chọn continue
			elif event.button == 1 & in_click_continue:
				game_close = False
				# load thông số từ file đã lưu
				with open("parameters.txt", "r") as f:
					remembers = f.read().split("\n")
					if "" in remembers:
						remembers.remove("")
					score = int(remembers[0])
					hscore = int(remembers[1])
					snk_x = int(remembers[2])
					snk_y = int(remembers[3])
	pygame.display.flip()
pygame.quit()
sys.exit()    # 270 dòng code