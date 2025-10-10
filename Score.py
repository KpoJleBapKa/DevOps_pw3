class Score:
    def __init__(self, canvas):
        self.canvas = canvas
        self.score = 0  # Початковий рахунок спійманих яєць
        self.lost = 0  # Початкова кількість пропущених яєць
        self.text = ""  # Перемінна для тексту
        self.show_text()  # Метод для відображення рахунку на полотні
        
    def show_text(self):
        # Метод створює текст на полотні або оновлює його
        if (self.text == ""):
            self.text = self.canvas.create_text(350, 10, text=f"Спіймав: 0 Пропустив: 0", font=('Helvetica', 16))
        else:
            self.canvas.itemconfig(self.text, text=f"Спіймав: {self.score} Пропустив: {self.lost}")
