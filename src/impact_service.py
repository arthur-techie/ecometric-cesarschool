from src.database import conectar


# =========================================================
# CALCULAR IMPACTO AMBIENTAL
# =========================================================
#
# Unidade:
#
# tempo -> minutos
# combustível -> ml
# co2 -> gramas
#
# =========================================================

def comparar_co2(

    placa,

    tipo
):

    conn = conectar()
    cursor = conn.cursor()

    # =====================================================
    # BUSCA DADOS AMBIENTAIS
    # =====================================================

    cursor.execute("""
        SELECT

            c.consumo_litro_hora,

            c.combustivel,

            c.fator_co2,

            c.hibrido,

            t.tempo_sem_tag,

            t.tempo_com_tag

        FROM veiculos v

        JOIN modelos m
            ON v.modelo_id = m.id

        JOIN categorias c
            ON m.categoria_id = c.id

        JOIN tempos_fila t
            ON t.tipo = ?

        WHERE v.placa = ?
    """, (

        tipo,

        placa
    ))

    res = cursor.fetchone()

    if not res:

        conn.close()

        raise ValueError(
            "❌ Veículo não encontrado"
        )

    (
        consumo_litro_hora,

        combustivel,

        fator_co2,

        hibrido,

        tempo_sem_tag,

        tempo_com_tag

    ) = res

    # =====================================================
    # TEMPO POUPADO
    # =====================================================

    tempo_poupado = (

        tempo_sem_tag -

        tempo_com_tag
    )

    # =====================================================
    # COMBUSTÍVEL POUPADO
    # =====================================================

    litros_poupados = (

        consumo_litro_hora *

        (tempo_poupado / 60)
    )

    # =====================================================
    # CONVERSÃO ML
    # =====================================================

    combustivel_poupado_ml = (

        litros_poupados * 1000
    )

    # =====================================================
    # CO2 EVITADO
    # =====================================================

    co2_evitar_g = (

        litros_poupados *

        fator_co2
    )

    # =====================================================
    # REGISTRA IMPACTO
    # =====================================================

    cursor.execute("""
        INSERT INTO impacto_ambiental (

            placa,

            tipo,

            tempo_poupado,

            combustivel_poupado_ml,

            co2_evitar_g

        )
        VALUES (?, ?, ?, ?, ?)
    """, (

        placa,

        tipo,

        round(tempo_poupado, 2),

        round(combustivel_poupado_ml, 2),

        round(co2_evitar_g, 2)
    ))

    conn.commit()
    conn.close()

    return {

        "tipo":
            tipo,

        "combustivel":
            combustivel,

        "hibrido":
            bool(hibrido),

        "tempo_poupado_min":
            round(tempo_poupado, 2),

        "combustivel_poupado_ml":
            round(combustivel_poupado_ml, 2),

        "co2_evitar_g":
            round(co2_evitar_g, 2)
    }


# =========================================================
# EQUIVALÊNCIA EM FOLHAS
# =========================================================

def calcular_equivalencia_folhas(

    co2_total
):

    return int(co2_total / 5)


# =========================================================
# EQUIVALÊNCIA ÁRVORES
# =========================================================

def calcular_equivalencia_arvores(

    co2_total
):

    return round(

        co2_total / 21000,

        2
    )


# =========================================================
# DASHBOARD AMBIENTAL
# =========================================================

def obter_painel_impacto(

    placa
):

    conn = conectar()
    cursor = conn.cursor()

    # =====================================================
    # SALDO CAPCOINS
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
    # IMPACTO TOTAL
    # =====================================================

    cursor.execute("""
        SELECT

            SUM(tempo_poupado),

            SUM(combustivel_poupado_ml),

            SUM(co2_evitar_g)

        FROM impacto_ambiental

        WHERE placa = ?
    """, (placa,))

    impacto = cursor.fetchone()

    tempo_total = impacto[0] or 0

    combustivel_total = impacto[1] or 0

    co2_total = impacto[2] or 0

    # =====================================================
    # TOTAL PASSAGENS
    # =====================================================

    cursor.execute("""
        SELECT COUNT(*)
        FROM passagens
        WHERE placa = ?
    """, (placa,))

    total_passagens = (
        cursor.fetchone()[0]
    )

    conn.close()

    # =====================================================
    # EQUIVALÊNCIAS
    # =====================================================

    folhas = calcular_equivalencia_folhas(
        co2_total
    )

    arvores = calcular_equivalencia_arvores(
        co2_total
    )

    return {

        "saldo_capcoins":
            saldo,

        "total_passagens":
            total_passagens,

        "tempo_total_min":
            round(tempo_total, 2),

        "combustivel_poupado_ml":
            round(combustivel_total, 2),

        "co2_total_g":
            round(co2_total, 2),

        "folhas_poupadas":
            folhas,

        "equivalente_arvores":
            arvores
    }


# =========================================================
# RANKING ESG
# =========================================================

def ranking_usuarios_verdes():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            placa,

            SUM(co2_evitar_g) as total_co2

        FROM impacto_ambiental

        GROUP BY placa

        ORDER BY total_co2 DESC
    """)

    ranking = cursor.fetchall()

    conn.close()

    return ranking


# =========================================================
# MÉTRICAS GLOBAIS ESG
# =========================================================

def metricas_globais():

    conn = conectar()
    cursor = conn.cursor()

    # =====================================================
    # CO2 TOTAL
    # =====================================================

    cursor.execute("""
        SELECT SUM(co2_evitar_g)
        FROM impacto_ambiental
    """)

    co2_total = (
        cursor.fetchone()[0] or 0
    )

    # =====================================================
    # TEMPO TOTAL
    # =====================================================

    cursor.execute("""
        SELECT SUM(tempo_poupado)
        FROM impacto_ambiental
    """)

    tempo_total = (
        cursor.fetchone()[0] or 0
    )

    # =====================================================
    # COMBUSTÍVEL TOTAL
    # =====================================================

    cursor.execute("""
        SELECT SUM(combustivel_poupado_ml)
        FROM impacto_ambiental
    """)

    combustivel_total = (
        cursor.fetchone()[0] or 0
    )

    conn.close()

    return {

        "co2_total_g":
            round(co2_total, 2),

        "tempo_total_min":
            round(tempo_total, 2),

        "combustivel_total_ml":
            round(combustivel_total, 2),

        "equivalente_arvores":
            calcular_equivalencia_arvores(
                co2_total
            )
    }