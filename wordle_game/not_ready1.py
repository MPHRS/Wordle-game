import pygame
import sys
import urllib.request
import os
import tkinter as tk

class Game:
    def __init__(self):
        pygame.font.init()
        pygame.init()
        self.flag = [1,1] # [0] - switch pages
        self.ui = UI()
        self.ui.start_page()
        self.ui.game_page()
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
                elif self.ui.input_box.rect.collidepoint(pygame.mouse.get_pos()) and self.flag[0] == -1:
                    self.ui.input_box.handle_event(event)
                    
                
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


class InputBox(tk.Frame):
    def __init__(self, master=None, label=None, entry_width=None, entry_var=None):
        super().__init__(master)
        self.label = label
        self.entry_width = entry_width
        self.entry_var = entry_var

        self.create_widgets()

    def create_widgets(self):
        if self.label:
            self.label_widget = tk.Label(self, text=self.label)
            self.label_widget.pack(side='left')

        if self.entry_var:
            self.entry_widget = tk.Entry(self, width=self.entry_width, textvariable=self.entry_var)
        else:
            self.entry_widget = tk.Entry(self, width=self.entry_width)

        self.entry_widget.pack(side='left')

    def get_text(self):
        return self.entry_widget.get()


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
        root = tk.Tk()
        input_var = tk.StringVar()
        self.input_box = InputBox(root, label="Enter text:", entry_width=20, entry_var=input_var)
        self.input_box.pack()

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
    
    

    button = tk.Button(root, text="Get text", command=lambda: print(input_box.get_text()))
    button.pack()

    root.mainloop()