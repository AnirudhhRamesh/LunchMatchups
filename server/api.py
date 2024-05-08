import fastapi

app = fastapi.FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}
