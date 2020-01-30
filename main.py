# важные импорты
import pygame
from CONSTANTS import width, height, fps

# установка окружния основные иниты
clock = pygame.time.Clock()
pygame.init()
running = True
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption('Time Limit!')
full_screen_mod = True

# группы спрайтов
menu_sprite = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
static_obj_sprite = pygame.sprite.Group()
dinamic_obj_sprite = pygame.sprite.Group()
fps = clock.tick() / 1000
# Побочные импорты
from Player import Player, Menu
from map import Map

class MenuSprite():
    def __init__(self, group):
        self.player = player_main
        self.menu = Menu(group, self.player, screen)

    def update(self, clock, fps):
        self.menu.update(clock, fps)


# Переменные, создание объектов
map_ = Map(screen)
player_main = Player(player_sprite, map_)
player_main.teleportTo(map_.first_player_coords[0], map_.first_player_coords[1])
map_.changeCoords([-player_main.x_y[0] + width // 2,
                   -player_main.x_y[1] + height // 2 + player_main.image.get_height() // 2 - 10])
MenuSprite(menu_sprite)
# Основной цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not full_screen_mod:
                    full_screen_mod = True
                    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                else:
                    full_screen_mod = False
                    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
            # вспомогательные события
            if event.key == pygame.K_SPACE:
                player_main.changeMadnessAbout(15)
            if event.key == pygame.K_x:
                player_main.changeHungerAbout(-15, fps)
            if event.key == pygame.K_g:
                if player_main.i_may_go:
                    player_main.i_may_go = False
                else:
                    player_main.i_may_go = True
    player_sprite.update(fps)

    screen.fill((50, 50, 50))
    map_.draw()

    player_sprite.draw(screen)
    menu_sprite.update(fps)
    menu_sprite.draw(screen)


    fps = clock.tick() / 1000
    pygame.display.flip()
