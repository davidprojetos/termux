import requests
import sqlite3
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import time
import schedule
import os
import threading

# ============ CONFIGURAÇÕES ============

EMAIL_REMETENTE = 'seu_email@gmail.com'
SENHA_EMAIL = 'sua_senha_de_aplicativo'
EMAIL_DESTINATARIO = 'destinatario@email.com'

# ============ BUSCAR PREÇOS ============

def buscar_yahoo_finance(fii):
    print(f"🔎 [Yahoo Finance] {fii}")
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{fii}.SA"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        preco = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
        print(f"✅ Preço via Yahoo Finance: R${preco:.2f}")
        return float(preco)
    except Exception as e:
        print(f"❌ Erro ao buscar {fii} no Yahoo Finance: {e}")
        return None

def buscar_preco_fii(fii):
    fontes = [buscar_yahoo_finance]
    for fonte in fontes:
        try:
            preco = fonte(fii)
            if preco:
                return preco
        except Exception as e:
            print(f"⚠️ Falha em {fonte.__name__}: {e}")
    print(f"❌ Nenhuma fonte conseguiu o preço de {fii}.")
    return None

# ============ BANCO DE DADOS ============

def inicializar_banco():
    conn = sqlite3.connect('precos_fiis.db')
    c = conn.cursor()
    # Tabela de preços
    c.execute('''CREATE TABLE IF NOT EXISTS fiis (
                    fii TEXT,
                    data TEXT,
                    preco REAL,
                    PRIMARY KEY (fii, data)
                )''')
    # Tabela de posições (preço médio e última compra)
    c.execute('''CREATE TABLE IF NOT EXISTS posicoes (
                    fii TEXT PRIMARY KEY,
                    preco_medio REAL,
                    ultima_compra REAL
                )''')
    conn.commit()
    conn.close()

inicializar_banco()

# ============ LÓGICA DE MONITORAMENTO ============

def salvar_preco(fii, preco):
    conn = sqlite3.connect('precos_fiis.db')
    c = conn.cursor()
    hoje = datetime.now().date().isoformat()
    c.execute("DELETE FROM fiis WHERE fii = ? AND DATE(data) = ?", (fii, hoje))  # sobrescreve o preço do dia
    c.execute("INSERT INTO fiis (fii, data, preco) VALUES (?, ?, ?)",
              (fii, datetime.now().isoformat(), preco))
    conn.commit()
    conn.close()

def verificar_menor_preco(fii, preco_atual):
    conn = sqlite3.connect('precos_fiis.db')
    c = conn.cursor()
    c.execute("SELECT MIN(preco) FROM fiis WHERE fii = ?", (fii,))
    menor = c.fetchone()[0]
    conn.close()
    return menor is None or preco_atual < menor

def obter_posicao(fii):
    conn = sqlite3.connect('precos_fiis.db')
    c = conn.cursor()
    c.execute("SELECT preco_medio, ultima_compra FROM posicoes WHERE fii = ?", (fii,))
    dados = c.fetchone()
    conn.close()
    return dados if dados else (None, None)

def salvar_posicao(fii, preco_medio, ultima_compra):
    conn = sqlite3.connect('precos_fiis.db')
    c = conn.cursor()
    c.execute('''INSERT INTO posicoes (fii, preco_medio, ultima_compra)
                 VALUES (?, ?, ?)
                 ON CONFLICT(fii) DO UPDATE SET
                 preco_medio = excluded.preco_medio,
                 ultima_compra = excluded.ultima_compra''',
              (fii, preco_medio, ultima_compra))
    conn.commit()
    conn.close()

