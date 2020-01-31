import pygame
from CONSTANTS import width, height, load_image
from map import Map
from Player import Player, Menu

class Button(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.cur_frame = 0
        self.frames = []
        self.cut_sheet(Player.image_l, 1, 2)
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.y + self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        pass

class GameLevel():
    def __init__(self, screen):
        self.screen = screen
        # группы спрайтов
        self.menu_sprite = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.Group()
        self.static_obj_sprite = pygame.sprite.Group()
        self.dinamic_obj_sprite = pygame.sprite.Group()

        # объекты
        self.map_ = Map(self.screen)  # карта
        self.player_main = Player(self.player_sprite, self.map_)  # игрок
        self.player_main.teleportTo(self.map_.first_player_coords[0], self.map_.first_player_coords[1])

        self.map_.changeCoords([-self.player_main.x_y[0] + width // 2,
                                -self.player_main.x_y[1] + height // 2 + self.player_main.image.get_height() // 2 - 10])

        self.menu = MenuSprite(self.menu_sprite, self.player_main, self.screen)

    def render(self, fps):
        self.screen.fill((50, 50, 50))
        self.map_.draw()
        self.player_sprite.draw(self.screen)
        self.menu_sprite.update(fps)
        self.menu_sprite.draw(self.screen)

    def update(self, fps):
        self.player_sprite.update(fps)



class MenuSprite():
    def __init__(self, group, player, screen):
        self.screen = screen
        self.menu = Menu(group, player, self.screen)

    def update(self, clock, fps_):
        self.menu.update(clock, fps_)
