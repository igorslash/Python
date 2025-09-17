from crewai import Crew
from flow import create_tasks
from agents import architect, developer, tester, documenter
import os

def main():
    print("🚀 Starting ToDo List App Development Crew...")
    
    # Создаем задачи
    tasks = create_tasks()
    
    # Создаем crew
    crew = Crew(
        agents=[architect, developer, tester, documenter],
        tasks=tasks,
        verbose=True
    )
    
    # Запускаем процесс
    result = crew.kickoff()
    
    print("✅ Development completed!")
    print(f"Results saved in 'output/' directory")
    
    return result

if __name__ == "__main__":
    main()