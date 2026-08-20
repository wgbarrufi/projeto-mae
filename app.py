from flask import Flask, render_template, request, session, redirect, flash

from repositories.aposta_repository import ApostaRepository
from repositories.partida_repository import PartidaRepository

from models.usuario import Usuario
from models.partida import Partida
from models.aposta import Aposta

from services.usuario_service import UsuarioService
from services.partida_service import PartidaService

from datetime import datetime

from services.aposta_service import ApostaService

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY")


@app.route("/")
def index():

    nome = session.get("usuario_nome")

    return render_template(
        "index.html",
        usuario_nome=nome
    )


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        try:

            usuario = Usuario(
                nome=request.form["nome"],
                email=request.form["email"],
                cpf=request.form["cpf"],
                dataNascimento=datetime.strptime(
                    request.form["dataNascimento"],
                    "%Y-%m-%d"
                ).date(),
                login=request.form["login"],
                senha=request.form["senha"]
            )

            UsuarioService().cadastrar(usuario)

            return "Usuário cadastrado com sucesso!"

        except Exception as e:
            return f"Erro: {e}"

    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        try:

            usuario = UsuarioService().autenticar(
                request.form["login"],
                request.form["senha"]
            )

            session["usuario_id"] = usuario.id
            session["usuario_nome"] = usuario.nome
            session["usuario_pontos"] = usuario.pontos
            session["usuario_tipo"] = usuario.tipo

            print(usuario.tipo)

            return redirect("/")
        
        except Exception as e:

            return f"Erro: {e}"

    return render_template("login.html")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

@app.route("/partidas")
def partidas():

    if not session.get("usuario_id"):
        return redirect("/login")

    partidas = PartidaRepository().listar_disponiveis()

    aposta_service = ApostaService()

    odds = {}

    for partida in partidas:

        odds[partida.id] = aposta_service.calcular_odds(
            partida.id
        )

    return render_template(
        "partidas.html",
        partidas=partidas,
        odds=odds
    )
@app.route("/trocar-senha", methods=["GET", "POST"])
def trocar_senha():

    if "usuario_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        try:

            senha_atual = request.form["senha_atual"]
            nova_senha = request.form["nova_senha"]
            confirmar_senha = request.form["confirmar_senha"]

            if nova_senha != confirmar_senha:
                raise ValueError(
                    "A confirmação da nova senha não confere."
                )

            UsuarioService().trocar_senha(
                session["usuario_id"],
                senha_atual,
                nova_senha
            )

            flash("Senha alterada com sucesso!")

            return redirect("/")

        except Exception as e:

            flash(str(e))

    return render_template("trocar_senha.html")

@app.route("/apostar/<int:partida_id>/<palpite>")
def apostar(partida_id, palpite):

    if "usuario_id" not in session:
        return redirect("/login")

    try:

        # Busca a partida
        partida = PartidaRepository().buscar_por_id(
            partida_id
        )

        if not partida:
            raise ValueError(
                "Partida não encontrada."
            )

        # Verifica se a partida já foi encerrada
        if partida.encerrada:
            raise ValueError(
                "Esta partida já foi encerrada."
            )

        # Verifica se a partida já começou
        if partida.data_hora <= datetime.now():
            raise ValueError(
                "Não é mais possível apostar nesta partida."
            )

        # Obtém a odd atual do resultado escolhido
        if palpite == "CASA":
            odd_atual = partida.odd_casa

        elif palpite == "EMPATE":
            odd_atual = partida.odd_empate

        elif palpite == "VISITANTE":
            odd_atual = partida.odd_visitante

        else:
            raise ValueError(
                "Palpite inválido."
            )

        aposta = Aposta(
            usuario_id=session["usuario_id"],
            partida_id=partida_id,
            palpite=palpite,
            odd=1.0,
            valor_pontos=10,
            multiplicador=1
        )

        ApostaService().cadastrar(aposta)

        usuario = UsuarioService().repository.buscar_por_id(
            session["usuario_id"]
        )

        session["usuario_pontos"] = usuario.pontos

        flash(
            f"Aposta realizada com sucesso! "
            f"Odd utilizada: {odd_atual:.2f}"
        )

    except Exception as e:

        flash(str(e))

    return redirect("/partidas")

@app.route("/minhas-apostas")
def minhas_apostas():

    if "usuario_id" not in session:
        return redirect("/login")

    apostas = ApostaService().listar_por_usuario(
        session["usuario_id"]
    )

    return render_template(
        "minhas_apostas.html",
        apostas=apostas
    )

@app.route("/multiplicar-aposta/<int:aposta_id>")
def multiplicar_aposta(aposta_id):

    if "usuario_id" not in session:
        return redirect("/login")

    try:

        aposta = ApostaService().multiplicar_aposta(
            aposta_id,
            session["usuario_id"]
        )

        usuario = UsuarioService().repository.buscar_por_id(
            session["usuario_id"]
        )

        session["usuario_pontos"] = usuario.pontos

        flash(
            f"Aposta multiplicada para x{aposta.multiplicador}!"
        )

    except Exception as e:

        flash(str(e))

    return redirect("/minhas-apostas")

