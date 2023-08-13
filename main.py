import pygame, sys, os.path, random
from config import *
from player import Player
from obstacles import Obstacles

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        pygame.display.set_icon(pygame.image.load(self.accessFile("favicon.jpg")))
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.states = {"TITLE":0, "GAME":1, "TRANSITION":2, "DEATH":3}

        self.totalTime = 0

        self.bg = pygame.image.load(self.accessFile("background-day.jpg")).convert_alpha()
        self.titleText = pygame.image.load(self.accessFile("titletext.png")).convert_alpha()
        self.numSpritesheet = pygame.image.load(self.accessFile("num-spritesheet.png")).convert_alpha()

        self.obstacles = pygame.sprite.Group()
        self.numObstacles = 0
        self.obstacleSpawnTime = 2000
        self.obstacleTimer = pygame.time.set_timer(pygame.USEREVENT, self.obstacleSpawnTime)

        self.player = pygame.sprite.Group()
        self.p = Player()
        self.player.add(self.p)

        self.state = self.states.get("TITLE")
        self.score = 0
        self.titleTextYPos = HEIGHT / 2 - 28

        self.numIndices = {"0":0, "1":24, "2":40, "3":64, "4":88, "5":112, "6":136, "7":160, "8":184, "9":208}
    
    def update(self):
        if self.state == self.states.get("TITLE"):
            pygame.mouse.set_visible(True)
            self.totalTime += self.clock.get_time()
            if self.totalTime >= 100:
                self.titleTextYPos += self.p.titleSpeeds[self.p.index][1]
                self.player.update("TITLE")
                self.totalTime = 0

        elif self.state == self.states.get("GAME"):
            pygame.mouse.set_visible(False)
            if self.numObstacles > 0:
                self.totalTime += self.clock.get_time()
            self.obstacles.update()
            self.player.update("GAME")
            self.checkCollisions()
            self.updateScore()
        
        elif self.state == self.states.get("TRANSITION"):
            self.player.update("TRANSITION")

            if self.p.rect.bottom >= HEIGHT:
                self.p.rect.bottom = HEIGHT
                self.playSFX("swoosh.wav")
                self.state = self.states.get("DEATH")
        
        elif self.state == self.states.get("DEATH"):
            pygame.mouse.set_visible(True)
    
    def updateScore(self):
        self.firstPointFrames = (WIDTH - self.p.rect.right) / 5
        self.firstPointTime = (self.firstPointFrames / FPS) * 1000 + 150

        if self.totalTime >= self.firstPointTime:
            self.playSFX("point.wav")
            self.score += 1
            self.totalTime = 0

        if self.totalTime >= self.obstacleSpawnTime and self.score > 0:
            self.playSFX("point.wav")
            self.score += 1
            self.totalTime = 0

    def handlePresses(self, event:int):
        if self.state == self.states.get("TITLE") or self.state == self.states.get("DEATH"):
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                if mousePos[0] >= 575 and mousePos[0] <= 705 and mousePos[1] >= 576 and mousePos[1] <= 624:
                    presses = pygame.mouse.get_pressed()
                    if presses[0] == True:
                        if self.state == self.states.get("TITLE"):
                            self.state = self.states.get("GAME")
                            self.totalTime = 0
                        elif self.state == self.states.get("DEATH"):
                            self.playSFX("swoosh.wav")
                            self.__init__()

        elif self.state == self.states.get("GAME"):
            if event.type == pygame.KEYDOWN:
                self.p.handleKeyPresses(event)

    def drawBG(self):
        self.screen.blit(self.bg, (0,0))

    def draw(self):
        if self.state == self.states.get("TITLE"):
            self.screen.blit(self.titleText, (25, self.titleTextYPos))
            self.loadFile("startbutton.jpg", False, None, None, WIDTH / 2, 600)
        else:
            self.drawScore()
            
        if self.state == self.states.get("DEATH"):
            self.loadFile("gameover.png", False, None, None, WIDTH / 2, HEIGHT / 2)
            self.loadFile("okbutton.jpg", True, 130, 48, WIDTH / 2, 600)

    def determineScoreLocation(self) -> pygame.Vector2:
        totalWidth = 0
        for digit in str(self.score):
            if digit != "1":
                totalWidth += 24
            else:
                totalWidth += 16
        scoreDisplay = pygame.Rect(0, 0, totalWidth, 36)
        scoreDisplay.center = pygame.Vector2(WIDTH / 2, HEIGHT / 4)
        return scoreDisplay.topleft

    def drawScore(self):
        topleft = self.determineScoreLocation()
        for digit in str(self.score):
            if digit != "1":
                img = self.getImage(self.numSpritesheet, self.numIndices[digit], 24, 36)
                self.screen.blit(img, (topleft))
                topleft += pygame.Vector2(24, 0)
            else:
                img = self.getImage(self.numSpritesheet, self.numIndices[digit], 16, 36)
                self.screen.blit(img, (topleft))
                topleft += pygame.Vector2(16, 0)
                    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.USEREVENT and self.state == self.states.get("GAME"):
                    yPos = random.randint(-150, 150)
                    pipe = Obstacles("top", yPos)
                    self.obstacles.add(pipe)
                    self.numObstacles += 1

                    pipe2 = Obstacles("bottom", yPos)
                    self.obstacles.add(pipe2)
                    self.numObstacles += 1
                    
                self.handlePresses(event)
            
            self.screen.fill("black")
            self.update()

            self.drawBG()

            self.obstacles.draw(self.screen)
            self.player.draw(self.screen)
            self.draw()

            pygame.display.update()
            self.clock.tick(FPS)
    
    def checkCollisions(self):
        for bird in self.player:
            obstacleCollision = pygame.sprite.spritecollide(bird, self.obstacles, False)
            if obstacleCollision or bird.rect.top <= 0:
                self.playSFX("hit.wav")
                self.state = self.states.get("TRANSITION")
                self.playSFX("die.wav")
            if bird.rect.bottom >= HEIGHT:
                bird.rect.bottom = HEIGHT
                self.state = self.states.get("DEATH")
    
    def loadFile(self, filename:str, transform:bool, w:int, h:int, x:int, y:int):
        self.image = pygame.image.load(self.accessFile(filename)).convert_alpha()
        if transform:
            self.image = pygame.transform.scale(self.image, (w, h))
        self.imageRect = self.image.get_rect()
        self.imageRect.center = (x, y)
        self.screen.blit(self.image, self.imageRect.topleft)
    
    def playSFX(self, filename:str):
        sound = pygame.mixer.Sound(self.accessAudio(filename))
        sound.play()

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
    def getImage(spritesheet, x, width, height):
        img = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        img.blit(spritesheet, (0, 0), (x, 0, width, height))
        return img

if __name__ == "__main__":
    game = Game()
    game.run()