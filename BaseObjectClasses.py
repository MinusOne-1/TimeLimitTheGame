import pygame

from CONSTANTS import static_obj_param, load_image, font, thing_param, interaction_obj_param, mod, font1


def burh(self):
    self.player.crafting_things = 'stick_matirial'
    self.player.crafting_stack = 2
    self.player.state = 'craft'
    self.may_be_interacted = False


interaction_obj_param['bush'] = {'num_of_anim': 1,
                                 'images': ['interaction_object_image/stick_bush.png', 'img_r', 'img_u', 'img_d'],
                                 'image_w': 200, 'image_h': 137, 'rows': 1, 'colomns': 2, 'force': 25,
                                 'comment': 'a bush. Ok.', 'fuc': burh}


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
        self.num_of_anim = 1  # количество анимаций
        self.force = 50

        self.force_rect = (0, 0)
        self.force_rect = (
            self.force_rect[0] - self.force, self.force_rect[1] - self.force, self.force * 2, self.force * 2)

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
        if self.num_of_anim >= 1:
            for i in range(0, (self.num_of_anim + 1) * self.param['image_w'],
                           self.param['image_w'] * self.param['rows']):
                self.cut_sheet(self.images[0], self.param['colomns'], self.param['rows'], i, 0)
            self.image = self.frames[self.naptr][self.cur_frame[0]][self.cur_frame[1]]
        else:
            self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.getCoordsInFrame()
        self.force = self.param['force']
        self.force_rect = self.getCoordsInFrame()
        self.force_rect = (
            self.force_rect[0] - self.param['image_w'] // 2, self.force_rect[1] - self.force, self.param['image_w'],
            self.force * 2)

    def getCoordsInFrame(self):
        coords_on_screen = (
            self.map.coords_about_screean[0] + self.x_y[0] - self.param['image_w'] // 2,
            self.map.coords_about_screean[1] + self.x_y[1] - self.param['image_h'])
        return coords_on_screen

    def getCoordsInFrameForMapRect(self):
        coords_on_screen = (
            self.map.coords_about_screean[0] + self.x_y[0],
            self.map.coords_about_screean[1] + self.x_y[1])
        return coords_on_screen

    def rectInMap(self):
        self.force_rect = self.getCoordsInFrameForMapRect()
        self.force_rect = (
            self.force_rect[0] - self.param['image_w'] // 2, self.force_rect[1] - self.force, self.param['image_w'],
            self.force * 2)

    def update(self, fps, point):
        self.rectInMap()
        self.rect.x, self.rect.y = self.getCoordsInFrame()
        self.collideMouse(point)
        if self.num_of_anim >= 1:
            self.i_j_k += 1
            if self.i_j_k % self.frames_in_itter == 0:
                self.cur_frame = (
                    self.cur_frame[0], (self.cur_frame[1] + 1) % len(self.frames[self.naptr][self.cur_frame[0]]))
                self.image = self.frames[self.naptr][self.cur_frame[0]][self.cur_frame[1]]

    def collideMouse(self, point):
        if self.rect.collidepoint(point):
            text = font.render(self.param['comment'], 1, (83, 189, 104))
            text_x = self.rect.x + (self.rect.w - text.get_width()) // 2
            text_y = self.rect.y - 50
            self.screen.blit(text, (text_x, text_y))


class DinamicObject(BaseObject):
    pass


