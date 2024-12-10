import sqlite3

# Função para criar a tabela de transações
def criar_tabela():
    conexao = sqlite3.connect("transacoes.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            tipo TEXT,
            categoria TEXT,
            valor REAL,
            data TEXT
        )
    """)
    conexao.commit()
    conexao.close()

# Função para adicionar uma nova transação
def adicionar_transacao(descricao, tipo, categoria, valor, data):
    conexao = sqlite3.connect("transacoes.db")
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO transacoes (descricao, tipo, categoria, valor, data)
        VALUES (?, ?, ?, ?, ?)
    """, (descricao, tipo, categoria, valor, data))
    conexao.commit()
    conexao.close()

# Função para visualizar todas as transações
def visualizar_transacoes():
    conexao = sqlite3.connect("transacoes.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM transacoes")
    transacoes = cursor.fetchall()
    conexao.close()
    return transacoes

# Função para editar uma transação existente
def editar_transacao(id, descricao, tipo, categoria, valor, data):
    conexao = sqlite3.connect("transacoes.db")
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE transacoes
        SET descricao = ?, tipo = ?, categoria = ?, valor = ?, data = ?
        WHERE id = ?
    """, (descricao, tipo, categoria, valor, data, id))
    conexao.commit()
    conexao.close()
