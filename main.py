import pygame
import os
import sys

from Core.objects import Platform, Block, Ball, Background, Game
from Core.constants import *



pygame.init()
size = width, height = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)

pygame.display.set_caption('Arkanoid')
pygame.display.set_icon(pygame.image.load("media\\logo.png"))
game = Game(screen)



def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    """
        Глвная функция, которая запускает проект и основной цикл игры,
        в котором проверяются ивенты(в том числе на то, что закончилась музыка,
        чтобы запустить её заново).
        Также вызывается метод update объекта Game, который отвечает за все
        изменения в игре, в том числе и отрисовка.
    """
    pygame.mixer.music.set_endevent(1)
    while True:
        screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == 1:
                pygame.mixer.music.play()
        game.update()



if __name__ == '__main__':
    start_screen()
