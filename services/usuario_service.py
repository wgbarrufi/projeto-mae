import re
from datetime import date

from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository


class UsuarioService:

    def __init__(self):
        self.repository = UsuarioRepository()

    def cadastrar(self, usuario: Usuario):

        # CPF já existe
        if self.repository.buscar_por_cpf(usuario.cpf):
            raise ValueError("CPF já cadastrado.")

        # Login já existe
        if self.repository.buscar_por_login(usuario.login):
            raise ValueError("Login já cadastrado.")

        # Idade
        if not self.__maior_de_idade(usuario.dataNascimento):
            raise ValueError("Usuário deve ser maior de 18 anos.")

        # Senha
        if not self.__senha_valida(usuario.senha):
            raise ValueError(
                "Senha deve conter 8 caracteres, letra maiúscula, minúscula, número e caractere especial."
            )
        # Email já existe
        if self.repository.buscar_por_email(usuario.email):
            raise ValueError("E-mail já cadastrado.")

        return self.repository.salvar(usuario)

    def __maior_de_idade(self, nascimento: date) -> bool:

        hoje = date.today()

        idade = hoje.year - nascimento.year

        if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):
            idade -= 1

        return idade >= 18

    def __senha_valida(self, senha: str) -> bool:

        regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$"

        return bool(re.match(regex, senha))

    def autenticar(self, login: str, senha: str):

        usuario = self.repository.buscar_por_login(login)

        if not usuario:
            raise ValueError("Usuário não encontrado.")

        if usuario.senha != senha:
            raise ValueError("Senha inválida.")

        return usuario

    def ranking(self):
        return self.repository.ranking()