from crewai import Agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

tester = Agent(
    role="Тестировщик",
    goal="Писать pytest-тесты и возвращать отчёты о багах",
    backstory="Инженер по качеству, педантичен в поиске ошибок.",
    llm=llm
)