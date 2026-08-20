from models.aposta import Aposta
from models.status_aposta import StatusAposta
from repositories.aposta_repository import ApostaRepository
from repositories.usuario_repository import UsuarioRepository
from repositories.partida_repository import PartidaRepository
from datetime import datetime
from services.usuario_service import UsuarioService

class ApostaService:
    """
    Camada de serviço responsável pelas regras de negócio das apostas.

    Controla criação, cálculo de odds, multiplicação, processamento
    dos resultados e atualização de pontos dos usuários.
    """

    def __init__(self):
        self.repository = ApostaRepository()
        self.usuario_repository = UsuarioRepository()
        self.partida_repository = PartidaRepository()

    def cadastrar(self, aposta: Aposta):
        """
        Registra uma aposta após validar usuário, saldo, partida,
        horário e existência de aposta anterior.
        """

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

        if not usuario:
            raise ValueError(
                "Usuário não encontrado."
            )

        if usuario.pontos < aposta.valor_pontos:
            raise ValueError(
                "Pontos insuficientes."
            )

        partida = self.partida_repository.buscar_por_id(
            aposta.partida_id
        )

        if not partida:
            raise ValueError(
                "Partida não encontrada."
            )

        if partida.encerrada:
            raise ValueError(
                "Esta partida já foi encerrada."
            )
        
        if datetime.now(partida.data_hora.tzinfo) >= partida.data_hora:
            raise ValueError(
                "Não é possível apostar em uma partida que já começou."
            )

        # Calcula as odds atuais antes de registrar a nova aposta
        odds = self.calcular_odds(aposta.partida_id)

        if aposta.palpite not in odds:
            raise ValueError(
                "Palpite inválido."
            )

        aposta.odd = odds[aposta.palpite]

        # Desconta os pontos do usuário
        usuario.pontos -= aposta.valor_pontos

        self.usuario_repository.atualizar(usuario)

        # Se o saldo chegou a zero, inativa o usuário
        UsuarioService().verificar_saldo(usuario.id)
        # Registra a aposta
        aposta_salva = self.repository.salvar(aposta)

        # Recalcula as odds depois da nova aposta
        novas_odds = self.calcular_odds(aposta.partida_id)

        partida.odd_casa = novas_odds["CASA"]
        partida.odd_empate = novas_odds["EMPATE"]
        partida.odd_visitante = novas_odds["VISITANTE"]

        self.partida_repository.atualizar(partida)

        return aposta_salva

    def calcular_odds(self, partida_id):

        apostas = self.repository.listar_por_partida(partida_id)

        quantidade_casa = 0
        quantidade_empate = 0
        quantidade_visitante = 0

        for aposta in apostas:

            if aposta.palpite == "CASA":
                quantidade_casa += 1

            elif aposta.palpite == "EMPATE":
                quantidade_empate += 1

            elif aposta.palpite == "VISITANTE":
                quantidade_visitante += 1

        total = (
            quantidade_casa
            + quantidade_empate
            + quantidade_visitante
        )

        # Se ainda não existem apostas,
        # todas começam com odd 1.0
        if total == 0:

            return {
                "CASA": 1.0,
                "EMPATE": 1.0,
                "VISITANTE": 1.0
            }

        def calcular_odd(quantidade):

            if quantidade == 0:
                return 1.0

            outros = total - quantidade

            return round(
                1 + (outros / quantidade),
                2
            )

        return {
            "CASA": calcular_odd(quantidade_casa),
            "EMPATE": calcular_odd(quantidade_empate),
            "VISITANTE": calcular_odd(quantidade_visitante)
        }

    def listar_por_usuario(self, usuario_id: int):

        return self.repository.listar_por_usuario(
            usuario_id
        )

    def listar_por_partida(self, partida_id: int):

        return self.repository.listar_por_partida(
            partida_id
        )

    def processar_aposta(
        self,
        aposta,
        gols_casa,
        gols_visitante
    ):
        """
        Processa uma aposta após o encerramento da partida.

        Atualiza o status da aposta, distribui pontos quando houver
        acerto e devolve os pontos investidos em caso de empate.
        """
        usuario = self.usuario_repository.buscar_por_id(
            aposta.usuario_id
        )

        if not usuario:
            raise ValueError("Usuário não encontrado.")

        if gols_casa == gols_visitante:

            aposta.status = StatusAposta.EMPATE

            valor_devolucao = (
                aposta.valor_pontos
                * aposta.multiplicador
            )

            usuario.pontos += int(valor_devolucao)

            self.usuario_repository.atualizar(usuario)

            self.repository.atualizar(aposta)

            return
        
        if gols_casa > gols_visitante:
            resultado = "CASA"

        else:
            resultado = "VISITANTE"

        if aposta.palpite == resultado:

            aposta.status = StatusAposta.GANHOU

            premio = (
                aposta.valor_pontos
                * aposta.odd
                * aposta.multiplicador
            )

            usuario.pontos += int(premio)

            usuario.acertos += 1

            self.usuario_repository.atualizar(
                usuario
            )

        else:

            aposta.status = StatusAposta.PERDEU

        self.repository.atualizar(aposta)

    def multiplicar_aposta(self, aposta_id, usuario_id):

        aposta = self.repository.buscar_por_id(aposta_id)

        if not aposta:
            raise ValueError("Aposta não encontrada.")

        if aposta.usuario_id != usuario_id:
            raise ValueError(
                "Você não pode alterar esta aposta."
            )

        if aposta.status != StatusAposta.PENDENTE:
            raise ValueError(
                "Não é possível multiplicar uma aposta encerrada."
            )

        usuario = self.usuario_repository.buscar_por_id(
            usuario_id
        )

        if not usuario:
            raise ValueError("Usuário não encontrado.")

        valor_multiplicacao = aposta.valor_pontos

        if usuario.pontos < valor_multiplicacao:
            raise ValueError(
                "Pontos insuficientes para multiplicar a aposta."
            )

        usuario.pontos -= valor_multiplicacao

        aposta.multiplicador += 1

        self.usuario_repository.atualizar(usuario)

        UsuarioService().verificar_saldo(usuario.id)

        return self.repository.atualizar(aposta)

    def verificar_aposta_existente(
        self,
        usuario_id,
        partida_id
    ):

        return self.repository.buscar_por_usuario_e_partida(
            usuario_id,
            partida_id
        )