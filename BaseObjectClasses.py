import pygame
from CONSTANTS import height, width, static_obj_param, load_image, font


class BaseObject(pygame.sprite.Sprite):

    def __init__(self, group, x_y, map_):
        super().__init__(group)
        self.i_j_k = 0  # счётчик итераций, для кадров.
        self.x_y = x_y  # координаты относительно карты
        self.map = map_  # карта
        self.naptr = 0  # направление персонажа относительно север-юг-запад-восток:
        #  0 - Юг, 1 - запад, 2 - север, 3 - восток
        self.frames = [[], [], [], []]
        self.frames_in_itter = 30  # кол-во иттераций на один кадр
        self.cur_frame = (0, 0)  # выделеный кадр анимации
        self.num_of_anim = 0  # количество анимаций

        # параметры объекта
        self.health = 200  # здоровье

    def cut_sheet(self, sheet, columns, rows, ots, napr):
        self.rect = pygame.Rect(0, ots, sheet.get_width() // columns,
                                sheet.get_height() // (rows * self.num_of_anim))
        self.frames[napr].append([])
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.y + self.rect.h * j)
                self.frames[napr][- 1].append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def getCoordsInFrame(self):
        coords_on_screen = (
        self.map.coords_about_screean[0] + self.x_y[0], self.map.coords_about_screean[1] + self.x_y[1])
        return coords_on_screen



class StaticObject(BaseObject):
    def __init__(self, group, screen, x_y, map_, obj_name):
        self.screen = screen
        super().__init__(group, x_y, map_)
        self.param = static_obj_param[obj_name]
        self.num_of_anim = self.param['num_of_anim']
        self.images = [load_image(i) for i in self.param['images'][:1]]

        for i in range(0, (self.num_of_anim + 1) * self.param['image_w'], self.param['image_w'] * self.param['rows']):
            self.cut_sheet(self.images[0], self.param['colomns'],  self.param['rows'], i, 0)

        self.image = self.frames[self.naptr][self.cur_frame[0]][self.cur_frame[1]]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.getCoordsInFrame()

    def update(self, fps, point):
        self.i_j_k += 1
        self.rect.x, self.rect.y = self.getCoordsInFrame()
        self.collide(point)
        if self.i_j_k % self.frames_in_itter == 0:
            self.cur_frame = (
                self.cur_frame[0], (self.cur_frame[1] + 1) % len(self.frames[self.naptr][self.cur_frame[0]]))
            self.image = self.frames[self.naptr][self.cur_frame[0]][self.cur_frame[1]]

    def collide(self, point):
        if self.rect.collidepoint(point):
            text = font.render(self.param['comment'], 1, (83, 189, 104))
            text_x = self.rect.x + (self.rect.w - text.get_width()) // 2
            text_y = self.rect.y - 50
            self.screen.blit(text, (text_x, text_y))
