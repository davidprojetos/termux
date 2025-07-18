import sqlite3

conn = sqlite3.connect("fiis.db")
c = conn.cursor()

# 1. Tenta adicionar a coluna (ignora erro se já existir)
try:
    c.execute("ALTER TABLE compras ADD COLUMN qtd_disponivel REAL")
except sqlite3.OperationalError:
    print("🔁 Coluna 'qtd_disponivel' já existe. Pulando criação.")

# 2. Atualiza os valores nulos
c.execute("""
    UPDATE compras
    SET qtd_disponivel = quantidade
    WHERE qtd_disponivel IS NULL
""")

conn.commit()
conn.close()
print("✅ Migração concluída: coluna 'qtd_disponivel' adicionada/preenchida.")
