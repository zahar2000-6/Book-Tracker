import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.books = []
        self.setup_ui()  # Сначала создаём UI
        self.load_data()  # Затем загружаем данные

    def setup_ui(self):
        # Поля ввода
        tk.Label(self.root, text="Название книги:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.title_entry = tk.Entry(self.root, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Автор:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.author_entry = tk.Entry(self.root, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Жанр:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.genre_entry = tk.Entry(self.root, width=30)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Количество страниц:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.pages_entry = tk.Entry(self.root, width=30)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        tk.Button(self.root, text="Добавить книгу", command=self.add_book).grid(row=4, column=0, columnspan=2, pady=10)

        # Фильтрация
        tk.Label(self.root, text="Фильтр по жанру:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.filter_genre = tk.Entry(self.root, width=30)
        self.filter_genre.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Фильтр страниц (>):").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.filter_pages = tk.Entry(self.root, width=30)
        self.filter_pages.grid(row=6, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Применить фильтры", command=self.apply_filters).grid(row=7, column=0, columnspan=2, pady=5)

        # Таблица
        columns = ("Название", "Автор", "Жанр", "Страниц")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

        # Кнопки сохранения/загрузки
        tk.Button(self.root, text="Сохранить в JSON", command=self.save_data).grid(row=9, column=0, pady=5)
        tk.Button(self.root, text="Загрузить из JSON", command=self.load_data).grid(row=9, column=1, pady=5)

    def validate_input(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()

        if not title or not author or not genre:
            messagebox.showerror("Ошибка", "Все текстовые поля должны быть заполнены!")
            return False, None, None, None, None

        try:
            pages_num = int(pages)
            if pages_num <= 0:
                messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом!")
                return False, None, None, None, None
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return False, None, None, None, None

        return True, title, author, genre, pages_num

    def add_book(self):
        is_valid, title, author, genre, pages = self.validate_input()
        if not is_valid:
            return

        book = {"title": title, "author": author, "genre": genre, "pages": pages}
        self.books.append(book)
        self.update_table()
        self.clear_entries()

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)

    def update_table(self, books=None):
        if hasattr(self, 'tree') and self.tree is not None:
            for item in self.tree.get_children():
                self.tree.delete(item)
            display_books = books if books is not None else self.books
            for book in display_books:
                self.tree.insert("", "end", values=(book["title"], book["author"], book["genre"], book["pages"]))

    def apply_filters(self):
        filtered_books = self.books
        genre_filter = self.filter_genre.get().strip().lower()
        pages_filter = self.filter_pages.get().strip()

        if genre_filter:
            filtered_books = [b for b in filtered_books if genre_filter in b["genre"].lower()]

        if pages_filter:
            try:
                min_pages = int(pages_filter)
                filtered_books = [b for b in filtered_books if b["pages"] >= min_pages
            except ValueError:
                messagebox.showwarning("Предупреждение", "Некорректное значение для фильтра страниц!")

        self.update_table(filtered_books)

    def save_data(self):
        try:
            with open("books.json", "w", encoding="utf-8") as f:
                json.dump(self.books, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", "Данные сохранены в books.json")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {str(e)}")

    def load_data(self):
        try:
            if os.path.exists("books.json"):
                with open("books.json", "r", encoding="utf-8") as f:
                    self.books = json.load(f)
                self.update_table()
                messagebox.showinfo("Успех", "Данные загружены из books.json")
            else:
                messagebox.showinfo("Информация", "Файл books.json не найден. Создан новый список.")
        except json.JSONDecodeError:
            messagebox.showerror("Ошибка", "Файл books.json повреждён. Создайте новый список книг.")
            self.books = []
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()
