import pygame, math
from CONSTANTS import width, height, load_image


class Player(pygame.sprite.Sprite):
    # картинки ерсонажа с разных сторон
    image_l = load_image('player_character/jaylf_sprite_l.png')
    image_r = load_image('player_character/jaylf_sprite_r.png')

    def __init__(self, group, map_):
        super().__init__(group)
        self.map = map_
        self.naptr = 1  # направление персонажа относительно север-юг-запад-восток:
        #  0 - Юг, 1 - запад, 2 - север, 3 - восток
        self.frames = [[], [], [], []]
        self.frames_in_itter = 10  # кол-во иттераций на один кадр
        self.cur_frame = (0, 0)  # выделеный кадр анимации
        self.num_of_anim = 2  # количество анимаций

        # разрезка западного направления
        for i in range(0, (self.num_of_anim + 1) * 233, 466):
            self.cut_sheet(Player.image_l, 5, 2, i, 1)
        # разрезка восточного направления
        for i in range(0, (self.num_of_anim + 1) * 233, 466):
            self.cut_sheet(Player.image_r, 5, 2, i, 3)
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
        self.i_may_go = False
        self.speed = 8  # скорость
        self.force = 1  # сила внешнего взаимодействия объекта
        self.i_j_k = 0  # счётчик итераций, для кадров.
        self.x_y = [0, 0]  # координаты игрока на карте игры
        self.mad_coaff = 0.09

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

    def update(self, fps, *args):
        self.i_j_k += 1
        # Тиковые параметры, которые изменяются с течением времни.
        self.light += 0.5 * fps
        if self.light >= 100:
            self.light = 100
        self.changeHungerAbout(0.1 * fps, fps)
        self.changeMadnessAbout(self.mad_coaff * fps)
        # Параметры, которые изменяются от внешних воздействий и колайдов
        # None
        # перемещение
        self.changeCoords()
        # Параметры отрисовки и нажатия на кнокпки
        pressed_keys = pygame.key.get_pressed()
        # замена позы на бег влево
        if pressed_keys[pygame.K_LEFT]:
            if self.naptr != 1:
                self.naptr = 1
            self.cur_frame = (1, self.cur_frame[1])
            self.image = self.frames[self.naptr][self.cur_frame[0]][self.cur_frame[1]]
            self.frames_in_itter = 8
        # замена позы на бег вправо
        elif pressed_keys[pygame.K_RIGHT]:
            if self.naptr != 3:
                self.naptr = 3
            self.cur_frame = (1, self.cur_frame[1])
            self.image = self.frames[self.naptr][self.cur_frame[0]][self.cur_frame[1]]
            self.frames_in_itter = 8
        # замена на позы на стойку
        else:
            self.cur_frame = (0, self.cur_frame[1])
            self.image = self.frames[self.naptr][self.cur_frame[0]][self.cur_frame[1]]
            self.frames_in_itter = 10
        # смена кадров
        if self.i_j_k % self.frames_in_itter == 0:
            self.cur_frame = (
                self.cur_frame[0], (self.cur_frame[1] + 1) % len(self.frames[self.naptr][self.cur_frame[0]]))
            self.image = self.frames[self.naptr][self.cur_frame[0]][self.cur_frame[1]]

    # метод проверки и изменения координат
    def changeCoords(self):
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            if not self.i_may_go:
                if self.map.map[(self.x_y[1] - 30) // 300][(self.x_y[0] - self.speed - 35) // 300] == 'g':
                    self.x_y[0] -= self.speed
                    self.map.coords_about_screean[0] += self.speed
            else:
                self.x_y[0] -= self.speed
                self.map.coords_about_screean[0] += self.speed
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            if not self.i_may_go:
                if self.map.map[(self.x_y[1] + 30) // 300][(self.x_y[0] + self.speed + 35) // 300] == 'g':
                    self.x_y[0] += self.speed
                    self.map.coords_about_screean[0] -= self.speed
            else:
                self.x_y[0] += self.speed
                self.map.coords_about_screean[0] -= self.speed
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            if not self.i_may_go:
                if self.map.map[(self.x_y[1] + self.speed + 30) // 300][(self.x_y[0] - 35) // 300] == 'g':
                    self.x_y[1] += self.speed
                    self.map.coords_about_screean[1] -= self.speed
            else:
                self.x_y[1] += self.speed
                self.map.coords_about_screean[1] -= self.speed
        if pygame.key.get_pressed()[pygame.K_UP]:
            if not self.i_may_go:
                if self.map.map[(self.x_y[1] - self.speed - 30) // 300][(self.x_y[0] + 35) // 300] == 'g':
                    self.x_y[1] -= self.speed
                    self.map.coords_about_screean[1] += self.speed
            else:
                self.x_y[1] -= self.speed
                self.map.coords_about_screean[1] += self.speed

    # метод применения заклинания к персонажу
    def castChar(self, char):
        pass

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

    def eatSomething(self, food):
        pass

    def teleportTo(self, x, y):
        self.x_y = [x, y]


class CraftMenuButton(pygame.sprite.Sprite):

    def __init__(self, group, x, y, img=''):
        super().__init__(group)
        self.image = pygame.Surface([110, 50])
        self.image.fill(pygame.Color("red"))
        self.speed = 3
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_closepoint = x + 45
        # личные меню
        self.list_of_craft = []
        self.name = ''

    def update(self, fps):
        # При наведении мышкой выдвигается и задвигается назад в иначе
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.rect.x < self.x_closepoint:
                self.rect.x += self.speed
        else:
            if self.rect.x > self.x_closepoint - 45:
                self.rect.x -= self.speed
        # При нажатиии на закладку показывается список рецептов крафта.

    def addToListOfCraft(self, rec):
        self.list_of_craft.append(rec)

    def setName(self, name):
        self.name = name


class Menu(pygame.sprite.Sprite):
    def __init__(self, group, pl, screen, img=''):
        self.list_of_menu = []
        self.stats = []
        self.clock = InGameClock(group, width - 300 - 50, height - 300 - 200)
        self.createStats(group, pl, screen)
        super().__init__(group)
        self.image = pygame.Surface([70, 800])
        self.image.fill(pygame.Color("yellow"))
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = (height - self.image.get_height()) // 2

    def update(self, fps):
        for i in range(3):
            self.list_of_menu[i].update(fps)
        for i in self.stats:
            i.update(fps)
        self.clock.update(fps)

    def createStats(self, group, pl, screen):
        x, y = width - 70 * 3 - 70 - 35, 100
        self.stats = [PlayerStatShower(x, y, group, pl, screen, 'health'),
                      PlayerStatShower(x + 70 + 35, y, group, pl, screen, 'hung'),
                      PlayerStatShower(x + 210, y, group, pl, screen, 'mad'),
                      PlayerStatShower(x, y + 70 + 35, group, pl, img='l_and_d', screen=screen)]
        self.stats[0].setName('Health')
        self.stats[1].setName('Hunger')
        self.stats[2].setName('Madness')
        self.stats[3].setName('Light & Dark energy')

        x, y = 35, 90
        for i in range(3):
            self.list_of_menu.append(CraftMenuButton(group, x, y))
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

    def update(self, fps):
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
            return 0
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
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            text = 'AAAAAAAAA'
            if self.name == 'Light & Dark energy':
                text = str(int(self.player.light)) + '/' + str(int(self.player.darkness))
            elif self.name == 'Health':
                text = str(int(self.player.health))
            elif self.name == 'Hunger':
                text = str(int(self.player.hunger))
            elif self.name == 'Madness':
                text = str(int(self.player.madness))
            font = pygame.font.Font('data/DS Brushes Normal.ttf', 50)
            text = font.render(text, 1, (255, 0, 0))
            text_x = self.rect.x + (self.rect.w - text.get_width()) // 2
            text_y = self.rect.y - 50
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
