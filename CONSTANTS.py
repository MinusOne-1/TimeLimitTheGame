import pygame

pygame.init()
size = width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
fps = 60

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