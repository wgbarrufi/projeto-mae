from datetime import datetime

from api.football_data_client import FootballDataClient
from models.partida import Partida
from repositories.partida_repository import PartidaRepository
from services.aposta_service import ApostaService

class PartidaService:
    """
    Camada de serviço responsável pelas regras relacionadas às partidas.

    Realiza sincronização com a API externa, listagem das partidas
    disponíveis e processamento do encerramento das partidas.
    """

    def __init__(self):
        self.repository = PartidaRepository()
        self.api = FootballDataClient()

    def sincronizar_partidas(self, competicao: str):
        """
        Consulta a API de futebol e armazena no banco as partidas
        ainda não cadastradas, utilizando o ID externo para evitar duplicidade.
        """

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
        """
        Retorna as partidas disponíveis para apostas.
        """
        return self.repository.listar_disponiveis()

    def encerrar_partida(
    self,
    partida_id,
    gols_casa,
    gols_visitante
    ):
        """
        Encerra uma partida, registra o placar e processa
        todas as apostas relacionadas a ela.
        """
        partida = self.repository.buscar_por_id(
            partida_id
        )

        if not partida:
            raise ValueError(
                "Partida não encontrada."
            )

        if partida.encerrada:
            raise ValueError(
                "Esta partida já foi encerrada."
            )

        partida.gols_casa = gols_casa
        partida.gols_visitante = gols_visitante
        partida.encerrada = True

        self.repository.atualizar(partida)

        apostas = ApostaService().listar_por_partida(
            partida_id
        )

        aposta_service = ApostaService()

        for aposta in apostas:

            aposta_service.processar_aposta(
                aposta,
                gols_casa,
                gols_visitante
            )
            
    def buscar_resultados(self, nome_time: str):

        if not nome_time or not nome_time.strip():
            raise ValueError(
                "Informe o nome de um time."
            )

        return self.repository.buscar_resultados_por_time(
            nome_time.strip()
        )