def rotina_monitoramento():
    if not os.path.exists("fiis.txt"):
        print("⚠️ Arquivo 'fiis.txt' não encontrado!")
        return

    with open("fiis.txt") as f:
        fiis = [linha.strip().upper() for linha in f if linha.strip()]

    for fii in fiis:
        preco = buscar_preco_fii(fii)
        if preco:
            salvar_preco(fii, preco)
            preco_medio, ultima_compra = obter_posicao(fii)
            print(f"\n🔍 Comparando {fii}:")
            if preco_medio:
                print(f"📊 Preço Médio: R${preco_medio:.2f}")
                print(f"📈 Último Preço de Compra: R${ultima_compra:.2f}")
                print(f"📉 Preço Atual: R${preco:.2f}")
                if preco < preco_medio:
                    print("💡 Está abaixo do preço médio.")
            else:
                print("ℹ️ Nenhuma posição registrada para esse FII.")

            if verificar_menor_preco(fii, preco):
                msg = f"O fundo {fii} atingiu o menor preço registrado: R${preco:.2f}"
                # enviar_email(EMAIL_DESTINATARIO, f"📉 Alerta: {fii} em menor preço!", msg)

# ============ HISTÓRICO ============

def mostrar_historico(fii):
    conn = sqlite3.connect('precos_fiis.db')
    c = conn.cursor()
    c.execute("SELECT data, preco FROM fiis WHERE fii = ? ORDER BY data DESC", (fii,))
    registros = c.fetchall()
    conn.close()

    if not registros:
        print(f"⚠️ Nenhum histórico encontrado para {fii}.")
        return

    print(f"\n📈 Histórico de preços para {fii}:")
    for data, preco in registros:
        data_fmt = datetime.fromisoformat(data).strftime('%d/%m/%Y %H:%M')
        print(f"  {data_fmt} → R${preco:.2f}")
    print()

def mostrar_historico_geral_resumido():
    conn = sqlite3.connect('precos_fiis.db')
    c = conn.cursor()
    c.execute("""
        SELECT fii, DATE(data), MAX(data), preco
        FROM (
            SELECT fii, data, preco
            FROM fiis
        )
        GROUP BY fii, DATE(data)
        ORDER BY fii, DATE(data) DESC
    """)
    registros = c.fetchall()
    conn.close()

    if not registros:
        print("⚠️ Nenhum dado encontrado no histórico.")
        return

    print("\n📊 Histórico geral (último preço por dia):\n")
    ultimo_fii = None
    for fii, data_dia, data_full, preco in registros:
        data_fmt = datetime.fromisoformat(data_full).strftime('%d/%m/%Y %H:%M')
        if fii != ultimo_fii:
            print(f"\n📌 {fii}")
            ultimo_fii = fii
        print(f"  {data_fmt} → R${preco:.2f}")
    print()

def mostrar_historico_geral_detalhado():
    conn = sqlite3.connect('precos_fiis.db')
    c = conn.cursor()
    c.execute("SELECT fii, data, preco FROM fiis ORDER BY fii, data DESC")
    registros = c.fetchall()
    conn.close()

    if not registros:
        print("⚠️ Nenhum dado encontrado no histórico.")
        return

    print("\n📊 Histórico geral detalhado (todos os registros):\n")
    ultimo_fii = None
    for fii, data, preco in registros:
        data_fmt = datetime.fromisoformat(data).strftime('%d/%m/%Y %H:%M')
        if fii != ultimo_fii:
            print(f"\n📌 {fii}")
            ultimo_fii = fii
        print(f"  {data_fmt} → R${preco:.2f}")
    print()

def comparar_com_base_local(fii):
    conn = sqlite3.connect('precos_fiis.db')
    c = conn.cursor()

    # Último preço registrado
    c.execute("SELECT data, preco FROM fiis WHERE fii = ? ORDER BY data DESC LIMIT 1", (fii,))
    resultado = c.fetchone()

    if not resultado:
        print(f"⚠️ Nenhum preço registrado no banco local para {fii}.")
        conn.close()
        return

    data, preco_atual = resultado

    # Posição (preço médio e última compra)
    c.execute("SELECT preco_medio, ultima_compra FROM posicoes WHERE fii = ?", (fii,))
    posicao = c.fetchone()
    conn.close()

    print(f"\n🔍 Comparando {fii}:")
    if posicao:
        preco_medio, ultima_compra = posicao
        print(f"📊 Preço Médio: R${preco_medio:.2f}")
        print(f"📈 Último Preço de Compra: R${ultima_compra:.2f}")
        print(f"📉 Preço Atual: R${preco_atual:.2f}")
        if preco_atual < preco_medio:
            print("💡 Está abaixo do preço médio.")
        else:
            print("📌 Está acima ou igual ao preço médio.")
    else:
        print("ℹ️ Nenhuma posição registrada para esse FII.")