@app.route("/ranking")
def ranking():

    usuarios = UsuarioService().ranking()

    return render_template(
        "ranking.html",
        usuarios=usuarios
    )

@app.route(
    "/encerrar-partida/<int:partida_id>",
    methods=["GET", "POST"]
)
def encerrar_partida(partida_id):

    if session.get("usuario_tipo") != "ADMIN":
        return "Acesso negado"

    if request.method == "POST":

        gols_casa = int(
            request.form["gols_casa"]
        )

        gols_visitante = int(
            request.form["gols_visitante"]
        )

        PartidaService().encerrar_partida(
            partida_id,
            gols_casa,
            gols_visitante
        )

        return redirect("/partidas")

    partida = (
        PartidaService()
        .repository
        .buscar_por_id(partida_id)
    )

    return render_template(
        "encerrar_partida.html",
        partida=partida
    )

@app.route("/admin")
def admin():

    if session.get("usuario_tipo") != "ADMIN":
        return "Acesso negado"

    return render_template("admin.html")


@app.route("/admin/partidas")
def admin_partidas():

    if session.get("usuario_tipo") != "ADMIN":
        return "Acesso negado"

    partidas = PartidaRepository().listar()

    return render_template(
        "admin_partidas.html",
        partidas=partidas
    )

@app.route("/admin/usuarios", methods=["GET", "POST"])
def admin_usuarios():

    if session.get("usuario_tipo") != "ADMIN":
        return "Acesso negado"

    usuario = None
    erro = None

    if request.method == "POST":

        cpf = request.form.get("cpf")

        usuario = UsuarioService().repository.buscar_por_cpf(cpf)

        if not usuario:
            erro = "Nenhum usuário encontrado com esse CPF."

    usuarios = UsuarioService().repository.listar()

    return render_template(
        "admin_usuarios.html",
        usuarios=usuarios,
        usuario=usuario,
        erro=erro
    )

@app.route("/admin/apostas", methods=["GET", "POST"])
def admin_apostas():

    if session.get("usuario_tipo") != "ADMIN":
        return "Acesso negado"

    partida = None
    apostas = []
    erro = None
    odds = None

    if request.method == "POST":

        try:

            partida_id = int(
                request.form["partida_id"]
            )

            partida = PartidaRepository().buscar_por_id(
                partida_id
            )

            if not partida:
                raise ValueError(
                    "Partida não encontrada."
                )

            aposta_service = ApostaService()

            apostas = aposta_service.listar_por_partida(
                partida_id
            )

            odds = aposta_service.calcular_odds(
                partida_id
            )

        except ValueError as e:

            erro = str(e)

    return render_template(
        "admin_apostas.html",
        partida=partida,
        apostas=apostas,
        odds=odds,
        erro=erro
    )

@app.route("/saldo")
def saldo():

    if "usuario_id" not in session:
        return redirect("/login")

    try:

        usuario = UsuarioService().repository.buscar_por_id(
            session["usuario_id"]
        )

        if not usuario:
            raise ValueError("Usuário não encontrado.")

        return render_template(
            "saldo.html",
            usuario=usuario
        )

    except Exception as e:

        flash(str(e))

        return redirect("/")    

@app.route("/cancelar-participacao", methods=["GET", "POST"])
def cancelar_participacao():

    if "usuario_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        try:

            UsuarioService().inativar_usuario(
                session["usuario_id"]
            )

            session.clear()

            flash(
                "Sua participação nas apostas foi cancelada. "
                "Sua conta está inativa."
            )

            return redirect("/")

        except Exception as e:

            flash(str(e))

            return redirect("/")

    return render_template("cancelar_participacao.html")

@app.route("/resultados", methods=["GET", "POST"])
def resultados():

    if "usuario_id" not in session:
        return redirect("/login")

    partidas = []
    pesquisa = ""
    erro = None
    pesquisou = False

    if request.method == "POST":

        pesquisou = True

        try:

            pesquisa = request.form["time"]

            partidas = PartidaService().buscar_resultados(
                pesquisa
            )

            if not partidas:
                erro = (
                    "Nenhum resultado encontrado "
                    "para o time pesquisado."
                )

        except Exception as e:

            erro = str(e)

    return render_template(
        "resultados.html",
        partidas=partidas,
        pesquisa=pesquisa,
        erro=erro,
        pesquisou=pesquisou
    )

@app.route("/admin/sincronizar-partidas", methods=["POST"])
def admin_sincronizar_partidas():

    if session.get("usuario_tipo") != "ADMIN":
        return "Acesso negado"

    try:

        quantidade = PartidaService().sincronizar_partidas("BSA")

        if quantidade == 0:
            flash(
                "Nenhuma nova partida foi importada. "
                "As partidas já estavam cadastradas."
            )

        else:
            flash(
                f"{quantidade} partidas importadas com sucesso!"
            )

    except Exception as e:

        flash(
            f"Erro ao consultar a API: {e}"
        )

    return redirect("/admin")






if __name__ == "__main__":
    app.run(debug=True)