class InteractionObject(BaseObject):
    def __init__(self, group, screen, x_y, map_, obj_name, player, arg=None, may_be_interacted=True):
        self.screen = screen
        self.may_be_interacted = may_be_interacted
        self.player = player
        super().__init__(group, x_y, map_)
        self.param = interaction_obj_param[obj_name]
        self.interactionAction = self.param['fuc']
        self.num_of_anim = self.param['num_of_anim']
        self.images = [load_image(i) for i in self.param['images'][:1]]
        self.timer = 0
        self.args_for_interaction = arg

        for i in range(0, (self.num_of_anim + 1) * self.param['image_w'], self.param['image_w'] * self.param['rows']):
            self.cut_sheet(self.images[0], self.param['colomns'], self.param['rows'], 0, 0)
        self.image = self.frames[self.naptr][self.cur_frame[0]][self.cur_frame[1]]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.getCoordsInFrame()
        self.interacted = False

        self.force = self.param['force']
        self.force_rect = self.getCoordsInFrame()
        self.force_rect = (
            self.force_rect[0] - self.param['image_w'] // 2, self.force_rect[1] - self.force, self.param['image_w'],
            self.force * 2)

    def rectInMap(self):
        self.force_rect = self.getCoordsInFrameForMapRect()
        self.force_rect = (
            self.force_rect[0] - self.param['image_w'] // 2, self.force_rect[1] - self.force, self.param['image_w'],
            self.force * 2)

    def getCoordsInFrame(self):
        coords_on_screen = (
            self.map.coords_about_screean[0] + self.x_y[0] - self.param['image_w'] // 2,
            self.map.coords_about_screean[1] + self.x_y[1] - self.param['image_h'])
        return coords_on_screen

    def getCoordsInFrameForMapRect(self):
        coords_on_screen = (
            self.map.coords_about_screean[0] + self.x_y[0],
            self.map.coords_about_screean[1] + self.x_y[1])
        return coords_on_screen

    def update(self, fps, point, mouse_button_down, mouse_button_down_r):
        self.updateInterectiveObj(fps, point, mouse_button_down, mouse_button_down_r)

    def updateInterectiveObj(self, fps, point, mouse_button_down, mouse_button_down_r):
        self.rect.x, self.rect.y = self.getCoordsInFrame()
        self.collideMouse(point, mouse_button_down, mouse_button_down_r)
        self.rectInMap()
        if 0 < self.timer < 200:
            text = font.render(self.param['comment'], 1, (83, 189, 104))
            text_x = self.rect.x + (self.rect.w - text.get_width()) // 2
            text_y = self.rect.y - 50
            self.screen.blit(text, (text_x, text_y))
            self.timer += 1
        if self.timer > 200:
            self.timer = 0
        self.image = self.frames[self.naptr][self.cur_frame[0]][self.cur_frame[1]]

    def interactionAction(self):
        pass

    def interaction(self):
        if not self.interacted and self.player.collideRectImMap(self.force_rect, 0, 0, 25,
                                                                25) and self.may_be_interacted:
            self.interacted = True
            if self.param['colomns'] > 1:
                self.cur_frame = (0, 1)
            self.interactionAction(self)
        elif self.interacted and self.player.collideRectImMap(self.force_rect, 0, 0, 25, 25) and self.may_be_interacted:
            self.interacted = False
            self.cur_frame = (0, 0)

    def collideMouse(self, point, mouse_button_down, mouse_button_down_r):
        if self.rect.collidepoint(point):
            if mouse_button_down_r:
                self.timer = 1
            elif mouse_button_down:
                self.interaction()


