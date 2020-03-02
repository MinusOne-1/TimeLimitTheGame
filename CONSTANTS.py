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
font1 = pygame.font.Font('data/m_Brody Regular.ttf', 20)
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

#функции для некоторых предметов

def box(self):
    self.interacted = False
    if self.opened:
        self.cur_frame = (0,0)
        self.opened = False
    else:
        self.opened = True
        self.cur_frame = (0, 1)

def portal(self):
    self.player.level.level_state = 'win'

def gate(u):
    u.timer = 1

def switch_gate(u):
    u.interacted = False
    u.timer = 1
    if u.args_for_interaction.interacted:
        u.args_for_interaction.param['comment'] = 'It`s closed!'
        u.args_for_interaction.interacted = False
        u.args_for_interaction.force = u.args_for_interaction.param['force']
        u.args_for_interaction.cur_frame = (0, 0)
        u.cur_frame = (0, 0)
    else:
        u.args_for_interaction.param['comment'] = 'Opened! Great!'
        u.args_for_interaction.force = 0
        u.args_for_interaction.cur_frame = (0, 1)
        u.args_for_interaction.interacted = True
        u.cur_frame = (0, 1)
    print(u.args_for_interaction.param['comment'])


# статические объекты, доступные для создания
static_obj_param = {'broken_portal': {'num_of_anim': 1,
                                      'images': ['static_objects_images/broken_portal.png', 'img_r', 'img_u', 'img_d'],
                                      'image_w': 280, 'image_h': 400, 'force': 20, 'type':'static_obj',
                                      'rows': 7, 'colomns': 2, 'comment': 'That a portal!.. Ow... It`s broken...'}
                    , 'sign_1': {'num_of_anim': 0,
                                      'images': ['static_objects_images/signt_arrows.png', 'img_r', 'img_u', 'img_d'],
                                      'image_w': 250, 'image_h': 300,'force': 10, 'type':'static_obj',
                                      'rows': 1, 'colomns': 1, 'comment': ''},
                    'sign_2': {'num_of_anim':0,
                               'images': ['static_objects_images/signt_health.png', 'img_r', 'img_u', 'img_d'],
                               'image_w': 250, 'image_h': 300,'force': 10, 'type':'static_obj',
                               'rows': 1, 'colomns': 1, 'comment': ''},
                    'sign_3': {'num_of_anim': 0,
                               'images': ['static_objects_images/signt_mad.png', 'img_r', 'img_u', 'img_d'],
                               'image_w': 250, 'image_h': 300, 'force': 10, 'type':'static_obj',
                               'rows': 1, 'colomns': 1, 'comment': ''},
                    'sign_4': {'num_of_anim': 0,
                               'images': ['static_objects_images/sign_things.png', 'img_r', 'img_u', 'img_d'],
                               'image_w': 250, 'image_h': 300, 'force': 10, 'type':'static_obj',
                               'rows': 1, 'colomns': 1, 'comment': ''},
                    'sign_5': {'num_of_anim': 0,
                               'images': ['static_objects_images/sign_interaction.png', 'img_r', 'img_u', 'img_d'],
                               'image_w': 250, 'image_h': 300, 'force': 10, 'type':'static_obj',
                               'rows': 1, 'colomns': 1, 'comment': ''}
                    }
