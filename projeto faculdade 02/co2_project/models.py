from database import conectar

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    # Estrutura de Veículos e Emissões
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        emissao_co2_por_minuto REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS modelos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria_id INTEGER,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS veiculos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT NOT NULL,
        modelo_id INTEGER,
        FOREIGN KEY (modelo_id) REFERENCES modelos(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tempos_fila (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        tempo_sem_tag REAL,
        tempo_com_tag REAL
    )
    """)

    # --- GAMIFICAÇÃO (CAPCOINS) ---
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saldo_capcoins (
        placa TEXT PRIMARY KEY,
        saldo INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS passagens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT NOT NULL,
        tipo TEXT NOT NULL,
        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recompensas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        custo INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()