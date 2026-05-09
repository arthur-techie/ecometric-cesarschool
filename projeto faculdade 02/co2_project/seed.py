from database import conectar
from models import criar_tabelas

def popular_banco():
    criar_tabelas()
    conn = conectar()
    cursor = conn.cursor()

    # Popula Categorias e Modelos se estiverem vazios
    cursor.execute("SELECT COUNT(*) FROM categorias")
    if cursor.fetchone()[0] == 0:
        categorias = [("Hatch", 33.3), ("Sedan", 38.3), ("SUV", 46.7)]
        cursor.executemany("INSERT INTO categorias (nome, emissao_co2_por_minuto) VALUES (?, ?)", categorias)

        modelos = [("Gol", 1), ("Onix", 1), ("Corolla", 2), ("Civic", 2), ("Compass", 3), ("HR-V", 3)]
        cursor.executemany("INSERT INTO modelos (nome, categoria_id) VALUES (?, ?)", modelos)

        tempos = [("shopping", 10, 1), ("pedagio", 5, 1)]
        cursor.executemany("INSERT INTO tempos_fila (tipo, tempo_sem_tag, tempo_com_tag) VALUES (?, ?, ?)", tempos)

    # Inserir Catálogo de Recompensas (A Loja)
    cursor.execute("SELECT COUNT(*) FROM recompensas")
    if cursor.fetchone()[0] == 0:
        catalogo = [
            ("Doação para ONG ambiental (R$ 10)", 100),
            ("Ecobag reutilizável", 150),
            ("Desconto em lavagem a seco ecológica", 150),
            ("Crédito em app de mobilidade verde (Bike Itaú)", 200),
            ("Garrafa térmica sustentável", 250),
            ("Plantio de 1 árvore (via parceiro)", 300),
            ("Desconto no próximo plano Taggy", 350),
            ("Cesta de produtos orgânicos", 400)
        ]
        cursor.executemany("INSERT INTO recompensas (nome, custo) VALUES (?, ?)", catalogo)
        print("🎁 Catálogo de recompensas cadastrado!")

    conn.commit()
    conn.close()
    print("✅ Banco de dados pronto com Gamificação!")

if __name__ == "__main__":
    popular_banco()