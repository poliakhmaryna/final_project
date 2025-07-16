"""Модуль notes.py для управління нотатками.
Містить класи NotesName, NoteText, TagNotes, NoteRecord та NotesBook для роботи з нотатками.
Також містить функції для додавання, видалення, редагування та пошуку нотаток.
"""
from collections import UserDict
import textwrap # для форматування тексту нотаток, переносу текста 
import json # для збереження нотаток у файл

class Field: #базовий клас для полів нотатки
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


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