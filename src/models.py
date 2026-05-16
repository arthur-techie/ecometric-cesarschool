from database import conectar


def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    # =========================================================
    # TABELA DE CATEGORIAS
    # =========================================================
    # Essa tabela agora representa o PERFIL AMBIENTAL
    # do veículo.
    #
    # consumo_litro_hora:
    # quanto o carro consome em marcha lenta.
    #
    # fator_co2:
    # quantidade de CO2 emitida por litro.
    #
    # hibrido:
    # 0 = não
    # 1 = sim
    # =========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nome TEXT NOT NULL,

        consumo_litro_hora REAL NOT NULL,

        combustivel TEXT NOT NULL,

        fator_co2 REAL NOT NULL,

        hibrido INTEGER DEFAULT 0
    )
    """)

    # =========================================================
    # TABELA DE MODELOS
    # =========================================================
    # Guarda os modelos dos veículos.
    #
    # Ex:
    # Corolla
    # Civic
    # Onix
    # Compass
    # =========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS modelos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nome TEXT NOT NULL,

        marca TEXT,

        ano INTEGER,

        categoria_id INTEGER,

        FOREIGN KEY (categoria_id)
            REFERENCES categorias(id)
    )
    """)

    # =========================================================
    # TABELA DE VEÍCULOS
    # =========================================================
    # Veículos cadastrados pelos usuários.
    #
    # Cada veículo aponta para um modelo.
    # =========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS veiculos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        placa TEXT NOT NULL UNIQUE,

        modelo_id INTEGER,

        FOREIGN KEY (modelo_id)
            REFERENCES modelos(id)
    )
    """)

    # =========================================================
    # TABELA DE TEMPOS DE FILA
    # =========================================================
    # Define:
    #
    # tempo_sem_tag:
    # quanto tempo o usuário leva sem Taggy.
    #
    # tempo_com_tag:
    # quanto tempo leva usando Taggy.
    #
    # Unidade:
    # MINUTOS
    # =========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tempos_fila (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        tipo TEXT NOT NULL,

        tempo_sem_tag REAL NOT NULL,

        tempo_com_tag REAL NOT NULL
    )
    """)

    # =========================================================
    # TABELA DE IMPACTO AMBIENTAL
    # =========================================================
    # Histórico ambiental gerado por cada uso da Taggy.
    #
    # tempo_poupado:
    # minutos economizados.
    #
    # combustivel_poupado_ml:
    # combustível poupado em mililitros.
    #
    # co2_evitar_g:
    # CO2 evitado em GRAMAS.
    # =========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS impacto_ambiental (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        placa TEXT NOT NULL,

        tipo TEXT NOT NULL,

        tempo_poupado REAL NOT NULL,

        combustivel_poupado_ml REAL NOT NULL,

        co2_evitar_g REAL NOT NULL,

        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =========================================================
    # TABELA DE SALDO CAPCOINS
    # =========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saldo_capcoins (
        placa TEXT PRIMARY KEY,

        saldo INTEGER DEFAULT 0
    )
    """)

    # =========================================================
    # TABELA DE PASSAGENS
    # =========================================================
    # Guarda os usos da Taggy.
    # =========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS passagens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        placa TEXT NOT NULL,

        tipo TEXT NOT NULL,

        capcoins_ganhos INTEGER DEFAULT 0,

        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =========================================================
    # TABELA DE RECOMPENSAS
    # =========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recompensas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nome TEXT NOT NULL,

        custo INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()

    print("✅ Estrutura do banco criada com sucesso!")