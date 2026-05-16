from database import conectar
from models import criar_tabelas


def popular_banco():

    # =========================================================
    # GARANTE QUE AS TABELAS EXISTEM
    # =========================================================

    criar_tabelas()

    conn = conectar()
    cursor = conn.cursor()

    # =========================================================
    # POPULAR CATEGORIAS
    # =========================================================
    # consumo_litro_hora:
    # consumo do veículo em marcha lenta.
    #
    # fator_co2:
    # emissão de CO2 em gramas por litro.
    #
    # hibrido:
    # 0 = não
    # 1 = sim
    # =========================================================

    cursor.execute("SELECT COUNT(*) FROM categorias")

    if cursor.fetchone()[0] == 0:

        categorias = [

            # HATCH GASOLINA
            (
                "Hatch",
                0.6,
                "gasolina",
                2310,
                0
            ),

            # SEDAN FLEX
            (
                "Sedan",
                0.8,
                "flex",
                2100,
                0
            ),

            # SUV GASOLINA
            (
                "SUV",
                1.2,
                "gasolina",
                2310,
                0
            ),

            # PICKUP DIESEL
            (
                "Pickup",
                1.5,
                "diesel",
                2680,
                0
            ),

            # HÍBRIDO
            (
                "Hibrido",
                0.3,
                "hibrido",
                900,
                1
            ),

            # ELÉTRICO
            (
                "Eletrico",
                0.0,
                "eletrico",
                0,
                0
            )
        ]

        cursor.executemany("""
            INSERT INTO categorias (
                nome,
                consumo_litro_hora,
                combustivel,
                fator_co2,
                hibrido
            )
            VALUES (?, ?, ?, ?, ?)
        """, categorias)

        print("✅ Categorias ambientais cadastradas!")

    # =========================================================
    # POPULAR MODELOS
    # =========================================================
    # categoria_id:
    #
    # 1 = Hatch
    # 2 = Sedan
    # 3 = SUV
    # 4 = Pickup
    # 5 = Hibrido
    # 6 = Eletrico
    # =========================================================

    cursor.execute("SELECT COUNT(*) FROM modelos")

    if cursor.fetchone()[0] == 0:

        modelos = [

            ("Gol", "Volkswagen", 2020, 1),
            ("Onix", "Chevrolet", 2022, 1),

            ("Corolla", "Toyota", 2023, 2),
            ("Civic", "Honda", 2022, 2),

            ("Compass", "Jeep", 2024, 3),
            ("HR-V", "Honda", 2023, 3),

            ("Hilux", "Toyota", 2024, 4),

            ("Corolla Hybrid", "Toyota", 2025, 5),

            ("BYD Dolphin", "BYD", 2025, 6)
        ]

        cursor.executemany("""
            INSERT INTO modelos (
                nome,
                marca,
                ano,
                categoria_id
            )
            VALUES (?, ?, ?, ?)
        """, modelos)

        print("✅ Modelos cadastrados!")

    # =========================================================
    # POPULAR TEMPOS MÉDIOS DE FILA
    # =========================================================
    # Unidade:
    # minutos
    # =========================================================

    cursor.execute("SELECT COUNT(*) FROM tempos_fila")

    if cursor.fetchone()[0] == 0:

        tempos = [

            # SHOPPING
            (
                "shopping",
                10,
                2
            ),

            # PEDÁGIO
            (
                "pedagio",
                5,
                1
            ),

            # CONDOMÍNIO
            (
                "condominio",
                4,
                1
            ),

            # DRIVE THRU
            (
                "drive_thru",
                8,
                3
            )
        ]

        cursor.executemany("""
            INSERT INTO tempos_fila (
                tipo,
                tempo_sem_tag,
                tempo_com_tag
            )
            VALUES (?, ?, ?)
        """, tempos)

        print("✅ Tempos médios cadastrados!")

    # =========================================================
    # POPULAR RECOMPENSAS
    # =========================================================

    cursor.execute("SELECT COUNT(*) FROM recompensas")

    if cursor.fetchone()[0] == 0:

        catalogo = [

            (
                "Doação ONG Ambiental",
                100
            ),

            (
                "Ecobag Sustentável",
                150
            ),

            (
                "Lavagem Ecológica",
                150
            ),

            (
                "Crédito Bike Itaú",
                200
            ),

            (
                "Garrafa Sustentável",
                250
            ),

            (
                "Plantio de Árvore",
                300
            ),

            (
                "Desconto Plano Taggy",
                350
            ),

            (
                "Cesta Orgânica",
                400
            )
        ]

        cursor.executemany("""
            INSERT INTO recompensas (
                nome,
                custo
            )
            VALUES (?, ?)
        """, catalogo)

        print("✅ Catálogo de recompensas cadastrado!")

    # =========================================================
    # FINALIZA
    # =========================================================

    conn.commit()
    conn.close()

    print("✅ Banco populado com sucesso!")


if __name__ == "__main__":
    popular_banco()