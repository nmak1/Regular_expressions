import csv
import re
from collections import namedtuple
from pprint import pprint

# Определяем структуру контакта
Contact = namedtuple('Contact', [
    'lastname',
    'firstname',
    'surname',
    'organization',
    'position',
    'phone',
    'email'
])


def format_phone(phone):
    """Приводит телефон к стандартному формату"""
    if not phone:
        return ''

    # Основной шаблон с учетом возможного добавочного номера
    phone_pattern = re.compile(
        r'(?:\+7|8)\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})'
        r'(?:\s*\(?(доб\.?)\s*(\d+)\)?)?'
    )

    match = phone_pattern.search(phone)
    if not match:
        return phone

    # Форматируем основной номер
    formatted = f"+7({match.group(1)}){match.group(2)}-{match.group(3)}-{match.group(4)}"

    # Добавляем добавочный номер если есть
    if match.group(5) and match.group(6):
        formatted += f" доб.{match.group(6)}"

    return formatted


def process_name_parts(name_parts):
    """Обрабатывает части ФИО, возвращает кортеж (lastname, firstname, surname)"""
    parts = ' '.join(name_parts).split()
    # Заполняем недостающие части пустыми строками
    return (*parts[:3], *([''] * (3 - len(parts))))[:3]


def process_contacts(contacts_list):
    if not contacts_list:
        return []

    # Отделяем заголовок
    header = contacts_list[0]
    contacts = contacts_list[1:]

    processed = []
    for contact in contacts:
        # Защита от IndexError для коротких строк
        contact_data = [contact[i] if i < len(contact) else '' for i in range(7)]

        # Обрабатываем ФИО
        lastname, firstname, surname = process_name_parts(contact_data[:3])

        # Форматируем телефон
        phone = format_phone(contact_data[5])

        # Создаем контакт с именованными полями
        processed.append(Contact(
            lastname=lastname,
            firstname=firstname,
            surname=surname,
            organization=contact_data[3],
            position=contact_data[4],
            phone=phone,
            email=contact_data[6]
        ))

    # Объединяем дубликаты
    unique_contacts = {}
    for contact in processed:
        key = (contact.lastname, contact.firstname)
        if key in unique_contacts:
            # Объединяем информацию, сохраняя непустые значения
            existing = unique_contacts[key]
            merged = existing._replace(
                surname=existing.surname or contact.surname,
                organization=existing.organization or contact.organization,
                position=existing.position or contact.position,
                phone=existing.phone or contact.phone,
                email=existing.email or contact.email
            )
            unique_contacts[key] = merged
        else:
            unique_contacts[key] = contact

    return [header] + [list(contact) for contact in unique_contacts.values()]


# Читаем исходные данные
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Обрабатываем контакты
processed_contacts = process_contacts(contacts_list)

# Сохраняем результат
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(processed_contacts)

# Выводим результат для проверки
pprint(processed_contacts)