from fastapi import FastAPI
import uvicorn

app = FastAPI(docs_url="/")
PORT = 8000


@app.get("/test")
def read_root():
    return {"message": "¡Hola, mundo!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, query_param: str = None):
    return {"item_id": item_id, "query_param": query_param}

def run_server():
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)



if __name__ == "__main__":
    run_server()
