import pygame
from CONSTANTS import width, height, load_image, font
from map import Map
from Player import Player, Menu
from BaseObjectClasses import StaticObject, InteractionObject, DefaultThing, ThingBox


class GameLevel():
    def __init__(self, screen, main_menu):
        self.screen = screen
        self.main_menu = main_menu

        # группы спрайтов
        self.menu_sprite = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.Group()
        self.static_obj_not_in_frame = []
        self.dinamic_obj_not_in_frame = []
        self.interaction_obj_not_in_frame = []
        self.things_ogf_spr = pygame.sprite.Group()
        self.interaction_obj_sprite = pygame.sprite.Group()
        self.static_obj_sprite = pygame.sprite.Group()
        self.dinamic_obj_sprite = pygame.sprite.Group()

        # объекты
        self.map_ = Map(self.screen)  # карта
        self.player_main = Player(self.player_sprite, self.map_, self)  # игрок
        self.player_main.teleportTo(self.map_.first_player_coords[0], self.map_.first_player_coords[1])
        self.player_main.setInventaryBox(ThingBox(self.player_main.inventary_group, 10, (width // 2 - (10 * 70 + (10 + 1) * 10) // 2, height - 200), self.player_main))

        self.map_.changeCoords([-self.player_main.x_y[0] + width // 2,
                                -self.player_main.x_y[1] + height // 2 + self.player_main.image.get_height() // 2 - 10])

        self.menu = InGameMenuSprite(self.menu_sprite, self.player_main, self.screen)
        self.levelGenerator()
        self.level_state = 'playing'

    def getCoordsOnMap(self, coords):
        coords_on_map = (
            coords[0] - self.map_.coords_about_screean[0], coords[1] - self.map_.coords_about_screean[1])
        return coords_on_map

    def cleanLevel(self):
        self.screen = screen
        self.main_menu = main_menu

        # группы спрайтов
        self.menu_sprite = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.Group()
        self.static_obj_not_in_frame = []
        self.dinamic_obj_not_in_frame = []
        self.interaction_obj_not_in_frame = []
        self.things_ogf_spr = pygame.sprite.Group()
        self.interaction_obj_sprite = pygame.sprite.Group()
        self.static_obj_sprite = pygame.sprite.Group()
        self.dinamic_obj_sprite = pygame.sprite.Group()

        # объекты
        self.map_ = Map(self.screen)  # карта
        self.player_main = Player(self.player_sprite, self.map_, self)  # игрок
        self.player_main.teleportTo(self.map_.first_player_coords[0], self.map_.first_player_coords[1])
        self.player_main.setInventaryBox(
            ThingBox(self.player_main.inventary_group, 10, (width // 2 - (10 * 70 + (10 + 1) * 10) // 2, height - 200),
                     self.player_main))

        self.map_.changeCoords([-self.player_main.x_y[0] + width // 2,
                                -self.player_main.x_y[1] + height // 2 + self.player_main.image.get_height() // 2 - 10])

        self.menu = InGameMenuSprite(self.menu_sprite, self.player_main, self.screen)
        self.levelGenerator()
        self.level_state = 'playing'

    def render(self, fps, point, mouse_button_down, mouse_button_down_r):
        self.screen.fill((50, 50, 50))
        self.map_.draw()
        self.static_obj_sprite.update(fps, point)
        self.static_obj_sprite.draw(self.screen)
        self.interaction_obj_sprite.draw(self.screen)
        self.interaction_obj_sprite.update(fps, point, mouse_button_down, mouse_button_down_r)
        self.player_sprite.draw(self.screen)

        self.menu_sprite.update(fps, point)
        self.menu_sprite.draw(self.screen)
        self.player_sprite.update(fps, self.getCoordsOnMap(point), mouse_button_down)
        self.things_ogf_spr.draw(self.screen)
        self.things_ogf_spr.update(fps, point, mouse_button_down)

        if self.level_state == 'win':
            self.main_menu.game_stat = 'WinFrame'
            self.cleanLevel()
            return 0
        if self.level_state == 'die':
            self.main_menu.game_stat = 'DieFrame'
            self.cleanLevel()
            return 0

    def levelGenerator(self):
        self.static_obj_not_in_frame.append(
            StaticObject(self.static_obj_sprite, self.screen, [3 * 300 + 50, 1 * 300 - 150], self.map_,
                         'broken_portal'))
        self.static_obj_not_in_frame.append(
            StaticObject(self.static_obj_sprite, self.screen, [4 * 300, 1 * 300], self.map_,
                         'sign_1'))
        self.static_obj_not_in_frame.append(
            StaticObject(self.static_obj_sprite, self.screen, [9 * 300, 3 * 300 - 180], self.map_,
                         'sign_2'))
        self.static_obj_not_in_frame.append(
            StaticObject(self.static_obj_sprite, self.screen, [11 * 300, 3 * 300 - 180], self.map_,
                         'sign_3'))
        self.static_obj_not_in_frame.append(
            StaticObject(self.static_obj_sprite, self.screen, [16 * 300, 3 * 300 - 180], self.map_,
                         'sign_4'))
        self.static_obj_not_in_frame.append(
            StaticObject(self.static_obj_sprite, self.screen, [25 * 300, 3 * 300 - 180], self.map_,
                         'sign_5'))
        self.interaction_obj_not_in_frame.append(InteractionObject(self.interaction_obj_sprite, self.screen,
                                                                   [24 * 300 + 50, 5 * 300 - 150], self.map_,
                                                                   'bush', self.player_main))
        self.interaction_obj_not_in_frame.append(InteractionObject(self.interaction_obj_sprite, self.screen,
                                                                   [24 * 300 + 50, 3 * 300 - 150], self.map_, 'cup_of_power', self.player_main))
        self.interaction_obj_not_in_frame.append(InteractionObject(self.interaction_obj_sprite, self.screen,
                                                                   [24 * 300 + 50, 11 * 300 - 150], self.map_, 'end_portal', self.player_main))
        DefaultThing(self.things_ogf_spr, 'grass_matirial' ,[16 * 300 + 50, 3 * 300], 10, self)
        DefaultThing(self.things_ogf_spr, 'grass_matirial', [20 * 300 + 50, 3 * 300], 10, self)


class InGameMenuSprite():
    def __init__(self, group, player, screen):
        self.screen = screen
        self.menu = Menu(group, player, self.screen)

    def update(self, clock, fps_):
        self.menu.update(clock, fps_)


class MainMenu():
    def __init__(self, screen, x, y, img=None, oposit=True, exit_lambds=lambda met: exit(0)):
        self.image = None
        if not img is None:
            self.image = pygame.sprite.Group()
            self.sprite = pygame.sprite.Sprite(self.image)
            self.sprite.image = load_image(img)
            self.sprite.rect = self.sprite.image.get_rect()
            self.sprite.rect.x, self.sprite.rect.y = 0, 0
        self.screen = screen
        self.game_stat = 'Main_menu'
        # группы спрайтов
        self.buttons = pygame.sprite.Group()
        x, y = x, y
        self.b_list = []
        self.b_list.append(
            Button(self.buttons, 'interface_images/main_menu/play_b.png', x, y, lambda met: 'Playing', self))
        y = y + 50 + 390 // 2
        if oposit:
            self.b_list.append(
                Button(self.buttons, 'interface_images/main_menu/options_b.png', x, y, lambda met: 'Pause_menu', self))
            y = y + 50 + 390 // 2
        self.b_list.append(
            Button(self.buttons, 'interface_images/main_menu/exit_b.png', x, y, exit_lambds, self))

    def update(self, point, mouse_button_down):
        self.buttons.update(point, mouse_button_down)

    def pressMouseButton(self, state):
        self.game_stat = state

    def render(self):
        self.screen.fill((230, 230, 230))
        if not self.image is None:
            self.image.draw(self.screen)
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
    def __init__(self, screen, main_menu, x, y, img=None):
        super().__init__(screen, x, y, exit_lambds=lambda u: 'Main_menu', oposit=False, img=img)
        self.main_manu = main_menu

    def pressMouseButton(self, state):
        self.main_manu.pressMouseButton(state)

