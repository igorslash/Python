from fastapi import FastAPI
app = FastAPI()
@app.post("/ask")
async def ask(query: str):
    return {"response": ask_gpt(query)}