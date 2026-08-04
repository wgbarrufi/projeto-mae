from models.aposta import Aposta
from models.status_aposta import StatusAposta
from repositories.aposta_repository import ApostaRepository
from repositories.usuario_repository import UsuarioRepository


class ApostaService:

    def __init__(self):
        self.repository = ApostaRepository()
        self.usuario_repository = UsuarioRepository()

    def cadastrar(self, aposta: Aposta):

        aposta_existente = (
            self.repository.buscar_por_usuario_e_partida(
                aposta.usuario_id,
                aposta.partida_id
            )
        )

        if aposta_existente:
            raise ValueError(
                "Você já apostou nesta partida."
            )

        usuario = self.usuario_repository.buscar_por_id(
            aposta.usuario_id
        )

        if usuario.pontos < aposta.valor_pontos:
            raise ValueError(
                "Pontos insuficientes."
            )

        usuario.pontos -= aposta.valor_pontos

        self.usuario_repository.atualizar(usuario)

        return self.repository.salvar(aposta)

    def listar_por_usuario(self, usuario_id: int):

        return self.repository.listar_por_usuario(
            usuario_id
        )

    def listar_por_partida(self, partida_id):

        return self.repository.listar_por_partida(
            partida_id
        )

    def processar_aposta(
        self,
        aposta,
        gols_casa,
        gols_visitante
    ):

        if gols_casa > gols_visitante:
            resultado = "CASA"

        elif gols_visitante > gols_casa:
            resultado = "VISITANTE"

        else:
            resultado = "EMPATE"

        if aposta.palpite == resultado:

            aposta.status = StatusAposta.GANHOU

            usuario = self.usuario_repository.buscar_por_id(
                aposta.usuario_id
            )

            usuario.pontos += int(
                aposta.valor_pontos * 2
            )

            usuario.acertos += 1

            self.usuario_repository.atualizar(
                usuario
            )

        else:

            aposta.status = StatusAposta.PERDEU

        self.repository.atualizar(aposta)

    def verificar_aposta_existente(self, usuario_id, partida_id):
        return self.repository.buscar_por_usuario_e_partida(
            usuario_id,
            partida_id
        )