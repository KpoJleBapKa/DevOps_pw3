from tkinter import *
import random
import time

tk = Tk() # Створює нове вікно Tkinter
tk.title("Гра: Ловець!")
tk.resizable(0, 0) # Вимикає можливість зміни розміру вікна користувачем.
# Робить вікно завжди знаходиться на верху інших вікон.
tk.wm_attributes("-topmost", 1)

# Створення полотна для малювання гри:
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
