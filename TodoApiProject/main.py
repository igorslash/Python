from crewai import Crew, Process
from agents.architect import architect
from agents.developer import developer
from agents.tester import tester
from agents.documenter import documenter
from tasks.flow import create_tasks

if __name__ == "__main__":
    tasks = create_tasks(architect, developer, tester, documenter)

    crew = Crew(
        agents=[architect, developer, tester, documenter],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()
    print("\n=== Итоговый результат ===\n")
    print(result)