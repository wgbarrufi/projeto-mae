from enum import Enum

class StatusAposta(Enum):
    PENDENTE = "PENDENTE"
    GANHOU = "GANHOU"
    PERDEU = "PERDEU"
    EMPATE = "EMPATE"
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"