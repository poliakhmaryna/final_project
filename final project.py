from collections import UserDict
from datetime import datetime, timedelta
import pickle
import re
import textwrap # для форматування тексту нотаток, переносу текста 
import json # для збереження нотаток у файл


#Серелізація
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()




#опис класів

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not (len(value) == 10):
            raise ValueError("Phone number must be 10 digits") 
        super().__init__(value)
class Birthday(Field):
    def __init__(self, value):
        try:
            birthday = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        self.value = birthday


#додала класс email та перевірку формата  його введення

class Email(Field):
    def __init__(self, value):
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value):
            raise ValueError("Invalid email format")
        super().__init__(value)


class Address(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Address cannot be empty")
        super().__init__(value)



# обов`язкові поля для створення контакту - name та phone, інше можна додати пізніше. якщо ми хочемо щоб була
# можливість ввести їх відразу треба переробити. напевно треба спитати у ментора яка вимога тут

class Record:
    def __init__(self, name):
        self.name = Name(name)     # обов'язкове поле
        self.phones = []           # список телефонів
        self.email = None          # email можна додати пізніше
        self.address = None        # адреса — теж пізніше
        self.birthday = None       # день народження — за бажанням





    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    

    def add_phone(self, phone):
        self.phones.append(Phone(phone))   
   
    def add_birthday (self, birthday):
        self.birthday= Birthday(birthday)
    
    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break
    def edit_phone(self, old_phone: str, new_phone: str):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
            break

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    def find(self, name):
        return self.data.get(name)
    
    
    
    
    
    def delete (self, name):
        if name in self.data:
            del self.data[name]
    
    # def get_upcoming_birthdays(self):
    #     today = datetime.today().date()
    #     upcoming_birthdays_this_week = []
        
    #     for user in self.data.values():
    #         name = user.name.value
    #         birthday = datetime.strptime(user.name.value, "%d.%m.%Y").date()
    #         birthday_this_year = birthday.replace(year=today.year)

    #         if birthday_this_year < today:
    #             birthday_this_year = birthday_this_year.replace(year=today.year + 1)

    #         delta_days = (birthday_this_year - today).days

    #         if 0 <= delta_days <= 7:
    #             congratulation_date = birthday_this_year

    #             if congratulation_date.weekday() == 5:
    #                 congratulation_date += timedelta(days=2)
    #             elif congratulation_date.weekday() == 6:
    #                 congratulation_date += timedelta(days=1)

    #             upcoming_birthdays_this_week.append({
    #                 "name": name,
    #                 "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
    #             })

    #     return upcoming_birthdays_this_week





#  класс Notes


class NotesName(Field): # клас для назви нотатки
    def __init__(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Назва нотатки має бути непорожнім рядком.")
        super().__init__(value)

class NoteText(Field): # клас для тексту нотатк
    def __init__(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Текст нотатки має бути непорожнім рядком.")
        super().__init__(value)


class TagNotes(Field): # клас для тегів нотаток
    def __init__(self, value):
        if value and not isinstance(value, str):
            raise ValueError("Тег має бути рядком.")
        if value and ',' in value:
            raise ValueError("Можна ввести лише один тег без роздільників.")
        super().__init__(value)

class NoteRecord: # клас для запису нотатки
    def __init__(self, name, text, tag=None):
        self.name = NotesName(name)
        self.text = NoteText(text)
        self.tag = TagNotes(tag) if tag else None

    def __str__(self): # метод для виведення нотатки у зручному форматі
        tag_display = f" [tag: {self.tag.value}]" if self.tag else ""
        return f"📌 Note: {self.name.value}\n{textwrap.fill(self.text.value, width=50)}{tag_display}\n"

    def to_dict(self): # метод для перетворення нотатки у словник для збереження у JSON
        """Повертає словник для JSON-серіалізації."""
        return {
            "name": self.name.value,
            "text": self.text.value,
            "tag": self.tag.value if self.tag else None
        }

    @classmethod # класовий метод для створення об'єкта з словника
    def from_dict(cls, data):
        return cls(data["name"], data["text"], data.get("tag"))


class NotesBook(UserDict): # клас для книги нотаток, що наслідує UserDict
    def add_note(self, record: NoteRecord): # клас для додавання нотатки
        self.data[record.name.value] = record

    def delete_note(self, name): # клас для видалення нотатки
        if name in self.data:
            del self.data[name]
            return True
        return False

    def search_by_name(self, name): # клас для пошуку нотатки за назвою
        return [note for key, note in self.data.items() if name.lower() in key.lower()]

    def search_by_text(self, text): # клас для пошуку нотатки за текстом
        return [note for note in self.data.values() if text.lower() in note.text.value.lower()]

    def search_by_tag(self, tag): # клас для пошуку нотатки за тегом
        return [note for note in self.data.values() if note.tag and tag.lower() == note.tag.value.lower()]

    def get_all_notes(self): # клас для отримання всіх нотаток
        return list(self.data.values())

    def to_list(self): # перетворює нотатки у список словників для збереження у JSON
        return [record.to_dict() for record in self.data.values()]

    def save(self, filename="notes.json"): # Зберігає нотатки у JSON-файл
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.to_list(), f, ensure_ascii=False, indent=2)

    def load(self, filename="notes.json"): # Завантажує нотатки з JSON-файлу
        try:
            with open(filename, "r", encoding="utf-8") as f:
                notes_list = json.load(f)
            for note_data in notes_list:
                record = NoteRecord.from_dict(note_data)
                self.add_note(record)
        except FileNotFoundError:
            pass  # Файл уперше не знайдено — працюємо з порожньою книгою




def input_error_contact(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Будь ласка, введіть ім'я та номер телефону."
        except KeyError:
            return "Вкажіть ім'я користувача."
        except IndexError:
            return "Вкажіть ім'я користувача."
    return inner
def parse_input(user_input):
    cmd, args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args



#вимога про контакти: add_contact - додеє контакт в книгу контактів , сhange_contact - редагує, delete  - видаляє.
#  це обовязкові функції згідно завдання. усі інші були в дз я залишила, та окремо додала функцію 



@input_error_contact
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Для додавання контакту введіть: add [ім'я] [телефон]")
    name = args[0]
    phone = args[1]
    record = book.find(name)
    
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = f"Створено контакт {name}."
    else:
        message = f"Контакт {name} вже існує."

    if phone:
        record.add_phone(phone)
        message += f" Додано номер телефону: {phone}."
    
    return message
@input_error_contact
def change_contact(args, book: AddressBook):
       name, new_phone = args
       record = book.find(name)
       if record:
           record.phones = []  
           record.add_phone(new_phone)
           return "Контакт змінено"
       else:
           return "Ой-йой, контакт не знайдено 😢"
@input_error_contact
def show_phone(name, book: AddressBook):
    if book.find(name):
        return ", ".join([phone.value for phone in book.find(name).phones])
    else:
        return "Ой-йой, контакт не знайдено 😢"
@input_error_contact
def show_all(book: AddressBook):
    result = ""
    for record in book.data.values():  # тут отримуємо всі записи
        phones = ", ".join(phone.value for phone in record.phones)
        result += f"{record.name.value}: {phones}\n"
    return result.strip() 

@input_error_contact
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"День народження додано до контакту {name}."
    else:
        return f"Ой-йой, контакт '{name}'не знайдено 😢"

@input_error_contact
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is on {record.birthday.value.strftime('%d.%m.%Y')}"
    elif record:
        return f"У контакта {name} дата дня народження не збережена."
    else:
        return f"Ой-йой, контакт '{name}'не знайдено 😢"

@input_error_contact
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays this week."

    lines = []
    for day, names in upcoming.items():
        line = f"{day}: {', '.join(names)}"
        lines.append(line)

    return "\n".join(lines)

@input_error_contact
def delete(args, book: AddressBook):
    name = args[0]
    if book.find(name):
        book.delete(name)
        return f"Контакт  '{name}' видалено"
    else:
        return f"Ой-йой, контакт '{name}'не знайдено 😢"

@input_error_contact
def add_email(args, book: AddressBook):
    name, email = args
    record = book.find(name)
    if record:
        record.email = Email(email)
        return f"Email додано до контакту {name}."
    return "Ой-йой, контакт '{name}'не знайдено 😢"

@input_error_contact
def add_address(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Введіть: add-address [ім'я] [адреса]")
    name = args[0]
    address = " ".join(args[1:])
    record = book.find(name)
    if record:
        record.address = Address(address)
        return f"Адресу додано до контакту {name}."
    return f"Ой-йой, контакт '{name}' не знайдено 😢"


def help_contacts():
    return """
Доступні команди:

• hello                – привітання
• add [ім'я] [телефон] – додати контакт
• change [ім'я] [телефон] – змінити номер телефону контакту
• phone [ім'я]          – показати номер телефону контакту
• all                   – показати всі контакти
• add-birthday [ім'я] [дата] – додати день народження
• show-birthday [ім'я]  – показати день народження контакту
• birthdays [кількість днів] – показати дні народження, що наближаються
• add-email [ім'я] [email] – додати email контакту
• add-address [ім'я] [адреса] – додати адресу контакту
• delete [ім'я]         – видалити контакт
• close, exit           – вийти з програми
"""







"""Модуль для управління нотатками. Включає класи для створення, видалення, пошуку та виведення нотаток.
Використовує UserDict для зберігання нотаток та забезпечує зручний інтерфейс для роботи з ними. """


def input_error(func): # декоратор для обробки помилок введення
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Помилка: {str(e)}"
    return wrapper

def parse_input(user_input):
    # 1) Видаляємо пробіли спереду/ззаду
    # 2) Розбиваємо на слова
    cmd, *args = user_input.strip().split()
    # 3) Повертаємо команду у нижньому регістрі та решту слів як аргументи
    return cmd.lower(), args

@input_error
def add_note(args, book: NotesBook): # Функція для додавання нотатки
    name = args[0] 
    text = " ".join(args[1:-1]) if len(args) > 2 else args[1] # якщо тег є, то беремо його як останній аргумент
    tag = args[-1] if len(args) > 2 else None # якщо тег не вказано, то None
    record = NoteRecord(name, text, tag) 
    book.add_note(record)
    return f"Нотатку '{name}' додано."


@input_error
def delete_note(args, book: NotesBook): # Функція для видалення нотатки
    name = args[0] 
    if book.delete_note(name):  
        return f"Нотатку '{name}' видалено." 
    return f"Ой-йой, нотатку '{name}' не знайдено 😢"

@input_error
def edit_name(args, book: NotesBook): # Функція для редагування назви нотатки
    if len(args) < 2:
        raise ValueError("Вкажи стару та нову назву нотатки.\nПриклад: edit_name [стара назва] [нова назва]")

    old_name, new_name = args[0], args[1]

    if old_name not in book.data:
        return f"Ой-йой, нотатку з назвою '{old_name}' не знайдено 😢"

    note = book.data.pop(old_name)
    note.name.value = new_name
    book.data[new_name] = note
    return f"Назву нотатки змінено з '{old_name}' на '{new_name}'."

@input_error
def edit_text(args, book: NotesBook): # Функція для редагування тексту нотатки
    if len(args) < 2:
        raise ValueError("Вкажи назву нотатки та новий текст.\nПриклад: edit_text [назва] [новий текст]")

    name = args[0]
    new_text = " ".join(args[1:])

    if name not in book.data:
        return f"Ой-йой, нотатку '{name}' не знайдено 😢"

    book.data[name].text.value = new_text
    return f"Текст нотатки '{name}' успішно оновлено."

@input_error
def show_notes(book: NotesBook): # Функція для виведення всіх нотаток
    notes = book.get_all_notes()
    if not notes:
        return "Книга нотаток порожня."
    return "\n".join(str(note) for note in notes)


@input_error
def search_note(args, book: NotesBook): # Функція для пошуку нотатки за назвою
    keyword = " ".join(args)
    results = book.search_by_name(keyword)
    return "\n".join(str(note) for note in results) if results else "Ой-йой, шось пішло не так 😅all Нотатки не знайдено."


@input_error
def search_note_text(args, book: NotesBook):  # Функція для пошуку нотатки за текстом
    keyword = " ".join(args)
    results = book.search_by_text(keyword)
    return "\n".join(str(note) for note in results) if results else "Ой-йой, шось пішло не так 😅 Нотатки не знайдено за текстом."


@input_error
def search_tag(args, book: NotesBook): # Функція для пошуку нотатки за тегом - бонусне завдання
    keyword = args[0]
    results = book.search_by_tag(keyword)
    return "\n".join(str(note) for note in results) if results else "Ой-йой, шось пішло не так 😅 Нотатки з таким тегом не знайдено."

@input_error # Функція для сортування тегів нотаток - бонусне завдання
def sort_tags(book: NotesBook):
    notes = book.get_all_notes()
    tags = [note.tag.value for note in notes if note.tag and note.tag.value]

    if not tags:
        return "📦 Упс! Схоже, цей тег десь сховався між рядками коду або випив всю кавусю... Ми його не знайшли 😅"

    sorted_tags = sorted(set(tags), key=str.lower)
    return "📚 Всі теги у нотатках (в алфавітному порядку):\n" + "\n".join(f"• {tag}" for tag in sorted_tags)

def show_help(): # Функція для виведення довідки з доступними командами
    return """
 Доступні команди Notes:

• help                             – показати весь список команд
• add [назва] [текст] [тег]        – додати нову нотатку
• edit_name [стара] [нова назва]   – змінити назву нотатки
• edit_text [назва] [новий текст]  – змінити текст нотатки
• all                              – показати всі нотатки
• delete [назва]                   – видалити нотатку за назвою
• search [частина назви]           – пошук за назвою нотатки
• search_notes [ключове слово]     – пошук за текстом нотатки
• search_tag [тег]                 – пошук за тегом нотатки
• sort_tags                        – показати всі теги, відсортовані за алфавітом
• back                             – повернутися до стартового меню
• exit / close                     – завершити роботу
"""
def main_menu():
    while True:
        print("\n📁 Головне меню")
        print("1. Книга контактів")
        print("2. Блокнот (Notes)")
        print("3. Вихід")

        choice = input("👉 Вибери опцію (1/2/3): ")

        if choice == "1":
            main_contacts()
        elif choice == "2":
            main_notes()
        elif choice == "3":
            print("👋 До побачення!")
            break
        else:
            print("⛔ Невірний вибір. Спробуй ще раз.")

def main_contacts():
    book = load_data()
    print("📖 Книга контактів – готова до роботи!")
    print("💡 Для перегляду всього переліку команд введіть: help_contacts")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("👋 Дякуємо за використання книги контактів! До нових зустрічей! 🐍")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "help_contacts":
            print(help_contacts())




        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print (show_phone(args[0], book))

        elif command == "all":
            print (show_all (book))

        elif command == "add-birthday":
            print (add_birthday (args, book))

        elif command == "show-birthday":
            print (show_birthday (args, book))

        elif command == "birthdays":
            print (birthdays (args, book))

        elif command == "add-email":
            print(add_email(args, book))

        elif command == "add-address":
            print(add_address(args, book))    
        
        elif command == "delete":
            print ( delete (args, book))    

        else:
            print("Invalid command.")


def main_notes(): # Головна функція для запуску програми
    notes = NotesBook() 
    notes.load() # Завантажуємо нотатки з файлу при запуску
    print("👋 Вітаємо в блокноті Notes 🐍 від Snaky sisters!")
    print("💡 Для перегляду всього переліку команд введіть: help")

    while True:
        user_input = input("--> ")

        command, args = parse_input(user_input)

        match command: # Використовуємо match-case для обробки команд
            case "add":
                print(add_note(args, notes))
                book.save() # Зберігаємо нотатки після додавання
            case "delete":
                print(delete_note(args, notes))
                book.save() # Зберігаємо нотатки після видалення
        
            case "edit_name": # Редагування назви нотатки
                print(edit_name(args, notes))
                book.save()

            case "edit_text": # Редагування тексту нотатки
                print(edit_text(args, notes))
                book.save()

            case "search": # Пошук нотатки за частиною назви
                print(search_note(args, notes))

            case "search_notes": # Пошук нотатки за текстом
                print(search_note_text(args, notes))

            case "search_tag":  # Пошук нотатки за тегом - бонусне завдання
                print(search_tag(args, notes))

            case "sort_tags": # Сортування тегів нотаток - бонусне завдання
                print(sort_tags(notes))

            case "all": # Показати всі нотатки
                print(show_notes(notes))

            case "back": # Повернення до стартового меню (додати таку саме команду в get_birthdays.py та контакти)
                print("I'll be back ↩ Але поки повертаємося в стартове меню.")
                break

            case "exit" | "close": # Завершення роботи програми
                print("👋 Дякуємо за використання блокноту Notes! До нових зустрічей! 🐍")
                break
            case "help": # Виведення довідки з усіма доступними командами
                print( show_help())

            case _: # заглушка для невідомих (помилкових) команд
                print("😳 Команда не розпізнана. Можливо, ти винайшла(-ов) нову функцію? Введи help для списку доступного 😅")
        
if __name__ == "__main__":

    main_menu()      
