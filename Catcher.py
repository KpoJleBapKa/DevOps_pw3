class Catcher:
    def __init__(self, canvas, color, score):
        # Ініціалізація атрибутів класу: полотно для малювання, рахунок і вигляд ловця
        self.canvas = canvas
        self.score = score  # Збереження посилання на об'єкт рахунку
        # Створення прямокутника (ловця) на полотні з визначеним кольором
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        # Переміщення ловця на початкову позицію (приблизно центр нижньої частини полотна)
        self.canvas.move(self.id, 200, 350)
        self.x = 0  # Початкова горизонтальна швидкість ловця (0 означає статичний)
        # Збереження ширини полотна для подальшого використання при обмеженні руху ловця
        self.canvas_width = self.canvas.winfo_width()
        # (подальші методи для руху ловця і збирання об'єктів мають бути визначені)
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)

    def turn_left(self, evt):
        # Якщо ловець не на краю зліва, встановлюємо швидкість для руху вліво
        if self.canvas.coords(self.id)[0] > 0:
            self.x = -20

    def turn_right(self, evt):
        # Якщо ловець не на краю справа, встановлюємо швидкість для руху вправо
        if self.canvas.coords(self.id)[2] >= self.canvas_width:
            self.x = 20


