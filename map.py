import pygame
from CONSTANTS import Maps, width, height, load_image

tile_images = {'r_grass_end': load_image('textur/end_of_grass_from_up.png'),
               'l_grass_end': pygame.transform.flip(load_image('textur/end_of_grass_from_up.png'), True, False),
               'd_grass_end': load_image('textur/end_of_grass_from_up_u_d.png'),
               'u_grass_end': pygame.transform.flip(load_image('textur/end_of_grass_from_up_u_d.png'), False, True),
               'left_grass_end_r_u_angle': load_image('textur/end_of_grass_angle.png'),
               'left_grass_end_r_d_angle': pygame.transform.flip(load_image('textur/end_of_grass_angle.png'), False,
                                                                 True),
               'left_grass_end_l_d_angle': pygame.transform.flip(load_image('textur/end_of_grass_angle.png'), True,
                                                                 True),
               'left_grass_end_l_u_angle': pygame.transform.flip(load_image('textur/end_of_grass_angle.png'), True,
                                                                 False),
               'front_grass_end': load_image('textur/end_of_grass.png'),
               'grass_end_d_u': load_image('textur/end_of_grass_two_sides_u_d.png'),
               'grass_end_l_r': load_image('textur/end_of_grass_two_sides_l_r.png'),
               'grass_end_three_sides_u_r_d': load_image('textur/end_of_grass_three_sides.png'),
               'grass_end_three_sides_u_l_d': pygame.transform.flip(load_image('textur/end_of_grass_three_sides.png'),
                                                                    True, False),
               'grass_end_three_sides_u_r_l': load_image('textur/end_of_grass_three_sides_u_d.png'),
               'grass_end_three_sides_d_l_r': pygame.transform.flip(load_image('textur/end_of_grass_three_sides_u_d.png'),
                                                                    False, True),
               'void': load_image('textur/plain_grass.png'),
               'plain_grass': load_image('textur/plain_grass.png')}


class Map():
    def __init__(self, screen):
        self.map = self.map_generate()
        self.map_surfaces = []
        self.screen = screen
        self.coords_about_screean = [0, 0]
        self.first_player_coords = None
        self.map_drawing()

    def map_generate(self):
        return Maps[0]

    def changeCoords(self, x_y):
        self.coords_about_screean = x_y

    def map_drawing(self):
        sur = pygame.Surface((len(self.map) * 300, len(self.map[0]) * 300))
        self.map_surfaces.append(sur)
        self.map_surfaces[0].fill((50, 50, 50))
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == '~':
                    pass
                    # sur.blit(tile_images['void'], (i * 300, j * 300))
                elif self.map[i][j] == 'g':
                    if self.first_player_coords is None:
                        self.first_player_coords = (j * 300 + 70, i * 300 + 70)
                    ends = self.checkEnds(i, j)  # низ лево верх право
                    if ends[0] and ends[1] and not ends[2] and ends[3]:
                        sur.blit(tile_images['grass_end_three_sides_d_l_r'], (j * 300, i * 300))
                        continue
                    if not ends[0] and ends[1] and ends[2] and ends[3]:
                        sur.blit(tile_images['grass_end_three_sides_u_r_l'], (j * 300, i * 300))
                        continue
                    if ends[0] and not ends[1] and ends[2] and ends[3]:
                        sur.blit(tile_images['grass_end_three_sides_u_r_d'], (j * 300, i * 300))
                        continue
                    if ends[0] and ends[1] and ends[2] and not ends[3]:
                        sur.blit(tile_images['grass_end_three_sides_u_l_d'], (j * 300, i * 300))
                        continue
                    if not ends[0] and not ends[1] and ends[2] and ends[3]:
                        sur.blit(tile_images['left_grass_end_r_u_angle'], (j * 300, i * 300))
                        continue
                    if ends[0] and not ends[1] and not ends[2] and ends[3]:
                        sur.blit(tile_images['left_grass_end_r_d_angle'], (j * 300, i * 300))
                        continue
                    if not ends[0] and ends[1] and ends[2] and not ends[3]:
                        sur.blit(tile_images['left_grass_end_l_u_angle'], (j * 300, i * 300))
                        continue
                    if ends[0] and ends[1] and not ends[2] and not ends[3]:
                        sur.blit(tile_images['left_grass_end_l_d_angle'], (j * 300, i * 300))
                        continue
                    if not ends[0] and ends[1] and not ends[2] and ends[3]:
                        sur.blit(tile_images['grass_end_l_r'], (j * 300, i * 300))
                        continue
                    if ends[0] and not ends[1] and ends[2] and not ends[3]:
                        sur.blit(tile_images['grass_end_d_u'], (j * 300, i * 300))
                        continue
                    if ends[0] and not ends[1] and not ends[2] and not ends[3]:
                        sur.blit(tile_images['d_grass_end'], (j * 300, i * 300))
                        continue
                    if ends[1] and not ends[0] and not ends[2] and not ends[3]:
                        sur.blit(tile_images['l_grass_end'], (j * 300, i * 300))
                        continue
                    if ends[2] and not ends[1] and not ends[0] and not ends[3]:
                        sur.blit(tile_images['u_grass_end'], (j * 300, i * 300))
                        continue
                    if ends[3] and not ends[1] and not ends[2] and not ends[0]:
                        sur.blit(tile_images['r_grass_end'], (j * 300, i * 300))
                        continue
                    sur.blit(tile_images['plain_grass'], (j * 300, i * 300))
        self.map_surfaces.append(sur)

    def checkEnds(self, i, j):
        # низ лево верх право
        ends = [False, False, False, False]
        if self.map[i + 1][j] == '~':
            ends[0] = True
        if self.map[i][j - 1] == '~':
            ends[1] = True
        if self.map[i - 1][j] == '~':
            ends[2] = True
        if self.map[i][j + 1] == '~':
            ends[3] = True
        return ends

    def draw(self):
        self.screen.blit(self.map_surfaces[0], self.coords_about_screean)
