import random

class Egg:
    def __init__(self, canvas, color, score):
        # Ініціалізація атрибутів класу: полотно для малювання, колір яйця і рахунок
        self.canvas = canvas
        self.color = color
        self.score = score  # Збереження посилання на об'єкт рахунку
        # Створення яйця на полотні як овалу з заданим кольором
        self.id = canvas.create_oval(0, 0, 25, 25, fill=color)
        # Розміщення яйця в випадковій горизонтальній позиції на полотні
        self.canvas.move(self.id, random.randint(10, 490), -10)
        # Визначення випадкової швидкості падіння яйця
        self.y = random.randint(1, 4)

    def draw(self):
        self.canvas.move(self.id, 0, self.y)  # Переміщення яйця вниз на кількість пікселів self.y

        pos = self.canvas.coords(self.id)  # Отримання поточної позиції яйця на полотні
        if pos[3] >= self.canvas.winfo_height():  # Перевірка чи яйце досягло нижньої межі полотна
            self.score.lost_egg()  # Збільшення лічильника пропущених яєць у об'єкті score
            self.canvas.delete(self.id)  # Видалення яйця з полотна
            return 'hit bottom'  # Повернення індикатору, що яйце вдарилося об дно
        return None  # Якщо яйце ще не вдарилося об дно, повернення None
