# важные импорты
import pygame
from CONSTANTS import width, height


# установка окружния основные иниты
clock = pygame.time.Clock()
pygame.init()
running = True
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption('Time Limit!')
full_screen_mod = True
fps = clock.tick() / 1000
from Level import GameLevel, MainMenu

menu = MainMenu(screen)
game = GameLevel(screen)

# Основной цикл
while running:
    mouse_button_down = False
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_button_down = True

    fps = clock.tick() / 1000

    point = pygame.mouse.get_pos()
    if menu.game_stat == 'Main_menu':
        menu.update(point, mouse_button_down)
        menu.render()
    elif menu.game_stat == 'Playing':
        game.update(fps)
        game.render(fps, point)
    elif menu.game_stat == 'Pause_menu':
        pass
    pygame.display.flip()
