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
from Level import GameLevel


game = GameLevel(screen)

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
                game.player_main.changeMadnessAbout(15)
            if event.key == pygame.K_x:
                game.player_main.changeHungerAbout(-15, fps)
            if event.key == pygame.K_g:
                if game.player_main.i_may_go:
                    game.player_main.i_may_go = False
                else:
                    game.player_main.i_may_go = True

    fps = clock.tick() / 1000
    game.update(fps)
    game.render(fps)
    pygame.display.flip()
