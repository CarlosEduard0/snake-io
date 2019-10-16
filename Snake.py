import pygame



class Snake:
    def __init__(self, id, start, direcao, color):
        self.id = id
        self.body = []
        self.body.append(start)
        self.body.append(((start[0] - 10) % 500, start[1]))
        self.body.append(((start[0] - 20) % 500, start[1]))
        self.direcao = direcao
        self.color = color

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i] = (self.body[i - 1][0], self.body[i - 1][1])

        if self.direcao == pygame.K_UP:
            self.body[0] = (self.body[0][0], (self.body[0][1] - 10) % 500)
        if self.direcao == pygame.K_RIGHT:
            self.body[0] = ((self.body[0][0] + 10) % 500, self.body[0][1])
        if self.direcao == pygame.K_DOWN:
            self.body[0] = (self.body[0][0], (self.body[0][1] + 10) % 500)
        if self.direcao == pygame.K_LEFT:
            self.body[0] = ((self.body[0][0] - 10) % 500, self.body[0][1])

    def grow(self):
        self.body.append((0, 0))
