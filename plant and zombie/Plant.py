import pygame
import Map
import MainGame
import Plant
scrrr_width=800
scrrr_height =560
LOG = 'File:{}NotFound:{}Error'.format(__file__,__name__)
class Plant(pygame.sprite.Sprite):
    def __init__(self):
        super(Plant, self).__init__()
        self.live=True

    # Tải hình ảnh
    def load_image(self):
        if hasattr(self, 'image') and hasattr(self, 'rect'):
            MainGame.window.blit(self.image, self.rect)
        else:
            print(LOG)
#5 Hoa hướng dương
class Sunflower(Plant):
    def __init__(self,x,y):
        super(Sunflower, self).__init__()
        self.image = pygame.image.load('imgs/sunflower.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.price = 50
        self.hp = 100
        #5 Bộ đếm thời gian
        self.time_count = 0

    #5 Tạo ra ánh sáng mặt trời
    def produce_money(self):
        self.time_count += 1
        if self.time_count == 25:
            MainGame.MainGame.money += 5
            self.time_count = 0
    #5 Hướng dương được thêm vào cửa sổ
    def display_sunflower(self):
        MainGame.MainGame.window.blit(self.image,self.rect)

#6 bắn đậu
class PeaShooter(Plant):
    def __init__(self,x,y):
        super(PeaShooter, self).__init__()
        # self.image 为一个 surface
        self.image = pygame.image.load('imgs/peashooter.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.price = 50
        self.hp = 200
        self.shot_count = 0

    def shot(self):
        should_fire = False
        for zombie in MainGame.MainGame.zombie_list:
            if zombie.rect.y == self.rect.y and zombie.rect.x < 800 and zombie.rect.x > self.rect.x:
                should_fire = True
        for zombie in MainGame.MainGame.Boss_list:
            if zombie.rect.y + 165 >= self.rect.y  and zombie.rect.x < 800 and zombie.rect.x > self.rect.x:
                should_fire = True
        #6 th nếu còn sống
        if self.live and should_fire:
            self.shot_count += 1
            if self.shot_count == 25:
                #6 Tạo một viên đạn dựa trên vị trí hiện tại của người bắn đậu
                peabullet = PeaBullet(self)
                #6 Lưu trữ dấu đầu dòng trong danh sách dấu đầu dòng
                MainGame.MainGame.peabullet_list.append(peabullet)
                self.shot_count = 0

    #6 vẽ bắn đậu vào cửa sổ
    def display_peashooter(self):
        MainGame.MainGame.window.blit(self.image,self.rect)
class PeaBullet(pygame.sprite.Sprite):
    def __init__(self,peashooter):
        self.live = True
        self.image = pygame.image.load('imgs/peabullet.png')
        self.damage = 60
        self.speed  = 10
        self.rect = self.image.get_rect()
        self.rect.x = peashooter.rect.x + 60
        self.rect.y = peashooter.rect.y + 15

    def move_bullet(self):
        #7 Di chuyển sang phải trong vùng màn hình
        if self.rect.x < scrrr_width:
            self.rect.x += self.speed
        else:
            self.live = False

    def nextLevel(self):
        MainGame.MainGame.score += 20
        MainGame.MainGame.remnant_score -=20
        for i in range(1,100):
            if MainGame.MainGame.score==100*i and MainGame.MainGame.remnant_score==0:
                    MainGame.MainGame.remnant_score=100*i
                    MainGame.MainGame.level+=1
                    MainGame.MainGame.produce_zombie+=50
    #7 va chạm của đạn và zombie
    def hit_zombie(self):
        for zombie in MainGame.MainGame.zombie_list:
            if pygame.sprite.collide_rect(self,zombie):
                #Sau khi bắn trúng zombie,sửa đổi trạng thái của viên đạn
                self.live = False
                #chinh hp zombie
                zombie.hp -= self.damage
                if zombie.hp <= 0:
                    zombie.live = False
                    self.nextLevel()
     #8danh boss
    def hit_Boss(self):
        for zombie in MainGame.MainGame.Boss_list:
            if pygame.sprite.collide_rect(self,zombie):
                self.live = False
                zombie.hp -= self.damage
                if zombie.hp <= 0:
                    zombie.live = False
                    MainGame.WINGAME=True
                    MainGame.MainGame().gameOver()
    def display_peabullet(self):
        MainGame.MainGame.window.blit(self.image,self.rect)
   
