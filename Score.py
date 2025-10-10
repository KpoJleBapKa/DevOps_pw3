class Score:
    def __init__(self, canvas):
        self.canvas = canvas
        self.score = 0  # Початковий рахунок спійманих яєць
        self.lost = 0  # Початкова кількість пропущених яєць
        self.text = ""  # Перемінна для тексту
        self.show_text()  # Метод для відображення рахунку на полотні
