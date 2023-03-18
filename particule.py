import pygame
import random

class Particule:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.moves = []
        self.score = [0, 0]
        self.onPath = 0

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 5)

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_color(self, color):
        self.color = color

    def get_moves(self):
        return self.moves

    def set_moves(self, moves):
        self.moves = moves

    def add_move(self, move):
        self.moves.append(move)

    def get_move(self, index):
        return self.moves[index]
    
    def set_move(self, index, move):
        self.moves[index] = move
    
    def get_score(self):
        return self.score
    
    def set_score(self, score):
        self.score = score

    def get_onPath(self):
        return self.onPath
    
    def set_onPath(self, onPath):
        self.onPath = onPath