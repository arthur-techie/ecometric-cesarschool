import requests

from src.database import conectar


# =========================================================
# CONFIGURAÇÃO DA API
# =========================================================

BASE_URL = "https://www.shopcar.com.br/"


# =========================================================
# CONSULTAR VEÍCULO NA API
# =========================================================
#
# Essa função consulta:
#
# marca
# modelo
# ano
# combustível
#
# =========================================================

def consultar_veiculo_shopcar(
    marca,
    modelo,
    ano
):

    try:

        # =================================================
        # MONTA URL
        # =================================================

        url = (
            f"{BASE_URL}/veiculos"
        )

        # =================================================
        # PARÂMETROS
        # =================================================

        params = {

            "marca": marca,

            "modelo": modelo,

            "ano": ano
        }

        # =================================================
        # REQUISIÇÃO
        # =================================================

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        # =================================================
        # VALIDA STATUS
        # =================================================

        response.raise_for_status()

        # =================================================
        # CONVERTE JSON
        # =================================================

        dados = response.json()

        # =================================================
        # VALIDA RETORNO
        # =================================================

        if not dados:

            raise ValueError(
                "❌ Veículo não encontrado na Shopcar"
            )

        return {

            "marca":
                dados.get("marca"),

            "modelo":
                dados.get("modelo"),

            "ano":
                dados.get("ano"),

            "combustivel":
                dados.get("combustivel"),

            "categoria":
                dados.get("categoria")
        }

    except requests.exceptions.Timeout:

        raise ValueError(
            "⏱️ Timeout na API Shopcar"
        )

    except requests.exceptions.ConnectionError:

        raise ValueError(
            "🌐 Erro de conexão com Shopcar"
        )

    except Exception as e:

        raise ValueError(
            f"❌ Erro API Shopcar: {e}"
        )


# =========================================================
# DESCOBRIR CATEGORIA PELO COMBUSTÍVEL
# =========================================================

def mapear_categoria_ambiental(
    categoria,
    combustivel
):

    categoria = categoria.lower()
    combustivel = combustivel.lower()

    # =====================================================
    # HÍBRIDO
    # =====================================================

    if "hibrid" in combustivel:

        return 5

    # =====================================================
    # ELÉTRICO
    # =====================================================

    if "eletric" in combustivel:

        return 6

    # =====================================================
    # SUV
    # =====================================================

    if "suv" in categoria:

        return 3

    # =====================================================
    # PICKUP
    # =====================================================

    if "pickup" in categoria:

        return 4

    # =====================================================
    # SEDAN
    # =====================================================

    if "sedan" in categoria:

        return 2

    # =====================================================
    # PADRÃO = HATCH
    # =====================================================

    return 1


# =========================================================
# CADASTRAR MODELO AUTOMATICAMENTE
# =========================================================

def cadastrar_modelo_automatico(
    marca,
    modelo,
    ano,
    categoria_id
):

    conn = conectar()
    cursor = conn.cursor()

    # =====================================================
    # VERIFICA SE JÁ EXISTE
    # =====================================================

    cursor.execute("""
        SELECT id
        FROM modelos
        WHERE nome = ?
        AND marca = ?
        AND ano = ?
    """, (

        modelo,
        marca,
        ano
    ))

    existente = cursor.fetchone()

    # =====================================================
    # SE EXISTIR
    # =====================================================

    if existente:

        conn.close()

        return existente[0]

    # =====================================================
    # SE NÃO EXISTIR
    # =====================================================

    cursor.execute("""
        INSERT INTO modelos (

            nome,

            marca,

            ano,

            categoria_id

        )
        VALUES (?, ?, ?, ?)
    """, (

        modelo,

        marca,

        ano,

        categoria_id
    ))

    modelo_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return modelo_id


# =========================================================
# CADASTRAR VEÍCULO VIA SHOPCAR
# =========================================================

def cadastrar_veiculo_via_shopcar(

    placa,

    marca,

    modelo,

    ano
):

    # =====================================================
    # CONSULTA API
    # =====================================================

    dados = consultar_veiculo_shopcar(

        marca,

        modelo,

        ano
    )

    # =====================================================
    # MAPEIA CATEGORIA
    # =====================================================

    categoria_id = mapear_categoria_ambiental(

        dados["categoria"],

        dados["combustivel"]
    )

    # =====================================================
    # CADASTRA MODELO
    # =====================================================

    modelo_id = cadastrar_modelo_automatico(

        dados["marca"],

        dados["modelo"],

        dados["ano"],

        categoria_id
    )

    # =====================================================
    # CADASTRA VEÍCULO
    # =====================================================

    conn = conectar()
    cursor = conn.cursor()

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

    return {

        "placa": placa,

        "marca": dados["marca"],

        "modelo": dados["modelo"],

        "ano": dados["ano"],

        "combustivel": dados["combustivel"],

        "categoria": dados["categoria"]
    }