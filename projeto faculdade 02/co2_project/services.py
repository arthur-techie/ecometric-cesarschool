from database import conectar
from datetime import datetime

# --- FUNÇÕES DE CADASTRO E CÁLCULO ---

def listar_modelos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.id, m.nome, c.nome FROM modelos m
        JOIN categorias c ON m.categoria_id = c.id
    """)
    dados = cursor.fetchall()
    conn.close()
    return dados

def cadastrar_veiculo_por_modelo(placa, modelo_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO veiculos (placa, modelo_id) VALUES (?, ?)", (placa, modelo_id))
    conn.commit()
    conn.close()

def comparar_co2(placa, tipo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.emissao_co2_por_minuto, t.tempo_sem_tag, t.tempo_com_tag
        FROM veiculos v
        JOIN modelos m ON v.modelo_id = m.id
        JOIN categorias c ON m.categoria_id = c.id
        JOIN tempos_fila t ON t.tipo = ?
        WHERE v.placa = ?
    """, (tipo, placa))
    res = cursor.fetchone()
    if not res:
        conn.close()
        raise ValueError("❌ Veículo não encontrado")
    
    emissao, t_sem, t_com = res
    return (emissao * t_sem), (emissao * t_com), (emissao * (t_sem - t_com)), (t_sem - t_com)

# --- FUNÇÕES DE GAMIFICAÇÃO ---

def registrar_uso_taggy(placa, tipo):
    conn = conectar()
    cursor = conn.cursor()
    
    # Pontuação base: Pedágio +5, Shopping +3
    pts_base = 5 if tipo == "pedagio" else 3
    cursor.execute("INSERT INTO passagens (placa, tipo) VALUES (?, ?)", (placa, tipo))
    
    # Bônus de Frequência Mensal
    mes = datetime.now().strftime('%Y-%m')
    cursor.execute("SELECT COUNT(*) FROM passagens WHERE placa = ? AND strftime('%Y-%m', data_hora) = ?", (placa, mes))
    qtd = cursor.fetchone()[0]
    
    bonus = 0
    if qtd == 10: bonus = 20
    elif qtd == 20: bonus = 50
    elif qtd == 40: bonus = 100

    total_ganho = pts_base + bonus

    # Atualiza saldo
    cursor.execute("SELECT saldo FROM saldo_capcoins WHERE placa = ?", (placa,))
    if cursor.fetchone():
        cursor.execute("UPDATE saldo_capcoins SET saldo = saldo + ? WHERE placa = ?", (total_ganho, placa))
    else:
        cursor.execute("INSERT INTO saldo_capcoins (placa, saldo) VALUES (?, ?)", (placa, total_ganho))
    
    conn.commit()
    conn.close()
    return pts_base, bonus, qtd

def obter_painel_impacto(placa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT saldo FROM saldo_capcoins WHERE placa = ?", (placa,))
    res = cursor.fetchone()
    saldo = res[0] if res else 0

    cursor.execute("SELECT tipo FROM passagens WHERE placa = ?", (placa,))
    passagens = cursor.fetchall()
    conn.close()

    co2_evitado = sum([20 if p[0] == "pedagio" else 10 for p in passagens])
    folhas = int(co2_evitado / 5) # Estimativa visual

    return saldo, len(passagens), co2_evitado, folhas

def listar_recompensas_catalogo():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, custo FROM recompensas ORDER BY custo ASC")
    dados = cursor.fetchall()
    conn.close()
    return dados