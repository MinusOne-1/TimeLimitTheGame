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

# статические объекты, доступные для создания
static_obj_param = {'broken_portal': {'num_of_anim': 1,
                                      'images': ['static_objects_images/broken_portal.png', 'img_r', 'img_u', 'img_d'],
                                      'image_w': 280, 'image_h': 400,
                                      'rows': 7, 'colomns': 2, 'comment': 'That a portal!.. Ow... It`s broken...'}}
dinamic_obj_param = {}
interaction_obj_param = {}
thing_param = {'name_th': {'image': 'iamge.png', 'type': 'equipment/food',
                           'strength': 100, 'usage': -10, 'actions':'use/drop'}}
