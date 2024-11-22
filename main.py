import json
import uuid
import os

# Путь к файлу для хранения данных
FILE_PATH = 'library.json'

class Book:

    def __init__(self, title, author, year):
        if year < 0:
            raise ValueError("Год не может быть меньше 0")
        self.id = str(uuid.uuid4())  # Генерация уникального id
        self.title = title
        self.author = author
        self.year = year
        self.status = "в наличии"  # Статус книги по умолчанию

    def to_dict(self):
        """Преобразует данные книги в словарь."""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status
        }

    @staticmethod
    def from_dict(data):
        """Создает экзмемпляр книги из словаря."""
        book = Book(data['title'], data['author'], data['year'])
        book.id = data['id']
        book.status = data['status']
        return book

    def __str__(self):
        return f"ID: {self.id}, название: {self.title}, автор: {self.author}, год: {self.year}, статус: {self.status}"

class Library:
    def __init__(self):
        self.books = self.load_books()

    def load_books(self):
        """Загружает книги из JSON файла."""
        if os.path.exists(FILE_PATH):
            try:
                with open(FILE_PATH, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [Book.from_dict(book_data) for book_data in data]
            except (json.JSONDecodeError, IOError) as e:
                print(f"Ошибка при загрузке данных: {e}")
                return []
        else:
            return []

    def save_books(self):
        """Сохраняет книги в JSON файл."""
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump([book.to_dict() for book in self.books], f, ensure_ascii=False, indent=4)

    def add_book(self, title, author, year):
        """Добавляет книгу в библиотеку."""
        book = Book(title, author, year)
        self.books.append(book)
        self.save_books()
        print(f"Книга '{title}' добавлена в библиотеку.")

    def remove_book(self, book_id):
        """Удаляет книги из библиотеки по ID."""
        book_to_remove = None
        for book in self.books:
            if book.id == book_id:
                book_to_remove = book
                break
        if book_to_remove:
            self.books.remove(book_to_remove)
            self.save_books()
            print(f"Книга '{book_to_remove.title}' удалена из библиотеки.")
        else:
            print("Книга с таким ID не найдена.")

    def find_books(self, search_term):
        """Ищет книг(и) по title, author или year."""
        found_books = [book for book in self.books if search_term.lower() in book.title.lower() or
                                               search_term.lower() in book.author.lower() or
                                               search_term.lower() in str(book.year)]
        if found_books:
            for book in found_books:
                print(book)
        else:
            print("Книги не найдены по запросу.")

    def display_books(self):
        """Отображает все книги из библиотеки."""
        if not self.books:
            print("Библиотека пуста.")
        else:
            for book in self.books:
                print(book)

    def change_status(self, book_id, new_status):
        """Изменяет статус книги."""
        if new_status not in ["в наличии", "выдана"]:
            print("Недопустимый статус. Статус должен быть 'в наличии' или 'выдана'.")
            return

        for book in self.books:
            if book.id == book_id:
                book.status = new_status
                self.save_books()
                print(f"Статус книги '{book.title}' изменен на '{new_status}'.")
                return
        print("Книга с таким ID не найдена.")

def print_menu():
    """Выводит в консоль главного меню."""
    print("\nМеню:")
    print("1. Добавить книгу")
    print("2. Удалить книгу")
    print("3. Найти книгу")
    print("4. Показать все книги")
    print("5. Изменить статус книги")
    print("0. Выйти")

def main():
    library = Library()

    while True:
        print_menu()
        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания книги: ")

            # Проверка корректности ввода года
            try:
                year = int(year)
                library.add_book(title, author, year)
            except ValueError:
                print("Неверный формат года. Пожалуйста, введите целое число.")

        elif choice == "2":
            book_id = input("Введите ID книги для удаления: ")
            library.remove_book(book_id)

        elif choice == "3":
            search_term = input("Введите для поиска (название, автор или год): ")
            library.find_books(search_term)

        elif choice == "4":
            library.display_books()

        elif choice == "5":
            book_id = input("Введите ID книги для изменения статуса: ")
            new_status = input("Введите новый статус ('в наличии' или 'выдана'): ")
            library.change_status(book_id, new_status)

        elif choice == "0":
            print("Выход из программы...")
            break

        else:
            print("Некорректный выбор, попробуйте снова.")

if __name__ == "__main__":
    main()