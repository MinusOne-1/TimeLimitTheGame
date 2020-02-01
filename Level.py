import pygame
from CONSTANTS import width, height, load_image, font
from map import Map
from Player import Player, Menu
from BaseObjectClasses import StaticObject


class GameLevel():
    def __init__(self, screen):
        self.screen = screen
        # группы спрайтов
        self.menu_sprite = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.Group()
        self.static_obj_not_in_frame = []
        self.dinamic_obj_not_in_frame = []
        self.static_obj_sprite = pygame.sprite.Group()
        self.dinamic_obj_sprite = pygame.sprite.Group()

        # объекты
        self.map_ = Map(self.screen)  # карта
        self.player_main = Player(self.player_sprite, self.map_)  # игрок
        self.player_main.teleportTo(self.map_.first_player_coords[0], self.map_.first_player_coords[1])

        self.map_.changeCoords([-self.player_main.x_y[0] + width // 2,
                                -self.player_main.x_y[1] + height // 2 + self.player_main.image.get_height() // 2 - 10])

        self.menu = InGameMenuSprite(self.menu_sprite, self.player_main, self.screen)
        self.levelGenerator()

    def render(self, fps, point):
        self.screen.fill((50, 50, 50))
        self.map_.draw()
        self.static_obj_sprite.update(fps, point)
        self.player_sprite.draw(self.screen)
        self.static_obj_sprite.draw(self.screen)
        self.menu_sprite.update(fps, point)
        self.menu_sprite.draw(self.screen)

    def update(self, fps):
        self.player_sprite.update(fps)

    def levelGenerator(self):
        self.static_obj_not_in_frame.append(
            StaticObject(self.static_obj_sprite, self.screen, [3 * 300 + 50, 1 * 300 - 150], self.map_,
                         'broken_portal'))


class InGameMenuSprite():
    def __init__(self, group, player, screen):
        self.screen = screen
        self.menu = Menu(group, player, self.screen)

    def update(self, clock, fps_):
        self.menu.update(clock, fps_)


class MainMenu():
    def __init__(self, screen, x, y):
        self.screen = screen
        self.game_stat = 'Main_menu'
        # группы спрайтов
        self.buttons = pygame.sprite.Group()
        x, y = x, y
        self.b_list = []
        self.b_list.append(
            Button(self.buttons, 'interface_images/main_menu/play_b.png', x, y, lambda met: 'Playing', self))
        y = y + 50 + 390 // 2
        self.b_list.append(
            Button(self.buttons, 'interface_images/main_menu/options_b.png', x, y, lambda met: 'Pause_menu', self))
        y = y + 50 + 390 // 2
        self.b_list.append(
            Button(self.buttons, 'interface_images/main_menu/exit_b.png', x, y, lambda met: exit(0), self))

    def update(self, point, mouse_button_down):
        self.buttons.update(point, mouse_button_down)

    def pressMouseButton(self, state):
        self.game_stat = state

    def render(self):
        self.screen.fill((230, 230, 230))
        self.buttons.draw(self.screen)


class Button(pygame.sprite.Sprite):
    def __init__(self, group, image, x, y, func, menu):
        self.menu = menu
        super().__init__(group)
        self.cur_frame = 0
        self.frames = []
        self.cut_sheet(load_image(image), 1, 2)
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.method = func

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.y + self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def method(self):
        pass

    def update(self, point, mouse_button_down):
        if self.rect.collidepoint(point):
            self.cur_frame = 1
            if mouse_button_down:
                self.menu.pressMouseButton(self.method(True))
        else:
            self.cur_frame = 0
        self.image = self.frames[self.cur_frame]


class PauseMenu(MainMenu):
    def __init__(self, screen, main_menu, x, y):
        super().__init__(screen, x, y)
        self.main_manu = main_menu

    def pressMouseButton(self, state):
        self.main_manu.pressMouseButton(state)

    def render(self):
        self.screen.fill((0, 0, 0))
        self.buttons.draw(self.screen)
