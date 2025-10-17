from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Olá QTS"}


@app.get("/user/{user_id}")
def read_user(user_id: int, q: str | None = None):
    return {"user_id": user_id, "q": q}


@app.get(
    "/gabriel/<name>",
)
def say_gabriel(name):
    saudacao = "Bom dia, Boa tarde, Boa noite"

    return {
        "mensagem": f"{saudacao}, {name}!",
    }


def uma_funcao_muito_longa(param1, param2, param3, param4, param5):
    print("Função muito longa!")
    return param1, param2, param3, param4, param5
