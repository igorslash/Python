from crewai import Task
from agents import architect, developer, tester, documenter
from utils import save_output


def create_tasks():
    # 1. Архитектура
    task1 = Task(
        description="Спроектировать консольное приложение ToDo List на Python. "
                   "Опиши архитектуру, структуру файлов и классов. "
                   "Учти: хранение задач в JSON, CRUD операции, валидацию данных.",
        agent=architect,
        expected_output="Детальное описание архитектуры с модулями, классами и методами",
        output_handler=lambda result: save_output("architect.md", result)
    )

    # 2. Разработка
    task2 = Task(
        description="Реализовать код приложения ToDo List на основе архитектуры из task1. "
                   "Используй ООП подход, добавь обработку ошибок, логирование. "
                   "Реализуй: добавление, удаление, просмотр задач, сохранение в JSON.",
        agent=developer,
        context=[task1],
        expected_output="Полный рабочий код приложения с комментариями",
        output_handler=lambda result: save_output("developer.py", result)
    )

    # 3. Первое тестирование
    task3 = Task(
        description="Написать комплексные pytest-тесты для ToDo List. "
                   "Покрой все основные функции: добавление, удаление, отображение задач. "
                   "Протестируй edge cases и обработку ошибок.",
        agent=tester,
        context=[task2],
        expected_output="Набор pytest-тестов и отчет о найденных багах",
        output_handler=lambda result: save_output("tester.md", result)
    )

    # 4. Исправление багов (будет выполняться только при необходимости)
    task2_fix = Task(
        description="Исправить ошибки в коде ToDo List на основе отчета из task3. "
                   "Убедись, что все тесты проходят, добавь недостающую функциональность.",
        agent=developer,
        context=[task2, task3],
        expected_output="Исправленный код приложения",
        output_handler=lambda result: save_output("developer_fix.py", result)
    )

    # 5. Повторное тестирование
    task3_retest = Task(
        description="Провести повторное тестирование исправленного кода. "
                   "Запусти все тесты, проверь фиксы багов. "
                   "Если остались ошибки - составь детальный отчет.",
        agent=tester,
        context=[task2_fix],
        expected_output="Финальный отчет о тестировании",
        output_handler=lambda result: save_output("tester_retest.md", result)
    )

    # 6. Документация
    task4 = Task(
        description="Создать comprehensive README с инструкцией по запуску приложения, "
                   "установке зависимостей, описанием API и примеров использования.",
        agent=documenter,
        context=[task2_fix, task3_retest],
        expected_output="Полная документация в формате README.md",
        output_handler=lambda result: save_output("README.md", result)
    )

    return [task1, task2, task3, task2_fix, task3_retest, task4]


# Функция для условного выполнения workflow
def get_workflow_with_conditions():
    tasks = create_tasks()
    
    # Здесь можно добавить логику условий выполнения
    # Например, на основе результатов тестирования
    return tasks



