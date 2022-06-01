import MainGame
import pygame
IMAGE_PATH = 'imgs/'

class Map():
    #3 Lưu tên của ảnh map có màu sắc khác nhau
    map_names_list = [IMAGE_PATH + 'map1.png', IMAGE_PATH + 'map2.png']
    #3hởi tạo bản đồ
    def __init__(self, x, y, img_index):
        self.image = pygame.image.load(Map.map_names_list[img_index])
        self.position = (x, y)
        # Có thể trồng nó không
        self.can_grow = True
    #3 Tải bản đồ
    def load_map(self):
        MainGame.MainGame.window.blit(self.image,self.position)