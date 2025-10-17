from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Olá QTS"}


@app.get("/top_dez")
def top_dez(nome: str):
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    return arr[0]  # Return the first element to avoid IndexError


@app.get("/user/{user_id}")
def read_user(user_id: int, q: str | None = None):
    return {"user_id": user_id, "q": q}


def uma_funcao_muito_longa(param1, param2, param3, param4, param5):
    print("Função muito longa!")
    return param1, param2, param3, param4, param5
