import pygame, os.path
from config import *
class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.birdSpritesheet = pygame.image.load(self.accessFile("bird-spritesheet.png")).convert_alpha()
    
        self.index = 1
        self.rotation = 0
        self.rotationExponent = 0

        self.birdImages = [] 
        for i in range(3): 
            img = self.getImage(self.birdSpritesheet, 0, i, 34, 24) 
            img = pygame.transform.scale(img, (51, 36)) 
            self.birdImages.append(img) 
        
        self.titleSpeeds = [(0, 5), (0, -10), (0, 5)]

        self.image = self.birdImages[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = pygame.Vector2(WIDTH / 4, HEIGHT / 2)
    
    def handleKeyPresses(self, event:int):
        if event.key == pygame.K_SPACE:
            self.playSFX("wing.wav")
            self.rect.center += pygame.Vector2(0, -60)
            self.rotation = 30
            self.rotationExponent = 0
            self.image = pygame.transform.rotate(self.image, self.rotation)
    
    def update(self, state:str):
        if state == "TITLE":
            self.rect.center += pygame.Vector2(self.titleSpeeds[self.index])
            self.index += 1
            if self.index > 2:
                self.index = 0
            self.image = self.birdImages[self.index]

        elif state == "GAME":
            self.rect.center += pygame.Vector2(0, 5)
            self.index += 1
            if self.index > 2:
                self.index = 0
            self.image = self.birdImages[self.index]
            self.image = pygame.transform.rotate(self.image, self.rotation)
            if self.rotation > -70:
                self.rotation -= 1.08 ** self.rotationExponent
                self.rotationExponent += 1
            if self.rotation < -70:
                self.rotation = -70

        elif state == "TRANSITION":
            self.rect.center += pygame.Vector2(0, 20)

    def playSFX(self, filename:str):
        sound = pygame.mixer.Sound(self.accessAudio(filename))
        sound.play()

    @staticmethod
    def accessFile(filename:str) -> str:
        cwd = os.path.dirname(__file__)
        path = f"{cwd}/Assets/sprites/{filename}"
        return path

    @staticmethod
    def accessFile(filename:str) -> str:
        cwd = os.path.dirname(__file__)
        path = f"{cwd}/Assets/sprites/{filename}"
        return path
    
    @staticmethod
    def accessAudio(filename:str) -> str:
        cwd = os.path.dirname(__file__)
        path = f"{cwd}/Assets/audio/{filename}"
        return path

    @staticmethod
    def getImage(spritesheet, row, col, width, height):
        img = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        x = col * width
        y = row * height
        img.blit(spritesheet, (0, 0), (x, y, width, height))
        return img