dinamic_obj_param = {}
interaction_obj_param = {'cup_of_power':
                             {'num_of_anim': 1,
                              'images': ['interaction_object_image/cup.png', 'img_r', 'img_u', 'img_d'],
                              'image_w': 280, 'image_h': 400, 'rows': 1, 'colomns': 2, 'type':'interaction_obj',
                              'comment': 'I think it`s want a power-thing', 'force': 70,
                              'num_of_cell': 1, 'fuc': lambda u: u},
                         'end_portal': {'num_of_anim': 1,
                              'images': ['interaction_object_image/portal.png', 'img_r', 'img_u', 'img_d'],
                              'image_w': 265, 'image_h': 402, 'rows': 1, 'colomns': 2, 'force': 20,  'type':'interaction_obj',
                              'comment': 'Wow! May be it is the End...', 'fuc': portal},
                         'spatial_discontinuity': {'num_of_anim': 1,
                                        'images': ['interaction_object_image/spatial_discontinuity.png', 'img_r', 'img_u', 'img_d'],
                                        'image_w': 205, 'image_h': 100, 'rows': 1, 'colomns': 1, 'type':'interaction_obj',
                                        'comment': 'Maybe it leads somewhere...', 'force': 50,
                                                   'fuc': lambda u: u.player.teleportTo(u.args_for_interaction.x_y[0] + 50, u.args_for_interaction.x_y[1] + 90)},
                         'switch_gate':{'num_of_anim': 1,
                                        'images': ['interaction_object_image/switch_gate.png', 'img_r', 'img_u', 'img_d'],
                                        'image_w': 200, 'image_h': 200, 'rows': 1, 'colomns': 2, 'force': 10,
                                        'comment': 'Something has to change?', 'type':'interaction_obj',
                                                   'fuc': switch_gate},
                         'gate':{'num_of_anim': 1,
                                        'images': ['interaction_object_image/gate.png', 'img_r', 'img_u', 'img_d'],
                                        'image_w': 300, 'image_h': 200, 'rows': 1, 'colomns': 2,
                                        'comment': 'It`s closed!', 'force': 20, 'type':'interaction_obj',
                                                   'fuc': gate},
                         'casket': {'num_of_anim': 1,
                                  'images': ['interaction_object_image/casket.png', 'img_r', 'img_u', 'img_d'],
                                  'image_w': 150, 'image_h': 150, 'rows': 1, 'colomns': 2, 'type':'interaction_obj',
                                  'comment': 'It looks like the one in my lab...', 'force': 40, 'num_of_cells': 3,
                                  'fuc': box}
                         }
thing_param = {'name_useable_thing':
                   {'image': 'iamge.png', 'actions': 'Drop/Use',
                              'strength': 100, 'usage': -10, 'comment': '', 'type': 'useable_things', 'type_of_use':'spawn/attack'},
               'name_food':
                   {'image': 'thig_obj_images/food_obj_images/eggs_img.png', 'comment': '',
                             'calorie': 10, 'heal': 0, 'red_madness': 0, 'actions': 'Drop/Eat', 'type':'food'},
               'name_matirial':
                   {'image': 'thig_obj_images/thing_obj_img/dead_grass.png',
                    'actions': 'Drop', 'comment': '', 'type': 'matirial_things'},
               'default_thing':
                   {'image': 'thig_obj_images/thing_obj_img/default_image.png',
                    'comment': '', 'type': 'default_thing'},
               'grass_matirial':
                   {'image': 'thig_obj_images/thing_obj_img/dead_grass.png', 'actions': 'Drop', 'comment': '',
                                 'recipe': [], 'type': 'matirial_things'},
               'rope_matirial':
                   {'image': 'thig_obj_images/thing_obj_img/rope.png', 'actions': 'Drop', 'comment': 'Do you want to bind someone?',
                                 'recipe': ['grass_matirial 3'], 'type': 'matirial_things'},
               'stick_matirial':
                   {'image': 'thig_obj_images/thing_obj_img/stick.png',
                    'actions': 'Drop', 'comment': '', 'type': 'matirial_things'},
               'grass_stick':
                   {'image': 'thig_obj_images/thing_obj_img/grass_stick.png', 'actions': 'Drop/Use',
                              'strength': 100, 'usage': -10, 'comment': '', 'type': 'useable_things',
                    'recipe': ['grass_matirial 3', 'stick_matirial 3', 'rope_matirial 3', 'light 50'],
                    'func':lambda u, x, y: u.spawn('interaction', 'bush', x, y)}}
def mod(a):
    if a < 0:
        return -a
    return a
