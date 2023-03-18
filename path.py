import pygame
import sys

class Path:
    def __init__(self, corners, startColor, endColor, pathColor, pathWidth):
        self.start = corners[0]
        self.end = corners[len(corners) - 1]
        self.corners = corners
        self.startColor = startColor
        self.endColor = endColor
        self.pathColor = pathColor
        self.pathWidth = pathWidth

    def draw(self, surface):
        for i in range(len(self.corners) - 1):
            pygame.draw.line(surface, self.pathColor, self.corners[i], self.corners[i + 1], self.pathWidth)
            pygame.draw.circle(surface, self.pathColor, self.corners[i], self.pathWidth // 2)
        pygame.draw.circle(surface, self.startColor, self.start, 50)
        pygame.draw.circle(surface, self.endColor, self.end, 50)
        
    def get_start(self):
        return self.start
    
    def get_end(self):
        return self.end
    
    def get_corners(self):
        return self.corners
    
    def get_corner(self, index):
        return self.corners[index]
    
    def get_corner_count(self):
        return len(self.corners)
    
    def get_path_width(self):
        return self.pathWidth
    
    def set_path_width(self, width):
        self.pathWidth = width