import sqlite3

# Inicializa o banco de dados e cria a tabela, se necessário
def init_db():
    conn = sqlite3.connect("gastos.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            categoria TEXT,
            descricao TEXT,
            tipo TEXT,
            valor REAL
        )
    """)
    conn.commit()
    conn.close()

# Conecta ao banco de dados
def get_connection():
    return sqlite3.connect("gastos.db")

# Insere uma transação no banco de dados
def inserir_transacao(data, categoria, descricao, tipo, valor):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transacoes (data, categoria, descricao, tipo, valor)
        VALUES (?, ?, ?, ?, ?)
    """, (data, categoria, descricao, tipo, valor))
    conn.commit()
    conn.close()

# Obtém todas as transações
def obter_transacoes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transacoes")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Atualiza uma transação existente
def atualizar_transacao(id, data, categoria, descricao, tipo, valor):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE transacoes
        SET data = ?, categoria = ?, descricao = ?, tipo = ?, valor = ?
        WHERE id = ?
    """, (data, categoria, descricao, tipo, valor, id))
    conn.commit()
    conn.close()

# Obtém uma transação específica pelo ID
def obter_transacao_por_id(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transacoes WHERE id = ?", (id,))
    transacao = cursor.fetchone()
    conn.close()
    return transacao
