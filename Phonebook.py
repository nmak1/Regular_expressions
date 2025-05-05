import csv
import re
from pprint import pprint


def process_contacts(contacts_list):
    # Шаг 1: Обработка ФИО
    processed_contacts = []
    for contact in contacts_list:
        # Берем первые 3 элемента (ФИО)
        name_parts = ' '.join(contact[:3]).split()
        # Заполняем ФИО, дополняя пустыми строками если частей меньше 3
        lastname = name_parts[0] if len(name_parts) > 0 else ''
        firstname = name_parts[1] if len(name_parts) > 1 else ''
        surname = name_parts[2] if len(name_parts) > 2 else ''

        # Остальные поля
        organization = contact[3]
        position = contact[4]
        phone = contact[5]
        email = contact[6]

        # Шаг 2: Форматирование телефона
        if phone:
            phone = re.sub(
                r'(\+7|8)\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})',
                r'+7(\2)\3-\4-\5',
                phone
            )
            # Обработка добавочного номера
            phone = re.sub(r'доб\.?\s*(\d+)', r'доб.\1', phone)

        processed_contacts.append([
            lastname, firstname, surname,
            organization, position, phone, email
        ])

    # Шаг 3: Объединение дубликатов
    unique_contacts = {}
    for contact in processed_contacts:
        key = (contact[0], contact[1])  # Ключ - фамилия и имя
        if key in unique_contacts:
            # Объединяем информацию
            existing_contact = unique_contacts[key]
            for i in range(2, 7):
                if not existing_contact[i] and contact[i]:
                    existing_contact[i] = contact[i]
        else:
            unique_contacts[key] = contact.copy()

    return list(unique_contacts.values())


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