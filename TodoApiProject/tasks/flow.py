from crewai import Task

from agents import architect, developer, tester, documenter
from utils import save_output


def create_task(architect, developer, tester, documenter, task2_fix):
    task1 = Task(description= "Спроектировать консольное приложение ToDo List на Python. "
                    "Опиши архитектуру, структуру файлов и классов.",
                 agent= architect,
    output_handler = lambda result: save_output("architect.md", result)
                 )


    task2 = Task(
        description="Реализовать код приложения ToDo List на основе архитектуры.",
        agent=developer,
        context=[task1],
        output_handler = lambda result: save_output("developer.py", result)
    )

    task3 = Task(
        description="Написать pytest-тесты для ToDo List. "
                    "Если найдены ошибки, вернуть баг-репорт.",
        agent=tester,
        context=[task2, task2_fix, ],
        output_handler=lambda result: save_output("tester.md", result)

    )

    task2_fix = Task(
        description="Исправить ошибки в коде ToDo List.",
        agent=developer,
        context=[task2],
        output_handler=lambda result: save_output("developer_fix.py", result)
    )

    task3_retest = Task(
        description="Написать pytest-тесты для ToDo List. ",
        output_handler = lambda result: save_output("tester_retest.md", result)
    )

    task4 = Task(
        description="Создать README с инструкцией по запуску приложения.",
        agent=documenter,
        context=[task2_fix, task3_retest, task3_retest],
        output_handler=lambda result: save_output("README.md", result)
    )

    return [task1, task2, task3, task2_fix, task3_retest, task4]


def create_tasks():
    return create_task(architect, developer, tester, documenter)



