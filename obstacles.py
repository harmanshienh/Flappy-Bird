import pygame, os.path
from config import * 
class Obstacles(pygame.sprite.Sprite):
    def __init__(self, pos, y) -> None:
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load(self.accessFile("pipe-green.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = pygame.Vector2(-5, 0)

        if self.pos == "bottom":
            self.rect.bottomleft = pygame.Vector2(WIDTH, HEIGHT + 360 + y)
        elif self.pos == "top":
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect.bottomleft = pygame.Vector2(WIDTH, HEIGHT - 360 + y)
    
    def update(self):
        self.rect.center += self.speed
        if self.rect.right == 0:
            self.kill()
            del self
    
    @staticmethod
    def accessFile(filename:str) -> str:
        cwd = os.path.dirname(__file__)
        path = f"{cwd}/Assets/sprites/{filename}"
        return path