def atualizar_posicao():
    fii = input("Digite o ticker do FII: ").strip().upper()
    try:
        preco_medio = float(input("Digite o preço médio de compra: ").strip().replace(",", "."))
        ultima_compra = float(input("Digite o preço da última compra: ").strip().replace(",", "."))
        salvar_posicao(fii, preco_medio, ultima_compra)
        print("✅ Posição atualizada com sucesso.")
    except ValueError:
        print("❌ Entrada inválida.")
        
        
def comparar_todos_com_base_local():
    if not os.path.exists("fiis.txt"):
        print("⚠️ Arquivo 'fiis.txt' não encontrado!")
        return

    with open("fiis.txt") as f:
        fiis = [linha.strip().upper() for linha in f if linha.strip()]

    conn = sqlite3.connect('precos_fiis.db')
    c = conn.cursor()

    for fii in fiis:
        # Pega o último preço registrado no banco
        c.execute("SELECT preco FROM fiis WHERE fii = ? ORDER BY data DESC LIMIT 1", (fii,))
        preco_result = c.fetchone()
        if not preco_result:
            print(f"\n🔍 {fii}: Nenhum preço registrado.")
            continue
        preco_atual = preco_result[0]

        # Pega posição (preço médio e última compra)
        c.execute("SELECT preco_medio, ultima_compra FROM posicoes WHERE fii = ?", (fii,))
        posicao = c.fetchone()

        print(f"\n🔍 Comparando {fii}:")
        if posicao:
            preco_medio, ultima_compra = posicao
            print(f"📊 Preço Médio: R${preco_medio:.2f}")
            print(f"📈 Último Preço de Compra: R${ultima_compra:.2f}")
            print(f"📉 Preço Atual: R${preco_atual:.2f}")
            if preco_atual < preco_medio:
                print("💡 Está abaixo do preço médio.")
            else:
                print("📌 Está acima ou igual ao preço médio.")
        else:
            print("ℹ️ Nenhuma posição registrada para esse FII.")

    conn.close()        
        

# ============ AGENDA ============

def agendar_rotina():
    schedule.every().day.at("22:27").do(rotina_monitoramento)
    while True:
        schedule.run_pending()
        time.sleep(60)

threading.Thread(target=agendar_rotina, daemon=True).start()

# ============ MENU ============

def menu():
    print("🟢 Monitor de FIIs iniciado. Aguardando horário agendado...\n")
    while True:
        print("\n📋 MENU PRINCIPAL")
        print("1. Rodar monitoramento agora")
        print("2. Ver histórico de um FII")
        print("3. Atualizar posição (preço médio e última compra)")
        print("4. Sair")
        print("5. Ver histórico geral (último preço por dia)")
        print("6. Ver histórico geral detalhado (todos os registros)")
        print("7. Comparar FII com base local (sem buscar online)")  # NOVA OPÇÃO
        print("8. Comparar todos os FIIs com base local (sem buscar online)")  # NOVA OPÇÃO
        
        
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            rotina_monitoramento()
        elif opcao == "2":
            fii = input("Digite o ticker do FII (ex: MXRF11): ").strip().upper()
            mostrar_historico(fii)
        elif opcao == "3":
            atualizar_posicao()
        elif opcao == "4":
            print("👋 Saindo...")
            break
        elif opcao == "5":
            mostrar_historico_geral_resumido()
        elif opcao == "6":
            mostrar_historico_geral_detalhado()
        elif opcao == "7":
            fii = input("Digite o ticker do FII para comparar: ").strip().upper()
            comparar_com_base_local(fii)
        elif opcao == "8":
            comparar_todos_com_base_local()    
        else:
            print("❌ Opção inválida.")

# ============ EXECUÇÃO ============

if __name__ == "__main__":
    menu()