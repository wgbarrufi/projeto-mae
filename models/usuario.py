from datetime import date, datetime
from statusAposta import StatusAposta


class Usuario:
    def __init__(self, nome: str, email: str, cpf: str, dataNascimento: date, login: str, senha: str, tipo: str = "USUARIO"):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.dataNascimento = dataNascimento
        self.login = login
        self.senha = senha
        self.pontos = 100
        self.status = StatusAposta.ATIVO
        self.acertos = 0
        self.tipo = tipo

    def __str__(self):
        return f"Usuario: {self.nome}, Senha: {self.senha}"

    def setSenha(self):
        if len(self.senha) < 8:
            return "A senha deve conter no minimo 8 caracteres."
        if not any(char.isdigit() for char in self.senha):
            return "A senha deve conter pelo menos 1 digito"
        if not any(char in "!@#$%^&*()_+?" for char in self.senha):
            return "A senha deve conter pelo menos um caracter especial."
        if not any(c.isupper() for c in self.senha):
            return "A senha deve conter pelo menos uma letra maiuscula."
        return "A senha é válida."
       
    def setIdade(self):
        hoje = date.today()

        idade = hoje.year - self.dataNascimento.year

        if (hoje.month, hoje.day) < (self.dataNascimento.month, self.dataNascimento.day):
            idade -= 1

        if idade < 18:
            return "A idade deve ser maior ou igual a 18 anos."

        return "Idade válida."
    

#======================== TESTE ========================

if __name__ == "__main__":
    nome = input("Qual o nome? ")
    senha = input("Qual a senha? ")
    dataNascimento = input("Qual a data de nascimento? (AAAA-MM-DD) ")

    dataNascimento = datetime.strptime(dataNascimento, "%Y-%m-%d").date()

    email = "email"
    cpf = "cpf"
    login = "login"
    tipo = "tipo"

    usuario1 = Usuario(nome, email, cpf, dataNascimento, login, senha, tipo)

    print(usuario1.setIdade())

        
