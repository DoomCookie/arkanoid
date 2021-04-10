import pygame
import random

from Core.constants import WIDTH, HEIGHT, FPS

import os
import sys


class Game:
    """
        Класс игры, который реализует всю логику игры и все игровые объекты.
        Также содержит метод, который отрисовывает и обновляет все объекты.
    """
    def __init__(self, screen):
        self.game = False
        self.sc = screen
        self.sound_play_lose = False
        self.sound_lose = pygame.mixer.Sound('media\\lose.wav')
        self.musics = ['media\\Monkeys Spinning Monkeys.mp3', "media\\Jaunty Gumption.mp3"]
        pygame.mixer.music.load(random.choice(self.musics))
        pygame.mixer.music.play()
        self.clock = pygame.time.Clock()
        self.platform_sprites = pygame.sprite.Group()
        self.win = False
        self.all_sprites = pygame.sprite.Group()
        self.ball_sprite = pygame.sprite.Group()
        self.background = Background(0,0, self.all_sprites)
        self.platform = Platform(WIDTH // 2,  HEIGHT - 40, self.platform_sprites)
        self.init_lvl()
        self.ball = Ball(WIDTH // 2, HEIGHT - self.platform.rect.height - 20,
                        self.all_sprites, self.platform, self.blocks_sprite)
        self.score = 0


    def draw(self):
        """
            Метод, который отрисовывает все спрайты и тексты на экране
        """
        self.all_sprites.draw(self.sc)
        self.all_sprites.update()
        self.blocks_sprite.draw(self.sc)
        self.blocks_sprite.update()
        self.platform_sprites.draw(self.sc)
        self.platform_sprites.update()
        self.ball_sprite.draw(self.sc)
        self.ball_sprite.update()
        self.clock.tick(FPS)

        f1 = pygame.font.Font(None, 36)
        self.score = (self.total - len(self.blocks)) * 100
        text1 = f1.render(str(self.score), True,
                      'white')
        self.sc.blit(text1, (0, 0))
        if not self.ball.lose and not self.win and not self.game:
            self.print_beg()
        if self.ball.lose:
            self.print_end(text = f"Вы проиграли. Ваш счёт: {self.score}")

        pygame.display.flip()


    def update(self):
        """
            Метод, который вычисляет логику каждое обновление экарана.
            Отлаливает нажатие на пробел для запуска, на enter для перезапуска.
            Проверяет положение мяча для отслеживания поражения.
            Отлавливает нажатие стрелок для управления платформой.
        """
        self.draw()
        self.check_win()

        if pygame.key.get_pressed()[pygame.K_SPACE] and not self.ball.lose and not self.win:
            self.ball.move = True
            self.game = True
        if pygame.key.get_pressed()[pygame.K_RETURN] and (self.ball.lose or self.win):
            self.restart()
        self.check_blocks()

        if self.ball.rect.y > self.platform.rect.y:
            if not self.sound_play_lose:
                self.sound_play_lose = True
                self.sound_lose.play()
            self.ball.lose = True
            self.ball.move = False
            self.game = False

        if not self.ball.lose and not self.win:
            if pygame.key.get_pressed()[pygame.K_LEFT] and self.platform.rect.x > 0:
                self.platform.rect = self.platform.rect.move(-10, 0)
                if not self.game:
                    self.ball.rect = self.ball.rect.move(-10, 0)
            if pygame.key.get_pressed()[pygame.K_RIGHT] and self.platform.rect.x < WIDTH - self.platform.rect.width:
                self.platform.rect = self.platform.rect.move(10, 0)
                if not self.game:
                    self.ball.rect = self.ball.rect.move(10, 0)


    def init_lvl(self):
        """
            Метод, который создаёт поле,основываясь на матрице-шаблоне.
        """
        #field = [[random.choice(["#", "."]) for i in range(8)] for j in range(8)]
        field = [
            ["#", "#", "#", "#", "#", "#", "#", "#"],
            ["#", "#", "#", "#", "#", "#", "#", "#"],
            ["#", "#", "#", "#", "#", "#", "#", "#"],
            ["#", "#", "#", "#", "#", "#", "#", "#"],
            ["#", "#", "#", "#", "#", "#", "#", "#"],
            ["#", "#", "#", "#", "#", "#", "#", "#"],
            ["#", "#", "#", "#", "#", "#", "#", "#"],
            ["#", "#", "#", "#", "#", "#", "#", "#"]
        ]
        # field = [
        #     ["#", "#", "#", "#", "#", "#", "#", "#"],
        #     [".", "#", "#", "#", "#", "#", "#", "."],
        #     [".", ".", "#", "#", "#", "#", ".", "."],
        #     [".", ".", ".", "#", "#", ".", ".", "."],
        #     [".", ".", ".", ".", ".", ".", ".", "."],
        #     [".", ".", ".", ".", ".", ".", ".", "."],
        #     [".", ".", ".", ".", ".", ".", ".", "."],
        #     [".", ".", ".", ".", ".", ".", ".", "."]
        # ]
        # field = [
        #     [".", ".", ".", ".", ".", ".", ".", "."],
        #     [".", ".", ".", ".", ".", ".", ".", "."],
        #     [".", ".", ".", ".", ".", ".", ".", "."],
        #     [".", ".", ".", ".", ".", ".", ".", "."],
        #     [".", ".", ".", ".", ".", ".", ".", "."],
        #     [".", ".", ".", ".", ".", ".", ".", "."],
        #     [".", ".", ".", ".", ".", ".", ".", "."],
        #     [".", ".", ".", ".", "#", ".", ".", "."]
        # ]
        self.total = sum((sum(1 for x in row if x == "#") for row in field))
        self.blocks_sprite = pygame.sprite.Group()
        left = (WIDTH - (94 * 8)) // 2
        top = 50
        self.blocks = []
        for i in range(8):
            for j in range(8):
                if field[i][j] == "#":
                    block = Block(left + (j * 94) , top + (i * 31), self.blocks_sprite)
                    self.blocks.append(block)


    def check_win(self):
        """
            Метод, который проверяет победу.
            Игрок победил когда список блоков будет пуст, то есть все блоки будут уничтожены.
        """
        if len(self.blocks) == 0:
            self. win = True
            self.game = False
            self.ball.move = False
            text = f"Вы выиграли. Ваш счёт: {self.score}"
            self.print_end(text)


    def print_beg(self):
        """
            Метод, который отрисовывает подсказку в начале игры.
        """
        f1 = pygame.font.Font(None, 36)
        text1 = f1.render('Для начала нажмите Пробел', True,
                      'green')
        rect1 = text1.get_rect()
        x1 = (WIDTH - rect1.width) // 2
        y1 = (HEIGHT - rect1.height) // 2
        self.sc.blit(text1, (x1, y1))


    def print_end(self, text):
        """
            Метод, который отрисовывает подсказку в конце игры.
            При поражении или победе.
        """
        f1 = pygame.font.Font(None, 36)
        text1 = f1.render(text, True,
                      'red')
        text2 = f1.render("Для продолжения нажмите ENTER", True,
                      'red')
        rect1 = text1.get_rect()
        rect2 = text2.get_rect()
        x1 = (WIDTH - rect1.width) // 2
        y1 = (HEIGHT - rect1.height) // 2
        x2 = (WIDTH - rect2.width) // 2
        y2 = y1 + rect1.height + 10
        self.sc.blit(text1, (x1, y1))
        self.sc.blit(text2, (x2, y2))


    def restart(self):
        """
            Метод для перезапуска игры, который переставляет все переключатели
            в начальное положение.
            Удаляет оставщиеся блоки, после чего заново создаёт поле.
            переносит платформу и шар в начальное положение
        """
        self.sound_play_lose = False
        self.ball.lose = False
        self.win = False
        self.ball.move = False
        self.platform.lose = False
        self.score = 0

        self.blocks_sprite = pygame.sprite.Group()
        for block in self.blocks[:]:
            block.kill()
        self.init_lvl()

        self.ball.blocks = self.blocks_sprite
        WIDTH // 2, HEIGHT - self.platform.rect.height - 20
        x = (WIDTH // 2) - (self.ball.rect.width // 2)
        y = (HEIGHT - self.platform.rect.height - 20) - self.ball.rect.height
        self.ball.rect.x = x
        self.ball.rect.y = y
        self.ball.dx = random.choice([-5,5])
        self.ball.dy = -5
        self.platform.rect.x = WIDTH // 2 - (self.platform.rect.width // 2)
        self.platform.rect.y = HEIGHT - 40



    def check_blocks(self):
        """
            Метод, который проверяет был ли блок уже уничтожен игроком.
            Если да, то удаляем его из списка блоков.
        """
        for block in self.blocks[:]:
            if block.death:
                self.blocks.remove(block)


class Platform(pygame.sprite.Sprite):
    """
        Объект платформы
    """
    def __init__(self, x, y, group):
        """
            инициализация объекта, загрузка спрайта и перемещение его в нужное положение.
        """
        super().__init__(group)
        self.frames = []
        self.cut_sheet(load_image("platform.png"), 1, 3)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(x - (self.rect.width // 2), y)
        self.count = 0


    def cut_sheet(self, sheet, columns, rows):
        """
            Метод для разделения картинки с несколькими спрайтами,
            взятый из учебника.
        """
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))


    def update(self):
        """
            Метод обновления платформы, в котором реализовано смены анимации платформы.
        """
        self.count += 1
        if self.count % 5 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]



class Block(pygame.sprite.Sprite):
    """
        Класс блока.
    """
    def __init__(self, x, y, group):
        """
            инициализация объекта, загрузка спрайтов и звука.
            Установка его здоровья и помещение в указанное место.
        """
        super().__init__(group)
        self.sound_point = pygame.mixer.Sound('media\\point.wav')
        self.frames = []
        i = random.randint(0, 9)
        self.cut_sheet(load_image(f"block{i}.png"), 2, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.count = 0
        self.total_hp = 2
        self.hp = 2
        self.death = False


    def cut_sheet(self, sheet, columns, rows):
        """
            Метод для разделения картинки с несколькими спрайтами,
            взятый из учебника.
        """
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))


    def touch(self):
        """
            Метод, который вызывается в случае касания мячом блока.
            Уменьшает его здоровье, меняет спрайт если здоровья меньше половины.
            Если здоровья ноль, то воспроизводится звук повышения очков,
            а сам блок удаляется.
        """
        self.hp -= 1;
        if self.hp <= self.total_hp // 2:
            self.image = self.frames[1]
        if self.hp == 0:
            self.sound_point.play()
            self.death = True
            self.kill()


