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
static_obj_param = {'test_obj': {'num_of_anim': 0, 'images': ['img_l', 'img_r', 'img_u', 'img_d'], 'comment': ''}}
