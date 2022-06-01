import MainGame
import pygame
class Zombie(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(Zombie, self).__init__()
        self.image = pygame.image.load('imgs/zombie.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = 800
        self.damage = 2
        self.speed = 1
        self.live = True
        self.stop = False
    #9 di chuyển zombie
    def move_zombie(self):
        if self.live and not self.stop:
            self.rect.x -= self.speed
            if self.rect.x < -80:
                #8 phương thức kết thúc game
                MainGame.GAMEOVER=True
                MainGame.MainGame().gameOver()

    #9 Xác định xem zombie có va chạm với cây không, nếu có va chạm thì gọi phương pháp tấn công cây
    def hit_plant(self):
        for plant in MainGame.MainGame.plants_list:
            if pygame.sprite.collide_rect(self,plant):
                #8  Sửa đổi trạng thái di chuyển của zombie
                self.stop = True
                self.eat_plant(plant)
    #9 Zombies tấn công cây trồng
    def eat_plant(self,plant):
        #9 hp cây trồng giảm
        plant.hp -= self.damage
        #9 Sửa đổi trạng thái của cây sau khi chết và sửa đổi trạng thái của bản đồ
        if plant.hp <= 0:
            a = plant.rect.y // 80 - 1
            b = plant.rect.x // 80
            map = MainGame.MainGame.map_list[a][b]
            map.can_grow = True
            plant.live = False
            #8Sửa đổi trạng thái di chuyển của zombie
            self.stop = False



    #9 Nạp zombie vào bản đồ
    def display_zombie(self):
        MainGame.MainGame.window.blit(self.image,self.rect)

# class zombie boss
class ZombieBoss(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(ZombieBoss, self).__init__()
        # self.image = pygame.image.load('imgs/zombie.png')
        self.image = pygame.image.load('imgs/boss1.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = 15000
        self.damage = 10
        self.speed = 1
        self.live = True
        self.stop = False
   
    def move_zombie(self):
        if self.live and not self.stop:
            self.rect.x -= self.speed
            if self.rect.x < -80:
                MainGame.GAMEOVER=True
                
                MainGame.MainGame().gameOver()

    def hit_plant(self):
        for plant in MainGame.MainGame.plants_list:
            if pygame.sprite.collide_rect(self,plant):
                self.stop = True
                self.eat_plant(plant)
    
    def eat_plant(self,plant):
        plant.hp -= self.damage
        
        if plant.hp <= 0:
            a = plant.rect.y // 80 - 1
            b = plant.rect.x // 80
            map = MainGame.MainGame.map_list[a][b]
            map.can_grow = True
            plant.live = False
            
            self.stop = False

    def display_zombie(self):
        MainGame.MainGame.window.blit(self.image,self.rect)