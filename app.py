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

app = Flask(__name__)

app.secret_key = "sistema_apostas_2026"


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

    return render_template(
        "partidas.html",
        partidas=partidas
    )

@app.route("/apostar/<int:partida_id>/<palpite>")
def apostar(partida_id, palpite):

    if "usuario_id" not in session:
        return redirect("/login")

    try:

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

        flash("Aposta realizada com sucesso!")

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

@app.route("/admin/usuarios")
def admin_usuarios():

    if session.get("usuario_tipo") != "ADMIN":
        return "Acesso negado"

    usuarios = UsuarioService().repository.listar()

    return render_template(
        "admin_usuarios.html",
        usuarios=usuarios
    )

@app.route("/admin/apostas")
def admin_apostas():

    if session.get("usuario_tipo") != "ADMIN":
        return "Acesso negado"

    apostas = ApostaRepository().listar()

    return render_template(
        "admin_apostas.html",
        apostas=apostas
    )





if __name__ == "__main__":
    app.run(debug=True)