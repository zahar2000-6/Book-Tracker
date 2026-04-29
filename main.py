import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("600x500")
        self.quotes = self.load_quotes()  # Загружаем предопределённые цитаты
        self.history = []  # История сгенерированных цитат

        # Инициализация элементов интерфейса
        self.create_widgets()

    def load_quotes(self):
        """Загружает список предопределённых цитат."""
        return [
            {"text": "Жизнь — это то, что люди больше всего стремятся сохранить и меньше всего берегут.", "author": "Жан-Жак Руссо", "topic": "философия"},
            {"text": "Успех — это способность идти от поражения к поражению без потери энтузиазма.", "author": "Уинстон Черчилль", "topic": "мотивация"},
            {"text": "Знание — сила.", "author": "Фрэнсис Бэкон", "topic": "образование"},
            {"text": "Будь верен самому себе.", "author": "Уильям Шекспир", "topic": "саморазвитие"},
            {"text": "В великом есть простота.", "author": "Леонардо да Винчи", "topic": "искусство"}
        ]

    def create_widgets(self):
        """Создаёт все элементы интерфейса."""

        # Заголовок
        ttk.Label(self.root, text="Random Quote Generator", font=("Helvetica", 16)).pack(pady=10)

        # Поле для отображения цитаты
        self.quote_label = ttk.Label(self.root, text="", wraplength=550, font=("Helvetica", 12), justify="center")
        self.quote_label.pack(pady=10)

        # Кнопка генерации цитаты
        ttk.Button(self.root, text="Сгенерировать цитату", command=self.generate_quote).pack(pady=5)

        # Раздел фильтрации
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(pady=10)

        ttk.Label(filter_frame, text="Фильтрация по автору:").grid(row=0, column=0, padx=5, pady=5)
        self.author_filter = ttk.Entry(filter_frame, width=20)
        self.author_filter.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="Фильтрация по теме:").grid(row=0, column=2, padx=5, pady=5)
        self.topic_filter = ttk.Entry(filter_frame, width=20)
        self.topic_filter.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(filter_frame, text="Применить фильтры", command=self.filter_quotes).grid(row=0, column=4, padx=5, pady=5)

        # Список истории цитат
        ttk.Label(self.root, text="История цитат:").pack(pady=5)
        self.history_list = tk.Listbox(self.root, height=10, width=60)
        self.history_list.pack(pady=5)

        # Кнопки сохранения/загрузки
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Сохранить историю", command=self.save_history).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Загрузить историю", command=self.load_history).grid(row=0, column=1, padx=5)

        # Форма добавления новой цитаты
        add_frame = ttk.Frame(self.root)
        add_frame.pack(pady=10)

        ttk.Label(add_frame, text="Добавить новую цитату:").grid(row=0, column=0, columnspan=3)

        ttk.Label(add_frame, text="Текст:").grid(row=1, column=0, padx=5, pady=5)
        self.text_entry = ttk.Entry(add_frame, width=30)
        self.text_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        ttk.Label(add_frame, text="Автор:").grid(row=2, column=0, padx=5, pady=5)
        self.author_entry = ttk.Entry(add_frame, width=30)
        self.author_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        ttk.Label(add_frame, text="Тема:").grid(row=3, column=0, padx=5, pady=5)
        self.topic_entry = ttk.Entry(add_frame, width=30)
        self.topic_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

        ttk.Button(add_frame, text="Добавить", command=self.add_quote).grid(row=4, column=1, padx=5, pady=5)

    def generate_quote(self):
        """Генерирует случайную цитату и добавляет в историю."""
        quote = random.choice(self.quotes)
        self.quote_label.config(text=f"{quote['text']}\n— {quote['author']} ({quote['topic']})")
        self.history.append(quote)
        self.update_history_list()

    def update_history_list(self):
        """Обновляет список истории цитат."""
        self.history_list.delete(0, tk.END)
        for quote in self.history:
            self.history_list.insert(tk.END, f"{quote['text']} ({quote['author']}, {quote['topic']})")

    def filter_quotes(self):
        """Фильтрует историю цитат по автору и теме."""
        author = self.author_filter.get().lower()
        topic = self.topic_filter.get().lower()
        filtered = [
            q for q in self.history
            if (author in q['author'].lower() or not author) and
            (topic in q['topic'].lower() or not topic)
        ]
        self.history_list.delete(0, tk.END)
        for quote in filtered:
            self.history_list.insert(tk.END, f"{quote['text']} ({quote['author']}, {quote['topic']})")

    def save_history(self):
        """Сохраняет историю цитат в файл JSON."""
        try:
            with open('history.json', 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", "История сохранена!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {str(e)}")

    def load_history(self):
        """Загружает историю цитат из файла JSON."""
        try:
            if os.path.exists('history.json'):
                with open('history.json', 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
                self.update_history_list()
                messagebox.showinfo("Успех", "История загружена!")
            else:
                messagebox.showwarning("Предупреждение", "Файл истории не найден.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить историю: {str(e)}")

    def add_quote(self):
        """Добавляет новую цитату в список цитат."""
        text = self.text_entry.get().strip()
        author = self.author_entry.get().strip()
        topic = self.topic_entry.get().strip()

        if not text or not author or not topic:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        new_quote = {"text": text, "author": author, "topic": topic}
        self.quotes.append(new_quote)
        messagebox.showinfo("Успех", "Цитата добавлена!")
        # Очищаем поля ввода
        self.text_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.topic_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()

