import random
import time
from tkinter import *
from Catcher import Catcher
from Score import Score
from Egg import Egg

tk = Tk()
tk.title("Гра: Ловець!")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)

canvas = Canvas(tk, width=500, height=400,
                bd=0, highlightthickness=0)
canvas.pack()

score = Score(canvas)
catcher = Catcher(canvas, 'blue', score)
eggs = []
while 1:  # Початок безкінечного циклу для ігрового процесу
    if random.randint(1, 100) == 1:  # Випадкова перевірка (1% шанс)
        eggs.append(Egg(canvas, 'red', score))  # Створення нового яйця та додавання до списку
    tk.update_idletasks()  # Оновлення ігрового інтерфейсу без блокування інших завдань
    tk.update()  # Повне оновлення всього ігрового вікна
    time.sleep(0.01)  # Коротка пауза

tk.update()
time.sleep(1)
