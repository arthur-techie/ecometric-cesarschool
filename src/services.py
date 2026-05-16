from datetime import datetime

from src.database import conectar


# =========================================================
# LISTAR MODELOS
# =========================================================

def listar_modelos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            m.id,

            m.nome,

            m.marca,

            m.ano,

            c.nome

        FROM modelos m

        JOIN categorias c
            ON m.categoria_id = c.id

        ORDER BY m.nome
    """)

    modelos = cursor.fetchall()

    conn.close()

    return modelos


# =========================================================
# CADASTRAR VEÍCULO MANUAL
# =========================================================

def cadastrar_veiculo_por_modelo(

    placa,

    modelo_id
):

    conn = conectar()
    cursor = conn.cursor()

    # =====================================================
    # VERIFICA DUPLICIDADE
    # =====================================================

    cursor.execute("""
        SELECT id
        FROM veiculos
        WHERE placa = ?
    """, (placa,))

    if cursor.fetchone():

        conn.close()

        raise ValueError(
            "❌ Veículo já cadastrado"
        )

    # =====================================================
    # CADASTRA
    # =====================================================

    cursor.execute("""
        INSERT INTO veiculos (

            placa,

            modelo_id

        )
        VALUES (?, ?)
    """, (

        placa,

        modelo_id
    ))

    conn.commit()
    conn.close()


# =========================================================
# REGISTRAR USO TAGGY
# =========================================================

def registrar_uso_taggy(

    placa,

    tipo
):

    conn = conectar()
    cursor = conn.cursor()

    # =====================================================
    # VERIFICA VEÍCULO
    # =====================================================

    cursor.execute("""
        SELECT id
        FROM veiculos
        WHERE placa = ?
    """, (placa,))

    if not cursor.fetchone():

        conn.close()

        raise ValueError(
            "❌ Veículo não encontrado"
        )

    # =====================================================
    # PONTUAÇÃO BASE
    # =====================================================

    pontos_base = {

        "pedagio": 5,

        "shopping": 3,

        "condominio": 2,

        "drive_thru": 2
    }

    pontos = pontos_base.get(tipo, 1)

    # =====================================================
    # REGISTRA PASSAGEM
    # =====================================================

    cursor.execute("""
        INSERT INTO passagens (

            placa,

            tipo

        )
        VALUES (?, ?)
    """, (

        placa,

        tipo
    ))

    # =====================================================
    # TOTAL PASSAGENS MÊS
    # =====================================================

    mes_atual = datetime.now().strftime(
        "%Y-%m"
    )

    cursor.execute("""
        SELECT COUNT(*)

        FROM passagens

        WHERE placa = ?

        AND strftime(
            '%Y-%m',
            data_hora
        ) = ?
    """, (

        placa,

        mes_atual
    ))

    total_mes = cursor.fetchone()[0]

    # =====================================================
    # BÔNUS FREQUÊNCIA
    # =====================================================

    bonus = 0

    if total_mes == 10:

        bonus = 20

    elif total_mes == 20:

        bonus = 50

    elif total_mes == 40:

        bonus = 100

    total_ganho = (

        pontos +

        bonus
    )

    # =====================================================
    # ATUALIZA SALDO
    # =====================================================

    cursor.execute("""
        SELECT saldo
        FROM saldo_capcoins
        WHERE placa = ?
    """, (placa,))

    existe = cursor.fetchone()

    if existe:

        cursor.execute("""
            UPDATE saldo_capcoins

            SET saldo = saldo + ?

            WHERE placa = ?
        """, (

            total_ganho,

            placa
        ))

    else:

        cursor.execute("""
            INSERT INTO saldo_capcoins (

                placa,

                saldo

            )
            VALUES (?, ?)
        """, (

            placa,

            total_ganho
        ))

    conn.commit()
    conn.close()

    return {

        "pontos_base":
            pontos,

        "bonus":
            bonus,

        "total_ganho":
            total_ganho,

        "total_passagens_mes":
            total_mes
    }


# =========================================================
# CATÁLOGO RECOMPENSAS
# =========================================================

def listar_recompensas_catalogo():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            nome,

            custo

        FROM recompensas

        ORDER BY custo ASC
    """)

    recompensas = cursor.fetchall()

    conn.close()

    return recompensas


# =========================================================
# RESGATAR RECOMPENSA
# =========================================================

def resgatar_recompensa(

    placa,

    recompensa_id
):

    conn = conectar()
    cursor = conn.cursor()

    # =====================================================
    # BUSCA RECOMPENSA
    # =====================================================

    cursor.execute("""
        SELECT

            nome,

            custo

        FROM recompensas

        WHERE id = ?
    """, (recompensa_id,))

    recompensa = cursor.fetchone()

    if not recompensa:

        conn.close()

        raise ValueError(
            "❌ Recompensa não encontrada"
        )

    nome_recompensa = recompensa[0]

    custo = recompensa[1]

    # =====================================================
    # BUSCA SALDO
    # =====================================================

    cursor.execute("""
        SELECT saldo
        FROM saldo_capcoins
        WHERE placa = ?
    """, (placa,))

    saldo_res = cursor.fetchone()

    saldo = (

        saldo_res[0]

        if saldo_res

        else 0
    )

    # =====================================================
    # VALIDA SALDO
    # =====================================================

    if saldo < custo:

        conn.close()

        raise ValueError(
            "❌ Saldo insuficiente"
        )

    # =====================================================
    # DESCONTA SALDO
    # =====================================================

    novo_saldo = saldo - custo

    cursor.execute("""
        UPDATE saldo_capcoins

        SET saldo = ?

        WHERE placa = ?
    """, (

        novo_saldo,

        placa
    ))

    conn.commit()
    conn.close()

    return {

        "recompensa":
            nome_recompensa,

        "saldo_restante":
            novo_saldo
    }