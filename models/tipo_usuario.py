from enum import Enum

class TipoUsuario(str, Enum):
    USUARIO = "USUARIO"
    ADMIN = "ADMIN"