#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
import jsonschema


# Создаёт словарь "студент" и возвращает его
def get_student():

    # Переменная для студента с оценкой хуже 4
    student_bad = False

    # Все оценки
    evaluations = []

    # Средняя оценка
    average_estimation = 0

    # Запросить данные о студенте.
    name = input("Фамилия и инициалы: ")
    group = int(input("Номер группы: "))

    # Ввод 5-ти оценок
    print("Введите 5 оценок через Enter:")
    for i in range(5):
        estimation = int(input())
        evaluations.append(estimation)

    # Проходит по оценкам
    for i, x in enumerate(evaluations):
        # Если оценки только 4 и 5, то он считается хорошим
        if evaluations[i] == 4 or evaluations[i] == 5:
            average_estimation += evaluations[i]
        else:
            # Иначе плохим
            student_bad = True
            break

    # Только хороший студент заносится в список
    if not student_bad:

        # Вычисляется средняя оценка
        average_estimation /= 5

        # Создать словарь.
        return {
            'name': name,
            'group': group,
            'average_estimation': average_estimation,
            # 'evaluations': evaluations,
        }
    else:
        return 0


# Выводит список студентов
def show_list(staff):

    if staff:

        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 8
        )

        print(line)

        print(
            '| {:^4} | {:^30} | {:^20} | {:^8} |'.format(
                "No",
                "Ф.И.О.",
                "Группа",
                "Средняя оценка"
            )
        )

        print(line)

        # Вывести данные о всех студентах.
        for idx, student in enumerate(staff, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>8} |'.format(
                    idx,
                    student.get('name', ''),
                    student.get('group', ''),
                    student.get('average_estimation', 0)
                )
            )

        print(line)

    else:
        print("Список пуст")


# Выводит справку о работе с программой
def show_help():

    print("Список команд:\n")
    print("add - добавить студента;")
    print("list - вывести список студентов;")
    print("help - отобразить справку;")
    print("exit - завершить работу с программой.")


# Сохраняет данные в файл
def save_students(file_name, staff):
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(staff, fout, ensure_ascii=False, indent=3)


# Читает данные из файла
def load_students(file_name):
    with open(file_name, "r", encoding="utf-8") as fin:
        file = json.load(fin)
        validate(file)
        return file


def validate(file):
    with open("schema.json") as f:
        schema = json.load(f)

    validator = jsonschema.Draft7Validator(schema)
    try:
        if not validator.validate(file):
            print("Валидация прошла успешно!")
    except jsonschema.exceptions.ValidationError:
        print("Ошибка валидации!")


if __name__ == '__main__':
    """
    Главная функция
    """

    # Список студентов.
    students = []

    # Организовать бесконечный цикл запроса команд.
    while True:

        # Запросить команду из терминала.
        command = input(">>> ").lower()

        # Выполнить действие в соответствие с командой.
        if command == 'exit':
            break

        # Студент адд #################################
        if command == 'add':

            student = get_student()
            # Если возвращает 0 (условия записи студента не соблюдены)
            if student == 0:
                continue

            # Добавить словарь в список.
            students.append(student)

            # Отсортировать список в случае необходимости.
            if len(students) > 1:
                students.sort(key=lambda item: item['average_estimation'],
                              reverse=True)

        # Лист #######################################
        elif command == 'list':
            show_list(students)

        elif command == 'help':
            show_help()

        elif command.startswith("save "):
            command = command.split()
            file_name = command[1]
            save_students(file_name, students)

        elif command.startswith("load "):
            command = command.split()
            file_name = command[1]
            students = load_students(file_name)

        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)
