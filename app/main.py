from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Olá QTS"}


@app.get("/user/{user_id}")
def read_user(user_id: int, q: str | None = None):
    return {"user_id": user_id, "q": q}


def uma_funcao_muito_longa(param1, param2, param3, param4, param5):
    print("Função muito longa!")
    return param1, param2, param3, param4, param5


@app.get("/mensagem")
def return_f299():
    return {
        "message": (
            "Mudanças na retirada de notebooks\n\n"
            "Com o objetivo de aprimorar o controle e a segurança dos "
            "equipamentos, desde o início do ano foi feito o fechamento "
            "dos carrinhos de carregamento dos notebooks às 19h30.\n\n"
            "Para situações em que um aluno eventualmente se atrase, foi "
            "permitida a retirada do equipamento por um colega, em seu nome. "
            "No entanto, observamos que em algumas turmas essa permissão tem "
            "sido utilizada de forma indevida, com um único aluno retirando "
            "vários notebooks (em alguns casos, quase para toda a turma), o "
            "que acaba incentivando atrasos sem justificativas relevantes.\n\n"
            "Diante disso, a partir de 2026, os carrinhos "
            "passarão a ser trancados mais cedo, às 18h50, não sendo mais "
            "permitida a retirada de notebooks por terceiros.\n\n"
            "Apenas alunos residentes em cidades onde atrasos são recorrentes "
            "(como Cananéia, Eldorado, entre outras) poderão realizar a "
            "retirada até 19h30. Casos excepcionais deverão ser tratados "
            "diretamente com a coordenação.\n\n"
            "Lamento a necessidade dessa medida e conto com a compreensão de "
            "todos. Obrigado."
        )
    }