class Ball(pygame.sprite.Sprite):
    """
        Класс мяча.
    """
    def __init__(self, x, y, group, platform, blocks):
        """
            инициализация объекта, загрузка спрайта и звука.
            Установка его начальных состояний и помещение в указанное место.
        """
        super().__init__(group)
        self.sound_block = pygame.mixer.Sound('media\\hit.wav')
        self.image = load_image("ball.png")
        self.move = False
        self.blocks = blocks
        self.rect = self.image.get_rect()
        self.platform = platform
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(x - (self.rect.width // 2), y - self.rect.height)
        self.dx, self.dy = 5, -5
        self.delay = 0
        self.lose = False

    def update(self, *args):
        """
            Метод обновления. Двигает мяч, если он должен двигаться self.move.
            Меняет направление в случае ударения о стенки, блоки, платформу.
            Ударение о стенки вычисляется по координатам, о платформе по маске,
            о блоки по колайдеру rect. Воспроизводит необходимы звуки.
        """
        if self.delay != 0:
            self.delay -= 1
        if self.move:
            self.rect = self.rect.move(self.dx, self.dy)
        if self.rect.x < 0 or self.rect.x > WIDTH - self.rect.width:
            self.dx = -self.dx
            self.sound_block.play()
        if self.rect.y < 0 or self.rect.y > HEIGHT - self.rect.height:
            self.dy = -self.dy
            self.sound_block.play()
        if pygame.sprite.collide_mask(self, self.platform) and self.delay == 0:
            self.dy = -self.dy
            self.delay = 60
            self.sound_block.play()
        if pygame.sprite.spritecollideany(self, self.blocks):
            block = pygame.sprite.spritecollideany(self, self.blocks)
            block.touch()
            self.dy = -self.dy
            self.sound_block.play()


class Background(pygame.sprite.Sprite):
    """
        Объект фона для отрисовки фона.
    """
    def __init__(self, x, y, group):
        """
            Загрузка фона, растягивание в размер окна, установка его в необходимы координаты.
        """
        super().__init__(group)
        self.image = load_image("background.jpg")
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)



def load_image(name, colorkey=None):
    """
        функция загрузки изображения из учебника.
    """
    fullname = os.path.join('media', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
