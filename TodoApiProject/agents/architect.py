from crewai import Agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

architect = Agent(
    role="Архитектор",
    goal="Спроектировать архитектуру приложения",
    backstory="Опытный архитектор ПО, умеет разбивать задачу на модули и классы.",
    llm=llm
)
