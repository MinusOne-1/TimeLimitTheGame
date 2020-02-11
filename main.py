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
from Level import GameLevel, MainMenu, PauseMenu

menu = MainMenu(screen, width // 2 - 393 // 2, 100, 'load_frame_images/art_for_frames.png')
pause = PauseMenu(screen, menu, width // 2 - 393 // 2, 100)
win = PauseMenu(screen, menu, width // 2 - 393 // 2, 452, img='load_frame_images/win_frame.png')
fail = PauseMenu(screen, menu, width // 2 - 393 // 2, 442, img='load_frame_images/dead_frame.png')
game = GameLevel(screen, main_menu=menu)

# Основной цикл
while running:
    mouse_button_down = False
    mouse_button_down_r = False
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
            if event.key == pygame.K_SPACE:
                if game.player_main.state == 'craft':
                    game.player_main.state = 'stay'
                else:
                    game.player_main.state = 'craft'
            if event.key == pygame.K_TAB and menu.game_stat:
                menu.game_stat = 'Pause_menu'
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_button_down = True
            elif event.button == 3:
                mouse_button_down_r = True

    fps = clock.tick() / 1000
    point = pygame.mouse.get_pos()
    if menu.game_stat == 'Main_menu':
        menu.update(point, mouse_button_down)
        menu.render()
    elif menu.game_stat == 'Playing':
        game.render(fps, point, mouse_button_down, mouse_button_down_r)
    elif menu.game_stat == 'Pause_menu':
        pause.update(point, mouse_button_down)
        pause.render()
    elif menu.game_stat == 'WinFrame':
        win.update(point, mouse_button_down)
        win.render()
    elif menu.game_stat == 'DieFrame':
        fail.update(point, mouse_button_down)
        fail.render()
    pygame.display.flip()
