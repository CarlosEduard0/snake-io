import random
import select
import socket
import threading
import time

import pickle

import pygame

from Snack import Snack
from Snake import Snake


def gen_snack():
    global serverData
    while True:
        snack = Snack()
        if not (snack in serverData['snacks']):
            serverData['snacks'].append(snack)
        time.sleep(1)


def move_snakes():
    global serverData
    while True:
        for snake in serverData['snakes']:
            snake.move()
            snack = Snack(snake.body[0])
            if any(i == snack for i in serverData['snacks']):
                snake.grow()
                serverData['snacks'].remove(snack)

            snakes = []
            for i in [x for x in serverData['snakes'] if x.id != snake.id]:
                for j in i.body:
                    snakes.append(j)
            if snake.body[0] in snake.body[1:] or snake.body[0] in snakes:
                for position in snake.body:
                    serverData['snacks'].append(Snack(position))
                serverData['snakes'].remove(snake)
        time.sleep(0.05)


port = 65432
read_list = []
serverData = {'snacks': [Snack((300, 400), (255, 255, 255))],
              'snakes': []}
              # 'snakes': [Snake(30, (100, 100), pygame.K_RIGHT, (0,0,0)),Snake(40, (200, 200), pygame.K_RIGHT, (0,0,0)),Snake(50, (200, 200), pygame.K_RIGHT, (0,0,0))]}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setblocking(False)
    s.bind(('', port))
    s.listen(5)
    read_list.append(s)
    threading.Thread(target=gen_snack).start()
    threading.Thread(target=move_snakes).start()
    while True:
        readable, writeable, error = select.select(read_list, [], [], 0.05)
        for sock in readable:
            if sock is s:
                conn, info = sock.accept()
                read_list.append(conn)
                serverData['snakes'].append(Snake(info[1], (random.randint(0, 49) * 10, random.randint(0, 49) * 10), pygame.K_RIGHT, (random.randint(0, 254), random.randint(0, 254), random.randint(0, 254))))
                print("connection received from ", info)
            else:
                try:
                    data = sock.recv(1024)
                    if data:
                        try:
                            snake = next(s for s in serverData['snakes'] if s.id == sock.getpeername()[1])
                            snake.direcao = int(str(data, 'utf-8'))
                        except StopIteration:
                            pass
                    else:
                        sock.close()
                        read_list.remove(sock)
                except:
                    pass

        if not (readable or writeable or error):
            for sock in read_list:
                if not (sock is s):
                    sock.send(pickle.dumps(serverData))
