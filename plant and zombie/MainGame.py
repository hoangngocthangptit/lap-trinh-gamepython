import Map
import Plant
import pygame
import random
import ZOMBIE
import sys
from time import time
from pygame.locals import *
pygame.init()
#global v
scrrr_width=800
scrrr_height =560
font = pygame.font.Font('imgs/font.TTF', 40)
GAMEOVER = False
WINGAME=False

def terminate(): # out game
    pygame.quit()
    sys.exit()

def drawText(text, font, surface, x, y): # in text ra màn hình
    TEXTCOLOR = (255, 255, 255)
    textobj = font.render(text, 1,TEXTCOLOR )
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
def waitForPlayerToPressKey():
    WINGAME=False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: #
                    terminate()
                if event.key == K_RETURN:
                    return
class MainGame():
    #2 Tạo cấp độ, điểm số, điểm số còn lại, tiền
    level = 1
    score = 0
    remnant_score = 100
    money = 200
    map_points_list = []
    map_list = []
    plants_list = []
    peabullet_list = []
    zombie_list = []
    Boss_list=[]
    count_zombie = 0
    produce_zombie = 100
    def init_window(self):
        #1 khởi tạo mô-đun hiển thị
        pygame.display.init()
        MainGame.window = pygame.display.set_mode([scrrr_width,scrrr_height])

    #2 Bản vẽ văn bản
    def draw_text(self, content, size, color):
        pygame.font.init()
        font = pygame.font.Font('imgs/font.TTF', size)
        text = font.render(content, True, color)
        return text

    #2 in ra các mẹo trợ giúp
    def load_help_text(self):
        text1 = self.draw_text('1.Leftmouse for sunflower              2.Rightmouse for shooter',
         23, (255, 150, 0))
        MainGame.window.blit(text1, (5, 5))

    #3 Khởi tạo điểm tọa độ trên map
    def init_plant_points(self):
        for y in range(1, 7):
            points = []
            for x in range(10):
                point = (x, y)
                points.append(point)
            MainGame.map_points_list.append(points)
            print("MainGame.map_points_list", MainGame.map_points_list)

    def init_map(self):# khởi tạo các pixel trên map

        for points in MainGame.map_points_list:
            temp_map_list = list()
            for point in points:
                # map = None
                if (point[0] + point[1]) % 2 == 0:
                    map = Map.Map(point[0] * 80, point[1] * 80, 0)
                else:
                    map = Map.Map(point[0] * 80, point[1] * 80, 1)
                # Thêm các ô bản đồ vào cửa sổ
                temp_map_list.append(map)
                print("temp_map_list", temp_map_list)
            MainGame.map_list.append(temp_map_list)
        print("MainGame.map_list", MainGame.map_list)

    def load_map(self): # in map ra màn hình
        for temp_map_list in MainGame.map_list:
            for map in temp_map_list:
                map.load_map()

                
    def load_plants(self):
        for plant in MainGame.plants_list:
            #6 Tối ưu hóa logic xử lý của các cây hoa
            if plant.live:
                if isinstance(plant, Plant.Sunflower):
                    plant.display_sunflower()
                    plant.produce_money()
                elif isinstance(plant, Plant.PeaShooter):
                    plant.display_peashooter()
                    plant.shot()
            else:
                MainGame.plants_list.remove(plant)

    #7 Cách tải tất cả các viên đạn
    def load_peabullets(self):
        for b in MainGame.peabullet_list:
            if b.live:
                b.display_peabullet()
                b.move_bullet()
                # v1.9 đạn bắn trúng thây ma ko
                b.hit_zombie()
                b.hit_Boss()
            else:
                MainGame.peabullet_list.remove(b)

 

    def deal_events(self):
        #8 Nhận tất cả các sự kiện
        eventList = pygame.event.get()
        #8 Duyệt qua danh sách các sự kiện và đánh giá
        for e in eventList:
            if e.type == pygame.QUIT:
                self.gameOver()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                # print('Đã nhấn nút chuột')
                print(e.pos)

                x = e.pos[0] // 80
                y = e.pos[1] // 80
                print(x, y)
                map = MainGame.map_list[y - 1][x]
                print(map.position)
                #8 thêm phán đoán tải bản đồ và phán đoán tiền khi tạo
                if e.button == 1:
                    if map.can_grow and MainGame.money >= 50:
                        sunflower = Plant.Sunflower(map.position[0], map.position[1])
                        MainGame.plants_list.append(sunflower)
                        print('plant number:{}'.format(len(MainGame.plants_list)))
                        map.can_grow = False
                        MainGame.money -= 50
                elif e.button == 3:
                    if map.can_grow and MainGame.money >= 50:
                        peashooter = Plant.PeaShooter(map.position[0], map.position[1])
                        MainGame.plants_list.append(peashooter)
                        print('plant number:{}'.format(len(MainGame.plants_list)))
                        map.can_grow = False
                        MainGame.money -= 50

    #9 khởi tạo thây ma
    def init_zombies(self):
        for i in range(1, 7):
            dis = random.randint(1,5) * 300
            zombie = ZOMBIE.Zombie(800 + dis, i * 80)
            MainGame.zombie_list.append(zombie)

    #9Tải tất cả thây ma vào bản đồ
    def load_zombies(self):
        for zombie in MainGame.zombie_list:
            if zombie.live:
                zombie.display_zombie()
                zombie.move_zombie()
                # v2.0 phương thức để gọi liệu có va chạm với thực vật hay không
                zombie.hit_plant()
                
            else:
                MainGame.zombie_list.remove(zombie)
     #10 boss
    def init_zombieBoss(self):
        for i in range(2, 6):           
            zombie = ZOMBIE.ZombieBoss(800 , i * 80)
            MainGame.Boss_list.append(zombie)

   
    def load_zombieBoss(self):
        zombie=MainGame.Boss_list[1]
        if zombie.live:
            zombie.display_zombie()
            zombie.move_zombie()
                
            zombie.hit_plant()
        else:
            # code win game
            MainGame.gameOver()
    #1 Bắt đầu trò chơi
    def start_game(self):
        #1 Cửa sổ khởi tạo
        self.init_window()
        #3 Khởi tạo tọa độ và bản đồ
        self.init_plant_points()
        self.init_map()
        #9 Gọi phương thức khởi tạo thây ma
        self.init_zombies()
        self.init_zombieBoss()
        #1 Miễn là trò chơi chưa kết thúc, nó vẫn tiếp tục lặp lại
        #mở nhạc nền
        pygame.mixer.music.load('imgs/grasswalk.mp3')
        pygame.mixer.music.play(-1,0,0)
        while True:
            #1 Kết xuất nền trắng
            MainGame.window.fill((255, 255, 255))
            #2 Văn bản được hiển thị và vị trí tọa độ
            MainGame.window.blit(self.draw_text('Monney $: {}'.format(MainGame.money), 26, (255, 100, 0)), (600, 40))
            if(MainGame.score<=1000): MainGame.window.blit(self.draw_text(
                'Level   {}         Score {}        Remainscore {}'.format(MainGame.level, 
                MainGame.score,1000- MainGame.score), 21,(255, 0, 0)), (5, 60))
            else: MainGame.window.blit(self.draw_text(
                'Level   {}         Score {}        Remainscore {}'.format(MainGame.level, 
                MainGame.score,0), 21,(255, 0, 0)), (5, 60))
            self.load_help_text()
            self.load_map()
            self.load_plants()
            self.load_peabullets()
            self.deal_events()
            self.load_zombies()
            #9 Bộ đếm tăng lên, mỗi khi đạt 100, phương thức khởi tạo thây ma được gọi
            MainGame.count_zombie += 1
            if MainGame.count_zombie == MainGame.produce_zombie:
                self.init_zombies()
                MainGame.count_zombie = 0
            if(MainGame.score >1000): 
                self.init_zombieBoss()
                self.load_zombieBoss()
            pygame.time.wait(8)
            pygame.display.update()

    #10 Kết thúc chương trình
    def gameOver(self):
        global WINGAME
        global GAMEOVER
        soundpath=["imgs/gameover.wav","imgs/win_sound.mp3"]
        sindex=0
        windowSurface = pygame.display.set_mode((scrrr_width, scrrr_height))
        windowSurface.blit((pygame.image.load('imgs/grassland.png')),(0,0))
        drawText('score: %s' % (MainGame.score), font, windowSurface, 10, 30)
        if GAMEOVER ==True:
            MainGame.window.blit(self.draw_text('game over', 50, (255, 0, 0)), (300, 200))
            drawText('YOU HAVE BEEN KISSED BY THE ZOMMBIE', font, windowSurface, (scrrr_width / 4)- 180,
             (scrrr_height / 3) + 100)
        elif WINGAME==True:
            sindex=1
            WINGAME = False
            MainGame.window.blit(self.draw_text('Win !!!', 70, (255, 0, 0)), (350, 200))
        else:
            drawText('The game is stopping', font, windowSurface, (scrrr_width / 4), (scrrr_height / 3) + 100)
            drawText('Press enter to continue or X to exit', font, windowSurface, (scrrr_width / 4) - 180, (scrrr_height / 3) + 150)
        pygame.display.update()
        pygame.mixer.music.stop()
        gameOverSound = pygame.mixer.Sound(soundpath[sindex])
        gameOverSound.play()
        waitForPlayerToPressKey()