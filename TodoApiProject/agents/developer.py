from crewai import Agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

developer = Agent(
    role="Разработчик",
    goal="Реализовать код по архитектуре и исправлять баги",
    backstory="Сильный Python-разработчик, пишет чистый и понятный код.",
    llm=llm
)