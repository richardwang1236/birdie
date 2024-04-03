import os
import random
import sys
import urllib.request
import zipfile

import pygame


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((900, 600))
        pygame.display.set_caption('Bird 按方向键操控')
        self.clock = pygame.time.Clock()
        self.image1 = pygame.image.load('back.jpg')
        self.image2 = pygame.image.load('end.jpg')
        self.bird = Bird()
        self.obs = Obs()
        with open('score.txt', "r") as file:
            self.content = int(file.read())

    def go(self):

        self.score = 0
        pygame.init()
        font = pygame.font.Font(None, 36)
        self.music2 = pygame.mixer.Sound("blast.wav")
        while True:
            self.text_surface = font.render(f"Score:{self.score}", True, (255, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.bird.move('up')
            elif keys[pygame.K_DOWN]:
                self.bird.move('down')

            self.clock.tick(30)

            if Bird.life == 0:
                if self.content <= self.score:
                    self.text_surface2 = font.render(f"Best Score:{self.score}", True, (255, 0, 0))
                    self.screen.blit(self.image2, (0, 0))
                    self.screen.blit(self.text_surface, (380, 400))
                    self.screen.blit(self.text_surface2, (380, 420))
                    with open('score.txt', "w") as file:
                        file.write(f"{self.score}")
                else:

                    self.text_surface2 = font.render(f"Best Score:{self.content}", True, (255, 0, 0))
                    self.screen.blit(self.image2, (0, 0))
                    self.screen.blit(self.text_surface2, (380, 420))
                    self.screen.blit(self.text_surface, (380, 400))


            else:
                self.screen.blit(self.image1, (0, 0))
                self.bird.show(self.screen)
                self.obs.show(self.screen)
                self.obs.move()
                self.screen.blit(self.text_surface, (760, 0))
                self.score += 1
            pygame.display.update()


class Bird(pygame.sprite.Sprite):
    B_group = pygame.sprite.Group()
    life = 3

    def __init__(self):
        super().__init__()
        self.image1 = pygame.image.load('bird1.png')
        self.image2 = pygame.image.load('bird2.png')
        self.image3 = pygame.image.load('bird3.png')
        self.image4 = pygame.image.load('bird3.png')
        self.image5 = pygame.image.load('bird3.png')
        self.rect = self.image1.get_rect()
        self.rect.topleft = (250, 300)
        self.num = 0
        self.sta = False
        self.B_group.add(self)
        self.mask = pygame.mask.from_surface(self.image1)

    def show(self, screen):
        if self.num % 4 == 0:
            self.sta = not self.sta
        if self.sta == True:
            screen.blit(self.image2, self.rect)
            self.num += 1
        if self.sta == False:
            screen.blit(self.image1, self.rect)
            self.num += 1

        if Bird.life == 3:
            screen.blit(self.image3, (0, 0))
            screen.blit(self.image4, (45, 0))
            screen.blit(self.image5, (90, 0))
        if Bird.life == 2:
            screen.blit(self.image3, (0, 0))
            screen.blit(self.image4, (45, 0))
        if Bird.life == 1:
            screen.blit(self.image3, (0, 0))

    def move(self, dir):
        if self.rect.top > 0 and self.rect.top < 520:
            if dir == 'up':
                self.rect = self.rect.move(0, -8)
            if dir == 'down':
                self.rect = self.rect.move(0, 8)
        else:
            if self.rect.top <= 0:
                if dir == 'up':
                    self.rect = self.rect.move(0, 8)
                if dir == 'down':
                    self.rect = self.rect.move(0, 8)
            if self.rect.top >= 520:
                if dir == 'up':
                    self.rect = self.rect.move(0, -8)
                if dir == 'down':
                    self.rect = self.rect.move(0, -8)


class Obs(pygame.sprite.Sprite):
    O_group = pygame.sprite.Group()

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('pipe.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (800, -50)
        self.O_group.add(self)
        self.mask = pygame.mask.from_surface(self.image)

    def show(self, screen):
        screen.blit(self.image, self.rect)

    def move(self):
        if pygame.sprite.spritecollide(self, Bird.B_group, False, pygame.sprite.collide_mask):
            Bird.life -= 1
            channel2 = game.music2.play()
            a = random.randint(-390, -40)
            self.rect.topleft = (800, a)
        if self.rect.left >= 0:
            speed = (game.score) / 150 + 5
            self.rect = self.rect.move(-speed, 0)
        else:
            a = random.randint(-390, -40)
            self.rect.topleft = (800, a)


if __name__ == '__main__':
    if os.path.exists('bird.zip'):
        pass
    else:
        url1 = 'https://2222-1317600699.cos.ap-nanjing.myqcloud.com/bird.zip'
        urllib.request.urlretrieve(url1, 'bird.zip')
        with zipfile.ZipFile('bird.zip', 'r') as zip_ref:
            zip_ref.extractall(os.getcwd())
    game = Game()
    game.go()
