import tkinter as tk
from tkinter import ttk
import random
import urllib.request
import os


def save_text(li):
    """save_text() - функция, которая получает первые пять введенных символов в виджете entry, сохраняет их в список letters и затем вызывает функцию render_squares()."""
    text = entry.get()[:5]
    tmp = []
    for el in text:
        tmp.append(el)
    if len(tmp) == 5:
        letters.append(tmp)
    entry.delete(0, 5)
    render_squares(letters, li[0], li[1])
# def run(iter, ):
#     while
def init_render(square_container):
    """init_render() - функция, которая очищает квадраты в square_container."""
    for i in range(6):
        for j in range(5):
            # Получаем квадратик с координатами (i, j)
            square = square_container.grid_slaves(row=i, column=j)[0]
            
            # Меняем цвет фона и убираем текст
            square.configure(background='white', text='')


def render_squares(letter, square_container, word):
    """render_squares() - функция, которая принимает список letter, контейнер с квадратами
      square_container и загаданное слово word. Функция изменяет цвет фона квадратов в соответствии с 
      угаданными символами. Если все символы отгаданы, то вызывается функция end()."""
    # получаем все созданные квадратики
    squares = square_container.grid_slaves()
    rows, columns = square_container.grid_size()
    for ll in range(len(letter)):
        row = square_container.grid_slaves(row=ll)
        temp_col = 0
        for i, square in enumerate(row[::-1]):
            if i <= 4:
                lette = letter[ll][i]
                if lette == word[i]:
                    temp_col += 1
                    square.config(background='#00ff00')
                elif lette in word:
                    square.config(background='#e5cf13')
                elif not lette in word:
                    square.config(background='#cccccc')
            if temp_col == 5:
                end(1)


                # устанавливаем букву в текст квадратика
            square.config(text=lette)
                # меняем цвет фона у квадратика
    if len(letter) == 6:
        end(2)

def end(var):
    """end() - функция, которая вызывается при окончании игры. 
    Если пользователь отгадал слово, выводится сообщение "Вы угадали! Начать заново?" с кнопкой "Да". 
    Если пользователь не отгадал слово, выводится сообщение "Слово было: {word}. """
    global letters, word
    letters = []
    popup = tk.Toplevel()
    popup.geometry("200x100")
    if var == 1:
        label = tk.Label(popup, text="You guessed right. Restart?")
        label.pack()
    else: 
        label = tk.Label(popup, text=f"The word was: {word}. Restart?")
        label.pack()
    button = ttk.Button(popup, text="Yes", command=lambda: [init_render(square_container),choose_word(five_letter_words), popup.destroy()])
    button.pack()
    quit_button = ttk.Button(popup, text="Exit", command=quit_game)
    quit_button.pack()
def quit_game():
    root.destroy()
def generate():
    # Создаем 5 рядов по 5 квадратиков
    for i in range(6):
        for j in range(5):
            square = ttk.Label(square_container, text="", font=('Helvetica', 14), background='white', foreground='#333', width=4, anchor="center")
            square.grid(row=i, column=j, padx=5, pady=5)

def choose_word(five_letter_words):
    global word
    word = random.choice(five_letter_words)


if __name__ == "__main__":
    global letters, root, word, five_letter_words
    letters =[]
    words = 0
    # Создаем главное окнo
    root = tk.Tk()
    root.title("Wordle game")

    # Создаем текстовый виджет
    text_widget = tk.Text(root, height=1, width=23)
    text_widget.insert(tk.END, "Enter five-letter word")
    # Размещаем текстовый виджет вверху по центру окна
    text_widget.pack(side="top")
    #если нет файла со словами - скачиваем
    filename = "words.txt"
    if not os.path.exists(filename):
        url = "https://www.mit.edu/~ecprice/wordlist.10000"
        urllib.request.urlretrieve(url, filename)
        # Чтение файла в переменную
    with open(filename) as f:
        words = f.read().splitlines()
    # Отбор слов из базы данных со словами на 5 букв
    five_letter_words = [word.lower() for word in words if len(word) == 5]
    # Задаём первое слово
    word = random.choice(five_letter_words)
    #Данные системы
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry("{}x{}".format(400, 400))
    #Настраиваем стиль для ввода слова
    entry_style = ttk.Style()
    entry_style.configure('EntryStyle.TEntry', font=('Helvetica', 14), background='#fff', foreground='#333', borderwidth=0, relief='flat')
    entry = ttk.Entry(root, style='EntryStyle.TEntry')
    entry.pack(pady=20, padx=10)
    #Настраиваем стиль для кнопки "Enter"
    button_style = ttk.Style()
    button_style.configure('ButtonStyle.TButton', font=('Helvetica', 14), background='#333', foreground='#fff', borderwidth=0)
    #Создаем контейнер для кнопок-квадратов
    square_container = ttk.Frame(root)
    square_container.pack(pady=20)
    #Генерируем квадратики для вывода текста
    generate()

    rows, columns = square_container.grid_size()
    button_style = ttk.Style()
    button_style.configure('ButtonStyle.TButton', foreground='black')
    #Создаем кнопку "Enter" и устанавливаем для нее команду, вызывающую функцию сохранения текста
    button = ttk.Button(root, text="Enter", style='ButtonStyle.TButton', command=lambda: save_text([square_container, word]))
    button.pack(side="top", pady=0, padx=20)
    # Запускаем главный цикл обработки событий
    root.mainloop()

