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
while 1:
    if random.randint(1, 100) == 1:
        eggs.append(Egg(canvas, 'red', score))
    for egg in list(eggs):  # Ітерація по копії списку яєць
        if egg.draw() == 'hit bottom':
            eggs.remove(egg) # Якщо яйце досягло дна - видаляємо
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)


        
tk.update()
time.sleep(1)
