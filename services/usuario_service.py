import re
from datetime import date

from werkzeug.security import generate_password_hash, check_password_hash

from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository
from models.status_usuario import StatusUsuario

class UsuarioService:
    """
    Camada de serviço responsável pelas regras de negócio dos usuários.

    Realiza cadastro, autenticação, troca de senha, consulta de saldo,
    inativação de contas e validações de idade e senha.
    """

    def __init__(self):
        self.repository = UsuarioRepository()

    def cadastrar(self, usuario: Usuario):
        """
        Cadastra um novo usuário após validar CPF, login, e-mail,
        idade mínima e regras de senha.
        """

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
                "Senha deve conter 8 caracteres, letra maiúscula, "
                "minúscula, número e caractere especial."
            )

        # Email já existe
        if self.repository.buscar_por_email(usuario.email):
            raise ValueError("E-mail já cadastrado.")

        # Transforma a senha em hash antes de salvar
        usuario.senha = generate_password_hash(usuario.senha)

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
        """
        Autentica um usuário verificando login, senha e status da conta.
        """

        usuario = self.repository.buscar_por_login(login)

        if not usuario:
            raise ValueError("Usuário não encontrado.")

        if usuario.status == StatusUsuario.INATIVO:
            raise ValueError(
                "Sua conta está inativa. Não é possível acessar o sistema."
            )

        if not check_password_hash(usuario.senha, senha):
            raise ValueError("Senha inválida.")

        return usuario

    def trocar_senha(
        self,
        usuario_id: int,
        senha_atual: str,
        nova_senha: str
    ):
        """
        Altera a senha do usuário após validar a senha atual
        e as regras de segurança da nova senha.
        """

        usuario = self.repository.buscar_por_id(usuario_id)

        if not usuario:
            raise ValueError("Usuário não encontrado.")

        # Confere se a senha atual está correta
        if not check_password_hash(
            usuario.senha,
            senha_atual
        ):
            raise ValueError("Senha atual inválida.")

        # Valida a nova senha
        if not self.__senha_valida(nova_senha):
            raise ValueError(
                "A nova senha deve conter pelo menos 8 caracteres, "
                "letra maiúscula, minúscula, número e caractere especial."
            )

        # Gera o hash da nova senha
        usuario.senha = generate_password_hash(
            nova_senha
        )

        return self.repository.atualizar(usuario)
    
    def ranking(self):
        return self.repository.ranking()

    def inativar_usuario(self, usuario_id: int):
        """
        Inativa a conta do usuário sem excluir seus dados do banco.
        """

        usuario = self.repository.buscar_por_id(usuario_id)

        if not usuario:
            raise ValueError("Usuário não encontrado.")

        if usuario.status == StatusUsuario.INATIVO:
            raise ValueError("Este usuário já está inativo.")

        usuario.status = StatusUsuario.INATIVO

        return self.repository.atualizar(usuario)

    def consultar_saldo(self, usuario_id: int):

        usuario = self.repository.buscar_por_id(usuario_id)

        if not usuario:
            raise ValueError("Usuário não encontrado.")

        return usuario.pontos

    def verificar_saldo(self, usuario_id: int):

        usuario = self.repository.buscar_por_id(usuario_id)

        if not usuario:
            raise ValueError("Usuário não encontrado.")

        if usuario.pontos <= 0:
            usuario.pontos = 0
            usuario.status = StatusUsuario.INATIVO

            self.repository.atualizar(usuario)

            return True

        return False

    