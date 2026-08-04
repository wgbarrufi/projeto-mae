from database.create_tables import create_db_and_tables
from services.partida_service import PartidaService


def main():

    create_db_and_tables()

    service = PartidaService()

    quantidade = service.sincronizar_partidas("BSA")

    print(f"\n{quantidade} partidas importadas.\n")

    partidas = service.listar_partidas()

    print(f"Total de partidas cadastradas: {len(partidas)}\n")

    for partida in partidas[:10]:
        print(f"[{partida.id}] {partida.time_casa} x {partida.time_visitante}")


if __name__ == "__main__":
    main()