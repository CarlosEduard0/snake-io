import socket
import time

import pickle
import pygame


def redrawWindow(screen, serverData):
    screen.fill((0, 0, 0))
    surface = pygame.Surface((10, 10))
    for i in serverData['snacks']:
        surface.fill(i.color)
        screen.blit(surface, i.position)
    for i in serverData['snakes']:
        surface.fill(i.color)
        for j in i.body:
            screen.blit(surface, j)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('localhost', 65432))
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()

    while True:
        clock.tick(20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    s.sendall(str(pygame.K_UP).encode())
                if event.key == pygame.K_RIGHT:
                    s.sendall(str(pygame.K_RIGHT).encode())
                if event.key == pygame.K_DOWN:
                    s.sendall(str(pygame.K_DOWN).encode())
                if event.key == pygame.K_LEFT:
                    s.sendall(str(pygame.K_LEFT).encode())

        try:
            data = s.recv(10240)
            if data:
                redrawWindow(screen, pickle.loads(data))
                pygame.display.update()
            else:
                break
        except:
            pass