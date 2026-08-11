from datetime import datetime

from api.football_data_client import FootballDataClient
from models.partida import Partida
from repositories.partida_repository import PartidaRepository
from services.aposta_service import ApostaService

class PartidaService:

    def __init__(self):
        self.repository = PartidaRepository()
        self.api = FootballDataClient()

    def sincronizar_partidas(self, competicao: str):

        dados = self.api.listar_partidas(competicao)

        partidas_salvas = 0

        for jogo in dados["matches"]:

            # Evita cadastrar a mesma partida duas vezes
            if self.repository.buscar_por_api_id(jogo["id"]):
                continue

            partida = Partida(
                api_id=jogo["id"],
                time_casa=jogo["homeTeam"]["name"],
                time_visitante=jogo["awayTeam"]["name"],
                data_hora=datetime.fromisoformat(
                    jogo["utcDate"].replace("Z", "+00:00")
                ),
                odd_casa = 1.0,
                odd_empate = 1.0,
                odd_visitante = 1.0,
            )

            self.repository.salvar(partida)
            partidas_salvas += 1

        return partidas_salvas

    def listar_partidas(self):
        return self.repository.listar_disponiveis()

    def encerrar_partida(
        self,
        partida_id,
        gols_casa,
        gols_visitante
    ):

        partida = self.repository.buscar_por_id(
            partida_id
        )

        partida.gols_casa = gols_casa
        partida.gols_visitante = gols_visitante
        partida.encerrada = True

        self.repository.atualizar(partida)

        apostas = ApostaService().listar_por_partida(
            partida_id
        )

        for aposta in apostas:

            ApostaService().processar_aposta(
                aposta,
                gols_casa,
                gols_visitante
            )