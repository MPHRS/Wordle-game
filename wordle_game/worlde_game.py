import pygame
import sys

# инициализация Pygame
pygame.init()

# создание игрового окна
window = pygame.display.set_mode((800, 600))

# основной игровой цикл
while True:
    for event in pygame.event.get():
        # проверка наличия события "закрыть окно"
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # проверка наличия события "нажатие клавиши"
        elif event.type == pygame.KEYDOWN:
            # получение символа клавиши
            key = pygame.key.name(event.key)

            # обработка введенного символа
            if key.isalpha():
                pass
                # выполните необходимые действия в игре, например, проверьте, соответствует ли символ букве в загаданном слове.
