import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = 'books.json'

# Загрузка данных из JSON
def load_books():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Сохранение данных в JSON
def save_books(books):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

# Добавление книги
def add_book():
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    genre = genre_entry.get().strip()
    pages = pages_entry.get().strip()

    if not title or not author or not genre or not pages:
        messagebox.showerror('Ошибка', 'Все поля должны быть заполнены')
        return

    try:
        pages = int(pages)
        if pages <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror('Ошибка', 'Количество страниц должно быть положительным числом')
        return

    book = {'title': title, 'author': author, 'genre': genre, 'pages': pages}
    books.append(book)
    save_books(books)
    update_table(books)
    clear_entries()

# Очистка полей ввода
def clear_entries():
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    pages_entry.delete(0, tk.END)

# Фильтрация по жанру и страницам
def filter_books():
    genre = filter_genre.get().strip()
    try:
        min_pages = int(filter_pages.get().strip()) if filter_pages.get().strip() else 0
    except ValueError:
        messagebox.showerror('Ошибка', 'В поле страниц должно быть число')
        return

    filtered = []
    for book in all_books:
        if genre and book['genre'].lower() != genre.lower():
            continue
        if min_pages and book['pages'] < min_pages:
            continue
        filtered.append(book)
    update_table(filtered)

# Обновление таблицы
def update_table(books_list):
    for i in tree.get_children():
        tree.delete(i)
    for book in books_list:
        tree.insert('', 'end', values=(book['title'], book['author'], book['genre'], book['pages']))

# Инициализация данных
all_books = load_books()

# Создание окна
root = tk.Tk()
root.title('Book Tracker')
root.geometry('700x500')

# Вкладки (Notebook)
notebook = ttk.Notebook(root)
notebook.pack(padx=10, pady=5, fill='both', expand=True)

# Вкладка "Добавить книгу"
add_frame = ttk.Frame(notebook)
notebook.add(add_frame, text='Добавить книгу')

# Поля ввода
tk.Label(add_frame, text='Название:').grid(row=0, column=0, padx=5, pady=5, sticky='e')
tk.Label(add_frame, text='Автор:').grid(row=1, column=0, padx=5, pady=5, sticky='e')
tk.Label(add_frame, text='Жанр:').grid(row=2, column=0, padx=5, pady=5, sticky='e')
tk.Label(add_frame, text='Страниц:').grid(row=3, column=0, padx=5, pady=5, sticky='e')

title_entry = tk.Entry(add_frame, width=40)
author_entry = tk.Entry(add_frame, width=40)
genre_entry = tk.Entry(add_frame, width=40)
pages_entry = tk.Entry(add_frame, width=40)

title_entry.grid(row=0, column=1, padx=5, pady=5)
author_entry.grid(row=1, column=1, padx=5, pady=5)
genre_entry.grid(row=2, column=1, padx=5, pady=5)
pages_entry.grid(row=3, column=1, padx=5, pady=5)

add_btn = tk.Button(add_frame, text='Добавить книгу', command=add_book)
add_btn.grid(row=4, column=0, columnspan=2, pady=15)

# Вкладка "Фильтр"
filter_frame = ttk.Frame(notebook)
notebook.add(filter_frame, text='Фильтр')

tk.Label(filter_frame, text='Жанр:').grid(row=0, column=0, padx=5, pady=5)
tk.Label(filter_frame, text='Страниц >:').grid(row=1, column=0, padx=5, pady=5)

filter_genre = tk.Entry(filter_frame)
filter_pages = tk.Entry(filter_frame)

filter_genre.grid(row=0, column=1, padx=5, pady=5)
filter_pages.grid(row=1, column=1, padx=5, pady=5)

filter_btn = tk.Button(filter_frame, text='Применить фильтр', command=filter_books)
filter_btn.grid(row=2, column=0, columnspan=2, pady=10)

# Вкладка "Список книг"
list_frame = ttk.Frame(notebook)
notebook.add(list_frame, text='Список книг')

tree = ttk.Treeview(list_frame,
                    columns=('title', 'author', 'genre', 'pages'),
                    show='headings')
tree.heading('title', text='Название')
tree.heading('author', text='Автор')
tree.heading('genre', text='Жанр')
tree.heading('pages', text='Страниц')
tree.column('title', width=200)
tree.column('author', width=150)
tree.column('genre', width=120)
tree.column('pages', width=80)
tree.pack(padx=10, pady=10, fill='both', expand=True)

update_table(all_books)
root.mainloop()
