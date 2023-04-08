import pygame
import sys
import urllib.request
import os


class Game:
    def __init__(self):
        pygame.font.init()
        pygame.init()
        self.flag = [1,1] # [0] - switch pages
        self.ui = UI()
        # получение размеров экрана
        self.clock = pygame.time.Clock()
        # Скачивание базы данных со словами на 5 букв и сохранение в файле
        filename = "words.txt"
        if not os.path.exists(filename):
            url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
            urllib.request.urlretrieve(url, filename)
        # Чтение файла в переменную
        with open(filename) as f:
            words = f.read().splitlines()

        # Отбор слов из базы данных со словами на 5 букв
        self.five_letter_words = [word.lower() for word in words if len(word) == 5]

    def disp_st_pg(self):
        self.ui.start_page()
        pygame.draw.rect(self.ui.screen, (255, 0, 0), self.ui.rect)
        mouse_pos = pygame.mouse.get_pos()
        self.ui.button_exit.draw(self.ui.screen, mouse_pos)
        self.ui.button_start.draw(self.ui.screen, mouse_pos)

    def disp_game_pg(self):
        self.ui.game_page()
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.rect(self.ui.screen, (255, 0, 0), self.ui.rect1)
        self.ui.button__back_to_menu.draw(self.ui.screen, mouse_pos)
        self.ui.input_box.update()
        # self.ui.screen.fill((30, 30, 30))
        self.ui.input_box.draw(self.ui.screen)


    def run(self):
        while True:
            self.clock.tick(60)
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.flag[0] ==1:
                        if self.ui.button_start.rect.collidepoint(event.pos):
                            self.flag[0] = -self.flag[0]
                        elif self.ui.button_exit.rect.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()
                    elif self.flag[0] == -1:
                        if self.ui.button__back_to_menu.rect.collidepoint(event.pos):
                            self.flag[0] = -self.flag[0]
                
            # Отрисовка экрана
            self.ui.screen.fill((120, 255, 175))
            if self.flag[0] == 1:
                self.disp_st_pg()
            elif self.flag[0] == -1:
                self.disp_game_pg()
        
            pygame.display.flip()
class Button:
    def __init__(self, x, y, w, h, color, active_color, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.active_color = active_color
        self.text = text
    def draw(self, screen, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.active_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        if self.text:
            font = pygame.font.Font(None, 20)
            text = font.render(self.text, True, (0, 0, 0))
            text_rect = text.get_rect(center=self.rect.center)
            screen.blit(text, text_rect)

class InputBox:
    def __init__(self, x, y, w, h, font=None, font_size=30):
        pygame.init()
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('lightskyblue3')
        self.text = ''
        self.font = font or pygame.font.Font(None, font_size)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # return text and deactivate
                    entered_text = self.text
                    self.text = ''
                    self.active = False
                    return entered_text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.font.size(self.text)[0]+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        txt_surface = self.font.render(self.text, True, self.color)
        # Resize the box if the text is too long.
        width = max(200, self.font.size(self.text)[0]+10)
        self.rect.w = width
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
        # Blit the text.
        screen.blit(txt_surface, (self.rect.x+5, self.rect.y+5))


class UI:
    def __init__(self):
        self.screen_info = pygame.display.Info()
        self.screen_width = self.screen_info.current_w
        self.screen_height = self.screen_info.current_h
        temp = min(self.screen_height, self.screen_height)
        self.screen = pygame.display.set_mode((temp//2, temp//2))

    def start_page(self):
        """ Here we are drawing all the elements on the start page"""
        # отрисовка прямоугольника на экране
        self.rect = pygame.Rect(250, 250, 100, 100)
        self.button_start = Button(100, 100, 50, 30, (255, 0, 0), (0, 255, 0), 'Click me')
        self.button_exit = Button(0, 0, 50, 30, (255, 0, 0), (0, 255, 0), 'exit')


    def game_page(self):
        self.rect1 = pygame.Rect(180, 200, 100, 100)
        self.button_enter_word = Button(100, 100, 50, 30, (255, 0, 0), (0, 255, 0), 'Enter word')
        self.button__back_to_menu = Button(400, 300, 50, 30, (255, 0, 0), (0, 255, 0), 'Back to menu')
        self.button__restart = Button(100, 100, 50, 30, (255, 0, 0), (0, 255, 0), 'Restart')
        self.input_box = InputBox(100, 100, 140, 32)
        
class Word:
    def __init__(self, word):
        # инициализация слова
        pass
    
    def check_letter(self, letter):
        # проверка, есть ли буква в слове
        pass
    
    def is_guessed(self):
        # проверка, угадано ли слово полностью
        pass    


if __name__ == "__main__":
    game = Game()
    game.run()