class InteractionContainer(InteractionObject):
    def __init__(self, group, screen, x_y, map_, obj_name, player, arg=None, may_be_interacted=True):
        super().__init__(group, screen, x_y, map_, obj_name, player, arg, may_be_interacted)
        self.conteiners = pygame.sprite.Group()
        self.opened = False
        self.container = ThingBox(self.conteiners, self.param['num_of_cells'], [self.rect.x
            , self.rect.y], self.player)

    def update(self, fps, point, mouse_button_down, mouse_button_down_r):
        self.updateInterectiveObj(fps, point, mouse_button_down, mouse_button_down_r)
        if self.opened:
            self.updateContainer(fps, point, mouse_button_down, mouse_button_down_r)

    def updateContainer(self, fps, point, mouse_button_down, mouse_button_down_r):
        self.container.changeCoords(self.rect.x - self.rect.w // 2, self.rect.y - 105)
        self.conteiners.draw(self.screen)
        self.conteiners.update(fps, point, mouse_button_down, mouse_button_down_r)


class DefaultThing(pygame.sprite.Sprite):
    def __init__(self, group, obj_name, x_y, stack_size, level):
        super().__init__(group)
        self.name = obj_name
        self.level = level
        self.param = thing_param[obj_name]
        self.image = load_image(self.param['image'])
        self.rect = self.image.get_rect()
        if self.name != 'default_thing':
            self.x_y = x_y
            self.rect.x, self.rect.y = self.getCoordsInFrame()
            self.stack_size = stack_size
            self.taked = False
            self.eq_coords = (0, 0)
            self.in_box = False
        else:
            self.rect.x, self.rect.y = x_y
        self.box = None

    def changeCoords(self, x, y):
        self.rect.x, self.rect.y = x, y

    def getCoordsInFrame(self):
        coords_on_screen = (
            self.level.map_.coords_about_screean[0] + self.x_y[0],
            self.level.map_.coords_about_screean[1] + self.x_y[1])
        return coords_on_screen

    def setBox(self, box, x, y):
        self.in_box = True
        self.box = box
        self.taked = False
        self.rect.x, self.rect.y = x, y

    def getCoordsOnMap(self, coords):
        coords_on_map = (
            coords[0] - self.level.map_.coords_about_screean[0], coords[1] - self.level.map_.coords_about_screean[1])
        return coords_on_map

    def takeThings(self, collide_or_not, mouse, point):
        if self.name != 'default_thing':
            if collide_or_not:
                self.showStack()
            if mouse and collide_or_not and not self.taked and not self.level.i_have_taked_thing:
                if self.in_box:
                    self.box.giveThing(self)
                else:
                    self.taked = True
                    self.level.i_have_taked_thing = True
                self.eq_coords = (point[0] - self.rect.x, point[1] - self.rect.y)
                return 0
            if not self.in_box:
                if mouse and self.taked:
                    self.taked = False
                    self.level.i_have_taked_thing = False
                    self.x_y = self.getCoordsOnMap((self.rect.x, self.rect.y))
                    self.rect.x, self.rect.y = self.getCoordsInFrame()
                elif self.taked:
                    self.rect.x, self.rect.y = point[0] - self.eq_coords[0], point[1] - self.eq_coords[1]
                elif not self.taked:
                    self.rect.x, self.rect.y = self.getCoordsInFrame()
            else:
                if collide_or_not:
                    text = font.render(self.param['actions'], 1, (0, 0, 0))
                    text_x = self.rect.x + (self.rect.w - text.get_width()) // 2
                    text_y = self.rect.y - 50
                    self.level.screen.blit(text, (text_x, text_y))

    def update(self, fps, point, mouse, *args):
        collide_or_not = self.rect.collidepoint(point)
        self.takeThings(collide_or_not, mouse, point)

    def showStack(self):
        text = font1.render(str(self.stack_size), 1, (0, 0, 0))
        text_x = self.rect.x + (self.rect.w - text.get_width()) // 2
        text_y = self.rect.y + self.rect.h + 3
        self.level.screen.blit(text, (text_x, text_y))
        temp = text.get_height()
        text = font1.render(' '.join(self.name.split('_')).title(), 1, (0, 0, 0))
        text_x = self.rect.x + (self.rect.w - text.get_width()) // 2
        text_y = self.rect.y + self.rect.h + 6 + temp
        self.level.screen.blit(text, (text_x, text_y))


class UsebaleThings(DefaultThing):
    def __init__(self, group, obj_name, x_y, stack_size, level):
        super().__init__(group, obj_name, x_y, stack_size, level)
        self.strength = self.param['strength']
        self.for_one_use = self.param['usage']
        self.func = self.param['func']

    def showStack(self):
        text = font1.render(str(self.stack_size), 1, (255, 255, 255))
        text_x = self.rect.x + (self.rect.w - text.get_width()) // 2
        text_y = self.rect.y + self.rect.h + 3
        self.level.screen.blit(text, (text_x, text_y))
        temp = text.get_height()
        text = font1.render(' '.join(self.name.split('_')).title(), 1, (255, 255, 255))
        text_x = self.rect.x + (self.rect.w - text.get_width()) // 2
        text_y = self.rect.y + self.rect.h + 6 + temp
        self.level.screen.blit(text, (text_x, text_y))
        text_y = self.rect.y + self.rect.h + 6 + temp
        temp = text.get_height()
        text = font1.render(str(self.strength), 1, (255, 255, 255))
        text_x = self.rect.x + (self.rect.w - text.get_width()) // 2
        text_y += temp
        self.level.screen.blit(text, (text_x, text_y))

    def useThing(self, level, x, y):
        self.func(level, x, y)
        self.strength += self.for_one_use
        if self.strength <= 0:
            self.level.player_main.inventary.deleteThing(th=self)

    def areWeUseThing(self, collide_or_not, mouse_b_r):
        if mouse_b_r:
            if collide_or_not:
                self.level.player_main.state = 'use'
                self.level.player_main.equipped = self

    def update(self, fps, point, mouse, mouse_b_r, *args):
        collide_or_not = self.rect.collidepoint(point)
        self.takeThings(collide_or_not, mouse, point)
        self.areWeUseThing(collide_or_not, mouse_b_r)


class ThingBox(pygame.sprite.Sprite):
    def __init__(self, gruop, num_of_cell, x_y, player):
        super().__init__(gruop)
        self.player = player
        self.image = pygame.Surface([num_of_cell * 70 + (num_of_cell + 1) * 10, 90])
        self.image.fill(pygame.Color("brown"))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x_y
        self.cells_group = pygame.sprite.Group()
        self.cells = [DefaultThing(self.cells_group, 'default_thing', [i, x_y[1] + 10], 1,
                                   self.player.level) for i in
                      range(self.rect.x + 10, self.rect.x + num_of_cell * 80, 80)]

    def changeCoords(self, x, y):
        self.rect.x, self.rect.y = x, y
        x = self.rect.x + 10
        y = self.rect.y + 10
        for i in self.cells:
            i.changeCoords(x, y)
            x += 80

    def collideRectImMap(self, rect):
        x, y, w, h = rect

        x1, y1, w1, h1 = self.rect
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

    def collideAnyInMap(self):
        for i in self.player.level.things_ogf_spr:
            if self.collideRectImMap(i.rect) and i not in self.cells and not i.taked:
                return i
        for i in self.player.level.usebale_things_ogf_spr:
            if self.collideRectImMap(i.rect) and i not in self.cells and not i.taked:
                return i

    def takeThing(self, thing):
        indx = mod(- self.rect.x + thing.rect.x - 10) // 80
        temp = self.cells[indx]
        if temp.name == thing.name:
            temp.stack_size += thing.stack_size
            thing.kill()
            return
        if temp.name != 'default_thing':
            self.giveThing(self.cells[indx])
        else:
            self.cells[indx].kill()
        self.cells[indx] = thing
        self.cells_group.add(thing)
        thing.setBox(self, self.rect.x + 10 + indx * 80, self.rect.y + 10)
        if thing.param['type'] == 'useable_things':
            self.player.level.usebale_things_ogf_spr.remove(thing)
        elif thing.param['type'] == 'food' or thing.param['type'] == 'matirial_things':
            self.player.level.things_ogf_spr.remove(thing)

    def giveThing(self, th):
        indx = self.cells.index(th)
        self.cells[indx].in_box = False
        self.cells[indx].box = None
        self.cells[indx].taked = True
        self.player.level.i_have_taked_thing = True

        if th.param['type'] == 'useable_things':
            self.player.level.usebale_things_ogf_spr.add(th)
        elif th.param['type'] == 'food' or th.param['type'] == 'matirial_things':
            self.player.level.things_ogf_spr.add(th)
        self.cells_group.remove(self.cells[indx])
        self.cells[indx] = DefaultThing(self.cells_group, 'default_thing',
                                        [self.rect.x + indx * 80 + 10, self.rect.y + 10], 1,
                                        self.player.level)

    def countThatThings(self, thing, need):
        res = 0
        indexes = []
        for i in range(len(self.cells)):
            if res >= need:
                res = need
                break
            if self.cells[i].name == thing:
                res += int(self.cells[i].stack_size)
                indexes.append(i)
        return (res, indexes)

    def deleteThing(self, th=None, indx=None):
        if not th is None:
            indx = self.cells.index(th)
        self.cells[indx].kill()
        self.cells[indx] = DefaultThing(self.cells_group, 'default_thing',
                                        [self.rect.x + indx * 80 + 10, self.rect.y + 10], 1,
                                        self.player.level)

    def takeThingForCraft(self, thing_indxs, need):
        for i in thing_indxs:
            if need >= self.cells[i].stack_size:
                need -= self.cells[i].stack_size
                self.deleteThing(indx=i)

            else:
                self.cells[i].stack_size -= need
                break

    def update(self, fps, point, mouse_button_down, mouse_button_down_r):

        self.cells_group.update(fps, point, mouse_button_down, mouse_button_down_r)
        self.cells_group.draw(self.player.level.screen)

        thing = self.collideAnyInMap()
        if thing:
            self.takeThing(thing)
