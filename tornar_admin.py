from models.usuario import Usuario
from models.aposta import Aposta
from models.partida import Partida

from repositories.usuario_repository import UsuarioRepository
from models.tipo_usuario import TipoUsuario

repo = UsuarioRepository()

usuario = repo.buscar_por_login("wagnerlogin")

usuario.tipo = TipoUsuario.ADMIN

repo.atualizar(usuario)

print("Usuário promovido para ADMIN!")