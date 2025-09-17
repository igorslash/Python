from crewai import Agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

documenter = Agent(
    role="Документатор",
    goal="Создавать README и документацию",
    backstory="Технический писатель, умеет делать инструкции простыми и понятными.",
    llm=llm
)