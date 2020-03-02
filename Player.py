import math
import pygame

from BaseObjectClasses import DefaultThing, UsebaleThings
from CONSTANTS import width, height, load_image, font, thing_param, font1
from Level import Button


class Player(pygame.sprite.Sprite):
    # картинки ерсонажа с разных сторон
    image_l = load_image('player_character/jaylf_sprite_l.png')
    image_r = load_image('player_character/jaylf_sprite_r.png')
    image_d = load_image('player_character/jaylf_sprite_d_stay.png')
    image_u = load_image('player_character/jaylf_sprite_u_stay.png')

    def __init__(self, group, map_, level):
        super().__init__(group)
        self.inventary_group = pygame.sprite.Group()
        self.inventary = ''
        self.level = level
        self.map = map_
        self.naptr = 1  # направление персонажа относительно север-юг-запад-восток:
        #  0 - Юг, 1 - запад, 2 - север, 3 - восток
        self.frames = [[], [], [], []]
        self.frames_in_itter = 10  # кол-во иттераций на один кадр
        self.cur_frame = (0, 0)  # выделеный кадр анимации
        self.num_of_anim = 3  # количество анимаций

        # разрезка западного направления
        for i in range(0, (self.num_of_anim) * 466 - 233 + 1, 466):
            self.cut_sheet(Player.image_l, 5, 2, i, 1)
        # разрезка восточного направления
        for i in range(0, (self.num_of_anim) * 466 - 233 + 1, 466):
            self.cut_sheet(Player.image_r, 5, 2, i, 3)
        # нарезка переднего направления
        for i in range(0, (self.num_of_anim) * 466 - 233 + 1, 466):
            self.cut_sheet(Player.image_d, 5, 2, i, 0)
        # нарезка pflytuj направления
        for i in range(0, (self.num_of_anim) * 466 - 233 + 1, 466):
            self.cut_sheet(Player.image_u, 5, 2, i, 2)
        self.image = self.frames[self.naptr][self.cur_frame[0]][self.cur_frame[1]]
        self.rect = self.image.get_rect()
        self.rect.x = width // 2 - self.image.get_width() // 2
        self.rect.y = height // 2 - self.image.get_height() // 2

        # Основные параметры
        self.positive_eff = []  # позитивные эффекты
        self.negative_eff = []  # негативные эффекты
        self.health = 200  # здоровье
        self.madness = 0  # безумие
        self.hunger = 0  # голод
        self.darkness = 50  # тёмная магическая сила
        self.light = 50  # светлая магическая сила

        # максимальные парамерты
        self.health_max = 200
        self.madness_max = 200
        self.hunger_max = 200

        # Cлужебные параметры
        self.equipped = None
        self.i_may_go = False
        self.speed = 8  # скорость
        self.force = 40  # дальность внешнего взаимодействия объекта
        self.i_j_k = 0  # счётчик итераций, для кадров.
        self.x_y = [0, 0]  # координаты игрока на карте игры
        self.force_rect = (self.x_y[1], self.x_y[0], self.force * 2, self.force * 2)
        self.mad_coaff = 0.09
        self.state = ''  # craft, run, stay, vector, use:#, dont_move
        self.vector = (self.speed, self.speed, 0, 0, False, False)
        self.timer = 0
        self.crafting_things = ''
        self.crafting_stack = 1

    def setInventaryBox(self, box):
        self.inventary = box

    def cut_sheet(self, sheet, columns, rows, ots, napr):
        self.rect = pygame.Rect(0, ots, sheet.get_width() // columns,
                                sheet.get_height() // (rows * self.num_of_anim))
        self.frames[napr].append([])
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.y + self.rect.h * j)
                self.frames[napr][-1].append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def getCoords(self):
        return (self.x_y[0], self.x_y[1])

    def getStats(self):
        return (self.health, self.madness, self.darkness, self.light)

    def getCoordsOnMap(self, coords):
        coords_on_map = (
            coords[0] - self.map.coords_about_screean[0], coords[1] - self.map.coords_about_screean[1])
        return coords_on_map

    def getCoordsInFrame(self, coords):
        coords_on_screen = (
            self.level.map_.coords_about_screean[0] + coords[0], self.level.map_.coords_about_screean[1] + coords[1])
        return coords_on_screen

    def update(self, fps, point, mouse_button_down, mouse_button_down_r, pressed_keys):
        self.inventary_group.draw(self.level.screen)
        in_frame_point = self.getCoordsInFrame(point)
        self.collideRectImMapWithSpeed()
        self.i_j_k += 1

        if self.health <= 0:
            self.level.level_state = 'die'
        # Тиковые параметры, которые изменяются с течением времни.
        self.light += 0.5 * fps
        if self.light >= 100:
            self.light = 100
        self.changeHungerAbout(0.1 * fps, fps)
        self.changeMadnessAbout(self.mad_coaff * fps)
        # Параметры, которые изменяются от внешних воздействий и колайдов
        # None

        # проверка состояния игрока - действия.

        if (mouse_button_down and not (self.inventary.rect.collidepoint(in_frame_point)) and
                not (self.state == 'craft' or self.state == 'dont_move' or 'use' in self.state)):
            self.state = 'vector'
            self.findVector(point)
        if self.state == 'dont_move':
            self.state = 'stay'
        if 'use' in self.state:
            if mouse_button_down:
                self.equipped.useThing(self.level, in_frame_point[0], in_frame_point[1])
                self.state = 'stay'
                self.equipped = None
            if mouse_button_down_r:
                self.state = 'stay'
                self.equipped = None
            pygame.draw.ellipse(self.level.screen, pygame.color.Color(255, 0, 0),
                                pygame.rect.Rect(in_frame_point[0] - 25, in_frame_point[1] - 25, 50, 50))
        self.inventary_group.update(fps, in_frame_point, mouse_button_down, mouse_button_down_r)

        # Параметры отрисовки и нажатия на кнокпки

        if self.state == 'vector':
            self.toVector()
        self.changeCoords(pressed_keys)
        # замена позы на бег влево
        if pressed_keys[pygame.K_LEFT] or (self.state == 'vector' and self.vector[0] < 0 and self.vector[-2]):
            if self.naptr != 1:
                self.naptr = 1
            self.cur_frame = (1, self.cur_frame[1])
            self.image = self.frames[self.naptr][self.cur_frame[0]][self.cur_frame[1]]
            self.frames_in_itter = 8
        # замена позы на бег вправо
        elif pressed_keys[pygame.K_RIGHT] or (self.state == 'vector' and self.vector[0] > 0 and self.vector[-2]):
            if self.naptr != 3:
                self.naptr = 3
            self.cur_frame = (1, self.cur_frame[1])
            self.image = self.frames[self.naptr][self.cur_frame[0]][self.cur_frame[1]]
            self.frames_in_itter = 8
        elif pressed_keys[pygame.K_DOWN] or (self.state == 'vector' and self.vector[1] > 0 and self.vector[-1]):
            if self.naptr != 0:
                self.naptr = 0
            self.cur_frame = (1, self.cur_frame[1])
            self.image = self.frames[self.naptr][self.cur_frame[0]][self.cur_frame[1]]
            self.frames_in_itter = 8
        elif pressed_keys[pygame.K_UP] or (self.state == 'vector' and self.vector[1] < 0 and self.vector[-1]):
            if self.naptr != 2:
                self.naptr = 2
            self.cur_frame = (1, self.cur_frame[1])
            self.image = self.frames[self.naptr][self.cur_frame[0]][self.cur_frame[1]]
            self.frames_in_itter = 3
        # замена на позы на стойку
        else:
            self.cur_frame = (0, self.cur_frame[1])
            self.image = self.frames[self.naptr][self.cur_frame[0]][self.cur_frame[1]]
            self.frames_in_itter = 10
        if self.state == 'craft':
            if self.timer >= 9:
                self.craftSomething()
                self.timer = 0
            if self.timer == 0:
                self.cur_frame = (2, 0)
                self.image = self.frames[self.naptr][self.cur_frame[0]][self.cur_frame[1]]
                self.frames_in_itter = 15
            if 0 < self.timer < 9:
                self.cur_frame = (2, self.cur_frame[1])
                self.frames_in_itter = 15
                self.image = self.frames[self.naptr][self.cur_frame[0]][self.cur_frame[1]]
        # смена кадров
        if self.i_j_k % self.frames_in_itter == 0:
            self.cur_frame = (
                self.cur_frame[0], (self.cur_frame[1] + 1) % len(self.frames[self.naptr][self.cur_frame[0]]))
            self.image = self.frames[self.naptr][self.cur_frame[0]][self.cur_frame[1]]
            if self.timer < 9 and (self.state == 'craft'):
                self.timer += 1

    # метод проверки и изменения координат
    def findVector(self, pos):
        self.vector = (self.speed, self.speed, pos[0], pos[1], True, True)
        if self.x_y[0] > pos[0]:
            self.vector = (-self.vector[0], self.vector[1], self.vector[2], self.vector[3], True, True)
        if self.x_y[1] > pos[1]:
            self.vector = (self.vector[0], -self.vector[1], self.vector[2], self.vector[3], True, True)

    def toVector(self):
        if self.vector[0] > 0:
            if self.x_y[0] <= self.vector[2]:
                if (self.map.map[(self.x_y[1] - 10) // 300][(self.x_y[0] + self.speed + 35) // 300] == 'g'
                        and not self.collideAnyInMap(self.vector[0], 0)):
                    self.x_y[0] += self.vector[0]
                    self.map.coords_about_screean[0] -= self.vector[0]
            else:
                self.vector = (self.vector[0], self.vector[1], self.vector[2], self.vector[3], False, self.vector[5])
        else:
            if self.x_y[0] >= self.vector[2]:
                if (self.map.map[(self.x_y[1] - 10) // 300][(self.x_y[0] - self.speed - 35) // 300] == 'g'
                        and not self.collideAnyInMap(self.vector[0], 0)):
                    self.x_y[0] += self.vector[0]
                    self.map.coords_about_screean[0] -= self.vector[0]
            else:
                self.vector = (self.vector[0], self.vector[1], self.vector[2], self.vector[3], False, self.vector[5])
        if self.vector[1] > 0:
            if self.x_y[1] <= self.vector[3]:
                if (self.map.map[(self.x_y[1] - self.speed + 30) // 300][(self.x_y[0] + 35) // 300] == 'g'
                        and not self.collideAnyInMap(0, self.vector[1])):
                    self.x_y[1] += self.vector[1]
                    self.map.coords_about_screean[1] -= self.vector[1]
            else:
                self.vector = (self.vector[0], self.vector[1], self.vector[2], self.vector[3], self.vector[4], False)
        else:
            if self.x_y[1] >= self.vector[3]:
                if (self.map.map[(self.x_y[1] + self.speed - 30) // 300][(self.x_y[0] - 35) // 300] == 'g'
                        and not self.collideAnyInMap(0, self.vector[1])):
                    self.x_y[1] += self.vector[1]
                    self.map.coords_about_screean[1] -= self.vector[1]
            else:
                self.vector = (self.vector[0], self.vector[1], self.vector[2], self.vector[3], self.vector[4], False)
        if not self.vector[-1] and not self.vector[-2]:
            self.state = 'stay'

    def changeCoords(self, keyboard):
        if keyboard[pygame.K_LEFT]:
            self.state = 'stay'
            if not self.i_may_go:
                if (self.map.map[(self.x_y[1] - 10) // 300][(self.x_y[0] - self.speed - 35) // 300] == 'g' and
                        not self.collideAnyInMap(-self.speed, 0)):
                    self.x_y[0] -= self.speed
                    self.map.coords_about_screean[0] += self.speed
            else:
                self.x_y[0] -= self.speed
                self.map.coords_about_screean[0] += self.speed
        if keyboard[pygame.K_RIGHT]:
            self.state = 'stay'
            if not self.i_may_go:
                if (self.map.map[(self.x_y[1] - 10) // 300][(self.x_y[0] + self.speed + 35) // 300] == 'g' and
                        not self.collideAnyInMap(self.speed, 0)):
                    self.x_y[0] += self.speed
                    self.map.coords_about_screean[0] -= self.speed
            else:
                self.x_y[0] += self.speed
                self.map.coords_about_screean[0] -= self.speed
        if keyboard[pygame.K_DOWN]:
            self.state = 'stay'
            if not self.i_may_go:
                if (self.map.map[(self.x_y[1] + self.speed + 30) // 300][(self.x_y[0] - 35) // 300] == 'g' and
                        not self.collideAnyInMap(0, self.speed)):
                    self.x_y[1] += self.speed
                    self.map.coords_about_screean[1] -= self.speed
            else:
                self.x_y[1] += self.speed
                self.map.coords_about_screean[1] -= self.speed
        if keyboard[pygame.K_UP]:
            self.state = 'stay'
            if not self.i_may_go:
                if (self.map.map[(self.x_y[1] - self.speed - 30) // 300][(self.x_y[0] + 35) // 300] == 'g' and
                        not self.collideAnyInMap(0, -self.speed)):
                    self.x_y[1] -= self.speed
                    self.map.coords_about_screean[1] += self.speed
            else:
                self.x_y[1] -= self.speed
                self.map.coords_about_screean[1] += self.speed

    # метод применения заклинания к персонажу
    def castChar(self, char):
        pass

    def collideAnyInMap(self, speed_x, speed_y):
        for i in self.level.static_obj_not_in_frame:
            if self.collideRectImMap(i.force_rect, speed_x, speed_y, 0, 0):
                return True
        for i in self.level.interaction_obj_not_in_frame:
            if self.collideRectImMap(i.force_rect, speed_x, speed_y, 0, 0):
                return True
        return False

    def collideRectImMapWithSpeed(self):
        self.force_rect = self.getCoordsInFrame(self.x_y)
        self.force_rect = (
        self.force_rect[0] - self.force, self.force_rect[1] - self.force, self.force * 2, self.force * 2)
        pygame.draw.rect(self.level.screen, pygame.color.Color(255, 0, 0), self.force_rect)

    def collideRectImMap(self, rect, speed_x, speed_y, plus_w, plus_h):
        x, y, w, h = rect
        x1, y1, w1, h1 = self.force_rect
        x1, y1 = x1 + speed_x - plus_w // 2, y1 + speed_y - plus_h // 2
        w1, h1 = w1 + plus_w, h1 + plus_h
        if ((x <= x1 <= x + w and y <= y1 <= y + h) or
                (x <= x1 + w1 <= x + w and y <= y1 + h1 <= y + h) or
                (x <= x1 + w1 <= x + w and y <= y1 <= y + h) or
                (x <= x1 <= x + w and y <= y1 + h1 <= y + h) or

                (x1 <= x <= x1 + w1 and y1 <= y <= y1 + h1) or
                (x1 <= x + w <= x1 + w1 and y1 <= y + h <= y1 + h1) or
                (x1 <= x + w <= x1 + w1 and y1 <= y <= y1 + h1) or
                (x1 <= x <= x1 + w1 and y1 <= y + h <= y1 + h1)):
            return True
        else:
            return False

    # метод изменения здоровья персонажа
    def changeHealthAbout(self, num):
        self.health -= num
        if self.health >= self.health_max:
            self.health = self.health_max
        elif self.health < 0:
            self.health = 0

    # метод изменения голода персонажа
    def changeHungerAbout(self, num, fps):
        self.hunger += num
        if self.hunger >= self.hunger_max:
            self.hunger = self.hunger_max
            self.changeHealthAbout(50 * fps)
        elif self.hunger < 0:
            self.hunger = 0
        if self.hunger >= 0.3 * self.hunger_max and self.mad_coaff < 0.1:
            self.mad_coaff *= 2
        if self.hunger >= 0.65 * self.hunger_max and self.mad_coaff < 0.3:
            self.mad_coaff *= 2

    # метод изменения безумия персонажа
    def changeMadnessAbout(self, num):
        self.madness += num
        if self.madness >= self.madness_max:
            self.madness = self.madness_max
        if self.madness < 0:
            self.madness = 0

    # метод перекачки магической силу туда или обратно
    def changeMagicForceAbout(self, num, light_dark_bool):
        if light_dark_bool:
            if self.light >= 100:
                return -1
            self.darkness -= num
            self.light += num
        else:
            if self.darkness >= 100:
                return -1
            self.darkness += num
            self.light -= num
        if self.darkness > 100 or self.light > 100:
            self.darkness = math.floor(math.fabs(self.darkness / 100)) * 100
            self.light = math.floor(math.fabs(self.light / 100)) * 100

    def giveSomething(self, thing):
        pass

    def eatSomething(self, food):
        pass

    def teleportTo(self, x, y):
        self.x_y = [x, y]
        self.force_rect = (self.x_y[0], self.x_y[1], self.force * 2, self.force * 2)
        self.map.changeCoords([-self.x_y[0] + width // 2,
                               -self.x_y[1] + height // 2 + self.image.get_height() // 2 - 10])

    def craftSomething(self):
        type_th = thing_param[self.crafting_things]['type']
        if type_th == 'matirial_things':
            DefaultThing(self.level.things_ogf_spr, self.crafting_things,
                         [self.x_y[0] - 35, self.x_y[1] - 35], self.crafting_stack,
                         self.level)
        elif type_th == 'food':
            pass
        elif type_th == 'useable_things':
            UsebaleThings(self.level.usebale_things_ogf_spr, self.crafting_things,
                          [self.x_y[0] - 35, self.x_y[1] - 35], self.crafting_stack,
                          self.level)
        self.crafting_stack = 1
        self.crafting_things = ''
        self.state = 'stay'


class CraftListThing(pygame.sprite.Sprite):
    back_image = load_image('interface_images/craft_table_bookmarks/craft_list_thing_backgr.png')

    def __init__(self, x, y, name):
        super().__init__()
        self.name = name
        self.param = thing_param[name]
        self.image = self.draw_icon()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw_icon(self):
        sur = CraftListThing.back_image.copy()
        text = ' '.join(self.name.split('_')).title()
        text = font1.render(text, 1, (0, 0, 0))
        text_x = (200 - text.get_width()) // 2
        text_y = 10
        sur.blit(text, (text_x, text_y))
        sur.blit(load_image(self.param['image']), (200 // 2 - 70 // 2, text.get_height() + 15))
        text_x, text_y = 8, text.get_height() + 15 + 8 + 70
        for i in self.param['recipe']:
            temp = i.split()
            image = ''
            if temp[0] == 'light':
                image = pygame.Surface((30, 30))
                image.fill((243, 242, 146))
            elif temp[0] == 'dark':
                image = pygame.Surface((30, 30))
                image.fill((61, 0, 61))
            else:
                image = pygame.transform.scale(load_image(thing_param[temp[0]]['image']), (30, 30))
            text = font1.render(temp[1] + 'x', 1, (0, 0, 0))
            sur.blit(text, (text_x, text_y))
            text_x += 3 + text.get_width()
            sur.blit(image, (text_x, text_y))
            text_x += 30
        return sur


class CraftMenuButton(pygame.sprite.Sprite):

    def __init__(self, group, x, y, screen, player, img=None, rec_list=[]):
        super().__init__(group)
        self.player = player
        self.screen = screen
        self.speed = 3
        self.collide_opened = False
        self.button_group = pygame.sprite.Group()
        Button(self.button_group, 'interface_images/craft_table_bookmarks/arror_button_up.png',
               150 + 200 // 2 - 135 // 2, height // 2 - 250 // 2 - 57 - 5, lambda u: '1', self)
        Button(self.button_group, 'interface_images/craft_table_bookmarks/create_button.png', 150 + 200 // 2 - 135 // 2,
               height // 2 - 250 // 2 + 250 - 70, lambda u: '', self)
        Button(self.button_group, 'interface_images/craft_table_bookmarks/arror_button_down.png',
               150 + 200 // 2 - 135 // 2, height // 2 - 250 // 2 + 250 + 5, lambda u: '-1', self)

        if not img is None:
            self.image = load_image(img)
            self.rect = self.image.get_rect()
        else:
            self.image = pygame.Surface([110, 50])
            self.image.fill(pygame.Color("red"))
        self.rect.x = x
        self.rect.y = y
        self.x_closepoint = x + 45
        # личные меню
        self.list_of_craft_names = rec_list
        self.list_of_craft = [pygame.sprite.Group(CraftListThing(150, height // 2 - 250 // 2, i)) for i in rec_list]
        self.name = ''
        self.open = False
        self.open_again = False
        self.cur_item = 0

    def update(self, fps, point, mouse_b):
        self.open_again = False
        if ((self.open and mouse_b and
                (150 <= point[0] <= 450 and height // 2 - 250 // 2 - 57 - 5 <= point[
                    1] <= height // 2 - 250 // 2 + 250 + 5 + 57))):
            self.collide_opened = True
        if self.open and len(self.list_of_craft_names):
            self.button_group.update(point, mouse_b)
        # При наведении мышкой выдвигается и задвигается назад в иначе
        if self.rect.collidepoint(point):
            if self.rect.x < self.x_closepoint:
                self.rect.x += self.speed
            # При нажатиии на закладку показывается список рецептов крафта.
            if mouse_b:
                self.open = True
        else:
            if mouse_b and not self.open_again:
                self.player.level.menu.menu.have_opened = False
                self.open = False
            if self.rect.x > self.x_closepoint - 45:
                self.rect.x -= self.speed
        if self.open:
            if len(self.list_of_craft) > 0:
                self.list_of_craft[self.cur_item].draw(self.screen)
                self.button_group.draw(self.screen)

    def addToListOfCraft(self, rec):
        self.list_of_craft.append(rec)

    def setName(self, name):
        self.name = name

    def pressMouseButton(self, arg):
        self.open_again = True
        if arg == '1' or arg == '-1':
            self.player.state = 'dont_move'
            self.cur_item += int(arg)
            self.cur_item = self.cur_item % len(self.list_of_craft)
        else:
            self.player.state = 'dont_move'
            thing = self.list_of_craft_names[self.cur_item]
            i_may_make_it = True
            recipe = []
            for i in thing_param[thing]['recipe']:
                temp = i.split()
                if temp[0] == 'light':
                    if self.player.light < int(temp[1]):
                        i_may_make_it = False
                        break
                    recipe.append(('light', int(temp[1])))
                elif temp[0] == 'dark':
                    if self.player.darkness < int(temp[1]):
                        i_may_make_it = False
                        break
                    recipe.append(('dark', int(temp[1])))
                else:
                    check_recipe = self.player.inventary.countThatThings(temp[0], int(temp[1]))
                    if check_recipe[0] != int(temp[1]):
                        i_may_make_it = False
                        break
                    recipe.append((check_recipe[1], int(temp[1])))

            if i_may_make_it:
                for i in recipe:
                    if i[0] == 'light':
                        self.player.light -= int(i[1])
                    elif i[0] == 'dark':
                        self.player.darkness -= int(i[1])
                    else:
                        self.player.inventary.takeThingForCraft(i[0], i[1])
                self.player.crafting_things = thing
                self.player.state = 'craft'


class Menu(pygame.sprite.Sprite):
    def __init__(self, group, pl, screen, img=None):
        self.screen = screen
        self.list_of_menu = []
        self.stats = []
        #        self.clock = InGameClock(group, width - 300 - 50, height - 300 - 200)
        self.stat_group = pygame.sprite.Group()
        self.createStats(self.stat_group, pl)
        super().__init__(group)
        if not img is None:
            self.image = load_image(img)
            self.rect = self.image.get_rect()
        else:
            self.image = pygame.Surface([70, 800])
            self.image.fill(pygame.Color("yellow"))
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = 50
        self.have_opened = False
        self.collide_opened_menu = False
        self.last_itteration = 0

    def update(self, fps, point, mouse, pressed_keys):
        self.collide_opened_menu = False
        if pressed_keys[pygame.K_q] and not self.last_itteration:
            open = False
            for i in self.list_of_menu:
                if i.open:
                    open = True
                    break
            print(open, self.have_opened)
            if not open and not self.have_opened:
                self.last_itteration = True
                self.have_opened = True
                self.list_of_menu[0].open = True
            elif open and self.have_opened:
                self.last_itteration = True
                self.have_opened = False
                for i in self.list_of_menu:
                    i.open = False
        else:
            if self.last_itteration != 5:
                self.last_itteration += 1
            else:
                self.last_itteration = 0
        for i in range(4):
            self.list_of_menu[i].update(fps, point, mouse)
        for i in self.stats:
            i.update(fps, point)
        self.stat_group.draw(self.screen)
        if (30 <= point[0] <= 140 and
                50 <= point[1] <= 50 + 800):
            self.stats[0].player.state = 'dont_move'

    def createStats(self, group, pl):
        x, y = width - 70 * 3 - 70 - 35, 100
        self.stats = [PlayerStatShower(x, y, group, pl, self.screen, 'health'),
                      PlayerStatShower(x + 70 + 35, y, group, pl, self.screen, 'hung'),
                      PlayerStatShower(x + 210, y, group, pl, self.screen, 'mad'),
                      PlayerStatShower(x, y + 70 + 35, group, pl, img='l_and_d', screen=self.screen)]
        self.stats[0].setName('Health')
        self.stats[1].setName('Hunger')
        self.stats[2].setName('Madness')
        self.stats[3].setName('Light & Dark energy')

        x, y = 35, 90
        imgs = ['interface_images/craft_table_bookmarks/arseal_icon.png',
                'interface_images/craft_table_bookmarks/devises_icon.png',
                'interface_images/craft_table_bookmarks/matirial_icon.png',
                'interface_images/craft_table_bookmarks/light_icon.png']
        crafts = [['grass_stick'], [], ['rope_matirial', 'grass_matirial'], []]
        for i in range(4):
            self.list_of_menu.append(CraftMenuButton(group, x, y, self.screen, pl, img=imgs[i], rec_list=crafts[i]))
            y += 80


class PlayerStatShower(pygame.sprite.Sprite):
    base_stat_img = load_image('interface_images/player_stats_icon/player_stat.png')
    l_d_gaier_img = load_image('interface_images/player_stats_icon/light_dark_gauger.png')

    def __init__(self, x, y, group, player, screen, img=None):
        super().__init__(group)
        self.screen = screen
        self.frames = []
        self.player = player
        self.image = pygame.Surface([70, 70])
        self.image.fill(pygame.Color("green"))
        self.cur_frame = 0
        if img == 'health':
            self.cut_sheet(PlayerStatShower.base_stat_img, 3, 0)
        elif img == 'hung':
            self.cut_sheet(PlayerStatShower.base_stat_img, 3, 1)
        elif img == 'mad':
            self.cut_sheet(PlayerStatShower.base_stat_img, 3, 2)
        elif img == 'l_and_d':
            self.image = PlayerStatShower.l_d_gaier_img
            self.frames.append(self.image)
        if img != None and img != 'l_and_d':
            self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # личные параметры
        self.num = 0
        self.name = ''

    def cut_sheet(self, sheet, columns, riad):
        self.rect = pygame.Rect(0, 0, 70,
                                70)
        for i in range(columns):
            frame_location = (self.rect.w * i, self.rect.h * riad)
            self.frames.append(sheet.subsurface(pygame.Rect(
                frame_location, self.rect.size)))

    def update(self, fps, point):
        if self.name == 'Light & Dark energy':
            pygame.draw.rect(self.screen, pygame.Color(243, 242, 146), pygame.Rect(self.rect.x + 4,
                                                                                   self.rect.y + 5 + 112 * (1 - (
                                                                                           self.player.light / 100)),
                                                                                   35,
                                                                                   112 * (self.player.light / 100)))
            pygame.draw.rect(self.screen, pygame.Color(61, 0, 61),
                             pygame.Rect(self.rect.x + self.image.get_width() - 4 - 35,
                                         self.rect.y + 5 + 112 * (1 - (self.player.darkness / 100)),
                                         35, 112 * (self.player.darkness / 100)))
        elif self.name == 'Health':
            pygame.draw.arc(self.screen, pygame.Color(70, 136, 50), (self.rect.x + 1, self.rect.y + 1, 69, 69),
                            0, 6.28 * (self.player.health / self.player.health_max), 34)
            if self.player.health < 0.65 * self.player.health_max and self.cur_frame == 0:
                self.cur_frame += 1
            if self.player.health < 0.30 * self.player.health_max and self.cur_frame == 1:
                self.cur_frame += 1
        elif self.name == 'Hunger':
            pygame.draw.arc(self.screen, pygame.Color(150, 40, 21), (self.rect.x + 1, self.rect.y + 1, 69, 69),
                            0, 6.28 * (self.player.hunger / self.player.hunger_max), 34)
            if self.player.hunger > 0.30 * self.player.hunger_max and self.cur_frame == 0:
                self.cur_frame += 1
            if self.player.hunger > 0.65 * self.player.hunger_max and self.cur_frame == 1:
                self.cur_frame += 1
            if 0.3 * self.player.hunger_max < self.player.hunger < 0.65 * self.player.hunger_max and self.cur_frame == 2:
                self.cur_frame -= 1
            if 0 < self.player.hunger < 0.3 * self.player.hunger_max and self.cur_frame == 1:
                self.cur_frame -= 1
        elif self.name == 'Madness':
            pygame.draw.arc(self.screen, pygame.Color(200, 96, 134), (self.rect.x + 1, self.rect.y + 1, 69, 69),
                            0, 6.28 * (self.player.madness / self.player.madness_max), 34)
            if self.player.madness > 0.30 * self.player.madness_max and self.cur_frame == 0:
                self.cur_frame += 1
            if self.player.madness > 0.65 * self.player.madness_max and self.cur_frame == 1:
                self.cur_frame += 1
        self.image = self.frames[self.cur_frame]

        # при наведении на показатель мышкой показывается число параметра и имя
        if self.rect.collidepoint(point):
            text = 'AAAAAAAAA'
            if self.name == 'Light & Dark energy':
                text = str(int(self.player.light)) + '/' + str(int(self.player.darkness))
            elif self.name == 'Health':
                text = str(int(self.player.health))
            elif self.name == 'Hunger':
                text = str(int(self.player.hunger))
            elif self.name == 'Madness':
                text = str(int(self.player.madness))
            text = font.render(text, 1, (230, 230, 230))
            if self.name != 'Light & Dark energy':
                text_x = self.rect.x + (self.rect.w - text.get_width()) // 2
                text_y = self.rect.y - 50
            else:
                text_x = self.rect.x - text.get_width() // 2 + self.rect.w // 2
                text_y = self.rect.y - text.get_height() // 2 + self.rect.h // 2
            self.screen.blit(text, (text_x, text_y))

    def setName(self, name):
        self.name = name

    def setParam(self, num):
        self.num = num


class InGameClock(pygame.sprite.Sprite):
    clock_img = load_image('interface_images/state_of_world/clock.png')

    def __init__(self, group, x, y, clock_img=None):
        super().__init__(group)
        self.image = InGameClock.clock_img
        if not (clock_img is None):
            pass
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, fps):
        pass
