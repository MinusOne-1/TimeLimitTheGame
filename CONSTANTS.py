import pygame
import os


# функция для загрузки картинок
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pygame.init()
size = width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
font = pygame.font.Font('data/m_Brody Regular.ttf', 50)
# досаём карты из файла
Maps = open('maps.txt', 'r')
m = Maps.readlines()
Maps.close()
Maps = []
for i in m:
    if 'begin' in i:
        Maps.append([])
        continue
    Maps[-1].append(i[:-1])


def portal(self):
    self.player.level.level_state = 'win'

# статические объекты, доступные для создания
static_obj_param = {'broken_portal': {'num_of_anim': 1,
                                      'images': ['static_objects_images/broken_portal.png', 'img_r', 'img_u', 'img_d'],
                                      'image_w': 280, 'image_h': 400,
                                      'rows': 7, 'colomns': 2, 'comment': 'That a portal!.. Ow... It`s broken...'}}
dinamic_obj_param = {}
interaction_obj_param = {'cup_of_power':
                             {'num_of_anim': 1,
                              'images': ['interaction_object_image/cup.png', 'img_r', 'img_u', 'img_d'],
                              'image_w': 280, 'image_h': 400, 'rows': 1, 'colomns': 2,
                              'comment': 'I think it`s want a power-thing',
                              'num_of_cell': 1, 'fuc': lambda u: u},
                         'end_portal': {'num_of_anim': 1,
                              'images': ['interaction_object_image/portal.png', 'img_r', 'img_u', 'img_d'],
                              'image_w': 265, 'image_h': 402, 'rows': 1, 'colomns': 2,
                              'comment': 'Wow! May be it is the End...', 'fuc': portal}}
thing_param = {'name_thing': {'image': 'iamge.png',
                              'strength': 100, 'usage': -10, 'comment': ''},
               'name_food': {'image': 'thig_obj_images/food_obj_images/eggs_img.png', 'comment': '',
                             'calorie': 10, 'heal': 0, 'red_madness': 0},
               'name_matirial': {'image': 'thig_obj_images/thing_obj_img/dead_grass.png', 'comment': ''},
               'default_thing': {'image': 'thig_obj_images/thing_obj_img/default_image.png', 'comment': ''}}

