#!/usr/bin/env python3
# fiiprovisor.py

import sqlite3
import argparse
from datetime import date, timedelta
from calendar import month_name

DB_FILE = 'fiis.db'

def connect():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(conn):
    c = conn.cursor()

    # Tabela de fundos
    c.execute('''
        CREATE TABLE IF NOT EXISTS fundos (
            ticker TEXT PRIMARY KEY,
            qty REAL NOT NULL,
            total_investido REAL NOT NULL
        )
    ''')

    # Tabela de proventos
    c.execute('''
        CREATE TABLE IF NOT EXISTS proventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            ano INTEGER NOT NULL,
            mes  INTEGER NOT NULL,
            valor_cota REAL NOT NULL,
            UNIQUE(ticker, ano, mes),
            FOREIGN KEY(ticker) REFERENCES fundos(ticker)
        )
    ''')

    # Tabela de compras
    c.execute('''
        CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            data DATE NOT NULL,
            quantidade REAL NOT NULL,
            valor REAL NOT NULL,
            FOREIGN KEY(ticker) REFERENCES fundos(ticker)
        )
    ''')

    conn.commit()

def import_proventos_two_months_ago(conn):
    """
    Insere os proventos de dois meses atrás (maio/2025) para os FIIs da carteira,
    usando valores obtidos via pesquisa em sites confiáveis.
    """
    from datetime import date, timedelta

    # Define mês e ano de dois meses atrás
    hoje = date.today()
    primeiro_mes = hoje.replace(day=1)
    mes_atrasado_date = primeiro_mes - timedelta(days=1)
    mes_atrasado_date = mes_atrasado_date.replace(day=1) - timedelta(days=1)
    ano, mes = mes_atrasado_date.year, mes_atrasado_date.month

    # Proventos de maio/2025 pesquisados
    proventos = {
        "MXRF11": 0.10,  # confirmado por Investidor10 e HubInvestor 1
        "BBRC11": 1.08,  # calendário XP mostrando R$1,08 2
        "BLMG11": 0.35,  # calendário XP mostrando R$0,35 3
        "BRCR11": 0.45,  # calendário XP mostrando R$0,45 4
        "GGRC11": 0.10,  # calendário XP mostrando R$0,10 5
        "HCTR11": 0.32,  # calendário XP mostrando R$0,32 6
        "KNCR11": 1.16,  # calendário XP mostrando R$1,16 7
        "MFII11": 1.10,  # calendário XP mostrando R$1,10 8
        "MXRF11": 0.10,
        "PLAG11": 0.46,  # calendário XP mostrando R$0,46 9
        "SARE11": 0.03,  # calendário XP mostrando R$0,03 10
        "VGHF11": 0.09,  # calendário XP mostrando R$0,09 11
        "VSLH11": 0.04,  # calendário XP mostrando R$0,04 12
        "XPSF11": 0.06,  # calendário XP mostrando R$0,06 13
    }

    c = conn.cursor()
    count = 0
    for ticker, valor in proventos.items():
        c.execute('''
            INSERT OR REPLACE INTO proventos (ticker, ano, mes, valor_cota)
            VALUES (?, ?, ?, ?)
        ''', (ticker, ano, mes, valor))
        count += 1

    conn.commit()
    print(f"✅ Inseridos/atualizados {count} proventos para {mes}/{ano} (dois meses atrás).")

def import_wallet(conn):
    dados_fiis = [  
        {"ticker": "BBRC11", "qty": 11, "total": 1102.53},  
        {"ticker": "BLMG11", "qty": 11, "total": 755.81},  
        {"ticker": "BRCR11", "qty": 25, "total": 1440.76},  
        {"ticker": "BTHF11", "qty": 70, "total": 788.02},  
        {"ticker": "GGRC11", "qty": 50, "total": 571.00},  
        {"ticker": "HCTR11", "qty": 15, "total": 1512.15},  
        {"ticker": "KNCR11", "qty": 5, "total": 492.10},  
        {"ticker": "MFII11", "qty": 15, "total": 1398.30},  
        {"ticker": "MXRF11", "qty": 250, "total": 2439.44},  
        {"ticker": "PLAG11", "qty": 35, "total": 1604.40},  
        {"ticker": "RZAT11", "qty": 15, "total": 1465.95},  
        {"ticker": "SARE11", "qty": 150, "total": 847.29},  
        {"ticker": "VGHF11", "qty": 260, "total": 2418.90},  
        {"ticker": "VSLH11", "qty": 200, "total": 1250.64},  
        {"ticker": "XPSF11", "qty": 100, "total": 650.25}  
    ]
    c = conn.cursor()
    for f in dados_fiis:
        c.execute('''
            INSERT OR IGNORE INTO fundos(ticker, qty, total_investido)
            VALUES(?, ?, ?)
        ''', (f['ticker'], f['qty'], f['total']))
    conn.commit()
    print("Carteira inicial importada.")


def add_fundo(conn, ticker, qty, total):
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM fundos WHERE ticker = ?", (ticker,))
    exists = c.fetchone()[0]

    if exists:
        c.execute("UPDATE fundos SET qty = ?, total_investido = ? WHERE ticker = ?", (qty, total, ticker))
        print(f"🔁 Fundo {ticker} atualizado.")
    else:
        c.execute("INSERT INTO fundos (ticker, qty, total_investido) VALUES (?, ?, ?)", (ticker, qty, total))
        print(f"✅ Fundo {ticker} inserido.")

    conn.commit()


def add_provento(conn, ticker, ano, mes, valor_cota):
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM proventos WHERE ticker = ? AND ano = ? AND mes = ?", (ticker, ano, mes))
    exists = c.fetchone()[0]

    if exists:
        c.execute("UPDATE proventos SET valor_cota = ? WHERE ticker = ? AND ano = ? AND mes = ?", (valor_cota, ticker, ano, mes))
        print(f"🔁 Provento {ticker} {mes}/{ano} atualizado.")
    else:
        c.execute("INSERT INTO proventos (ticker, ano, mes, valor_cota) VALUES (?, ?, ?, ?)", (ticker, ano, mes, valor_cota))
        print(f"✅ Provento {ticker} {mes}/{ano} inserido.")

    conn.commit()

def get_latest_proventos(conn):
    c = conn.cursor()
    c.execute('''
        SELECT p.ticker, p.valor_cota, f.qty, f.total_investido
        FROM proventos p
        JOIN fundos f USING(ticker)
        WHERE (p.ticker, p.ano, p.mes) IN (
            SELECT ticker, MAX(ano), MAX(mes)
            FROM proventos
            GROUP BY ticker
        )
    ''')
    return c.fetchall()


def report_individual(conn, ticker):
    c = conn.cursor()
    c.execute('SELECT * FROM fundos WHERE ticker = ?', (ticker,))
    fundo = c.fetchone()
    if not fundo:
        print("Fundo não encontrado.")
        return

    c.execute('''
        SELECT ano, mes, valor_cota
        FROM proventos
        WHERE ticker = ?
        ORDER BY ano DESC, mes DESC
        LIMIT 1
    ''', (ticker,))
    prov = c.fetchone()
    if not prov:
        print("Nenhum provento cadastrado para este fundo.")
        return

    valor_cota = prov['valor_cota']
    qty = fundo['qty']
    total_investido = fundo['total_investido']
    recebido_mensal = qty * valor_cota
    recebido_anual = recebido_mensal * 12
    rendimento_pct_mensal = (valor_cota / (total_investido / qty)) * 100
    meses_para_1_cota = (total_investido / qty) / recebido_mensal
    meses_para_return = total_investido / recebido_mensal

    print(f"--- Relatório para {ticker} ---")
    print(f"Quantidade de cotas: {qty}")
    print(f"Preço por cota (custo médio): {total_investido/qty:.2f}")
    print(f"Último provento: R$ {valor_cota:.4f}")
    print(f"Recebimento mensal: R$ {recebido_mensal:.2f}")
    print(f"Recebimento anual (proj.): R$ {recebido_anual:.2f}")
    print(f"Rendimento mensal (%): {rendimento_pct_mensal:.2f}%")
    print(f"Meses p/ comprar 1 cota: {meses_para_1_cota:.1f}")
    print(f"Meses p/ recuperar investimento: {meses_para_return:.1f}")

def report_all(conn):
    from tabulate import tabulate

    c = conn.cursor()

    # 1. Dados da carteira
    c.execute("SELECT ticker, qty, total_investido FROM fundos")
    fundos = {row[0]: {"qty": row[1], "total": row[2]} for row in c.fetchall()}

    # 2. Último provento por fundo
    
    c.execute("""
    SELECT ticker, AVG(valor_cota) as valor_medio
    FROM proventos
    GROUP BY ticker
    """)
    proventos = {row[0]: row[1] for row in c.fetchall()}
    
    '''
    c.execute("""
        SELECT ticker, valor_cota FROM proventos
        WHERE (ticker, ano, mes) IN (
            SELECT ticker, MAX(ano), MAX(mes)
            FROM proventos GROUP BY ticker
        )
    """)
    proventos = {row[0]: row[1] for row in c.fetchall()}
    '''

    # 3. Proventos acumulados
    c.execute("SELECT ticker, SUM(valor_cota) FROM proventos GROUP BY ticker")
    proventos_acumulados = {row[0]: row[1] for row in c.fetchall()}

    total_inv = 0.0
    total_rend_mensal = 0.0
    total_acumulado = 0.0
    tabela = []

    for ticker, dados in fundos.items():
        qty = dados["qty"]
        total = dados["total"]
        preco_medio = total / qty if qty > 0 else 0
        val_mes = proventos.get(ticker, 0.0)
        val_acumulado = proventos_acumulados.get(ticker, 0.0) * qty
        rendimento_mensal = val_mes * qty
        pct_mensal = (rendimento_mensal / total) * 100 if total else 0
        pct_acumulado = (val_acumulado / total) * 100 if total else 0
        payback_meses = total / rendimento_mensal if rendimento_mensal > 0 else float("inf")

        total_inv += total
        total_rend_mensal += rendimento_mensal
        total_acumulado += val_acumulado

        tabela.append([
            ticker,
            f"{qty:.1f}",
            f"R$ {preco_medio:.2f}",
            f"R$ {total:.2f}",
            f"R$ {rendimento_mensal:.2f}",
            f"{pct_mensal:.2f}%",
            f"R$ {val_acumulado:.2f}",
            f"{pct_acumulado:.2f}%",
            f"{payback_meses:.1f} meses" if payback_meses < float("inf") else "N/D"
        ])

    headers = [
        "Fundo", "Cotas", "Preço Médio", "Total Investido",
        "Rend. Mensal", "% Mensal", "Proventos Acum.", "% Acum.", "Payback"
    ]

    print("📊 Composição Atual da Carteira:")
    print(tabulate(tabela, headers=headers, tablefmt="grid"))

    total_pct_mensal = (total_rend_mensal / total_inv) * 100 if total_inv else 0
    total_pct_acumulado = (total_acumulado / total_inv) * 100 if total_inv else 0

    print("💼 Totais Consolidados:")
    print(f" - Total investido:         R$ {total_inv:.2f}")
    print(f" - Rendimento mensal atual: R$ {total_rend_mensal:.2f}")
    print(f" - Rendimento anual proj.:  R$ {total_rend_mensal * 12:.2f}")
    print(f" - % rendimento mensal:     {total_pct_mensal:.2f}%")
    print(f" - Proventos acumulados:    R$ {total_acumulado:.2f}")
    print(f" - % acumulado sobre total: {total_pct_acumulado:.2f}%")
    
def increment_month(year: int, month: int):
    if month == 12:
        return year + 1, 1
    return year, month + 1
    
def project_reinvestment(conn, target_rendimento):
    from datetime import date
    import math
    from calendar import month_name
    from tabulate import tabulate

    # Obtém dados atuais da carteira
    c = conn.cursor()
    c.execute("SELECT ticker, qty FROM fundos")
    fundos = {row[0]: row[1] for row in c.fetchall()}

    
    c.execute("""
    SELECT ticker, AVG(valor_cota) as valor_medio
    FROM proventos
    GROUP BY ticker
    """)
    proventos = {row[0]: row[1] for row in c.fetchall()}
    
    '''
    c.execute("""
        SELECT ticker, valor_cota FROM proventos
        WHERE (ticker, ano, mes) IN (
            SELECT ticker, MAX(ano), MAX(mes)
            FROM proventos GROUP BY ticker
        )
    """)
    proventos = {row[0]: row[1] for row in c.fetchall()}
    '''

    # Preço estimado por cota (valor total investido / qtd)
    c.execute("SELECT ticker, total_investido, qty FROM fundos")
    cotas_valores = {}
    for row in c.fetchall():
        ticker, total, qtd = row
        if qtd > 0:
            cotas_valores[ticker] = total / qtd

    saldo = 0.0
    meses = 0

    while True:
        meses += 1
        ganhos_mes = sum(fundos[ticker] * proventos.get(ticker, 0.0) for ticker in fundos)
        saldo += ganhos_mes

        for ticker in sorted(fundos, key=lambda t: t):
            preco_cota = cotas_valores.get(ticker)
            if preco_cota and saldo >= preco_cota:
                novas = math.floor(saldo / preco_cota)
                fundos[ticker] += novas
                saldo -= novas * preco_cota

        rendimento_projetado = sum(fundos[t] * proventos.get(t, 0.0) for t in fundos)
        if rendimento_projetado >= target_rendimento:
            break
        if meses > 360:
            print("⚠️ Projeção excedeu 30 anos. Meta pode ser inalcançável.")
            return

    final_month = (date.today().month + meses - 1) % 12 or 12
    final_year = date.today().year + ((date.today().month + meses - 1) // 12)

    print(f"📈 Meta de R$ {target_rendimento:.2f} de rendimento mensal atingida em {meses} meses ({month_name[final_month]}/{final_year}).")

    print("📊 Carteira final por fundo:")
    table = []
    total_mensal = 0.0
    for ticker in sorted(fundos):
        qtd = fundos[ticker]
        valor_cota = proventos.get(ticker, 0.0)
        rendimento_fundo = qtd * valor_cota
        total_mensal += rendimento_fundo
        table.append([ticker, f"{qtd:.1f}", f"R$ {valor_cota:.4f}", f"R$ {rendimento_fundo:.2f}"])

    print(tabulate(table, headers=["Fundo", "Cotas", "Rendimento/cota", "Rendimento total"], tablefmt="grid"))
    print(f"💰 Rendimento mensal projetado: R$ {total_mensal:.2f}")

def project_with_aporte(conn, target_rendimento, aporte_mensal):
    from datetime import date
    import math
    from calendar import month_name
    from tabulate import tabulate

    # Dados da carteira atual
    c = conn.cursor()
    c.execute("SELECT ticker, qty FROM fundos")
    fundos = {row[0]: row[1] for row in c.fetchall()}

    # Últimos proventos
    
    c.execute("""
    SELECT ticker, AVG(valor_cota) as valor_medio
    FROM proventos
    GROUP BY ticker
    """)
    proventos = {row[0]: row[1] for row in c.fetchall()}
    
    '''
    c.execute("""
        SELECT ticker, valor_cota FROM proventos
        WHERE (ticker, ano, mes) IN (
            SELECT ticker, MAX(ano), MAX(mes)
            FROM proventos GROUP BY ticker
        )
    """)
    proventos = {row[0]: row[1] for row in c.fetchall()}
  '''

    # Preço médio das cotas
    c.execute("SELECT ticker, total_investido, qty FROM fundos")
    cotas_valores = {}
    for row in c.fetchall():
        ticker, total, qtd = row
        if qtd > 0:
            cotas_valores[ticker] = total / qtd

    saldo = 0.0
    meses = 0

    while True:
        meses += 1
        ganhos_mes = sum(fundos[t] * proventos.get(t, 0.0) for t in fundos)
        saldo += ganhos_mes + aporte_mensal

        for ticker in sorted(fundos, key=lambda t: t):
            preco_cota = cotas_valores.get(ticker)
            if preco_cota and saldo >= preco_cota:
                novas = math.floor(saldo / preco_cota)
                fundos[ticker] += novas
                saldo -= novas * preco_cota

        rendimento_projetado = sum(fundos[t] * proventos.get(t, 0.0) for t in fundos)
        if rendimento_projetado >= target_rendimento:
            break

        if meses > 360:
            print("⚠️ Projeção ultrapassou 30 anos. Meta pode ser inalcançável.")
            return

    final_month = (date.today().month + meses - 1) % 12 or 12
    final_year = date.today().year + ((date.today().month + meses - 1) // 12)

    print(f"📈 Com aportes de R$ {aporte_mensal:.2f}/mês, você atinge R$ {target_rendimento:.2f} de rendimento mensal em {meses} meses ({month_name[final_month]}/{final_year}).")

    print("📊 Carteira final por fundo:")
    tabela = []
    total_rendimento = 0.0
    for ticker in sorted(fundos):
        qtd = fundos[ticker]
        valor_cota = proventos.get(ticker, 0.0)
        rendimento = qtd * valor_cota
        total_rendimento += rendimento
        tabela.append([ticker, f"{qtd:.1f}", f"R$ {valor_cota:.4f}", f"R$ {rendimento:.2f}"])

    print(tabulate(tabela, headers=["Fundo", "Cotas", "Rendimento/cota", "Rendimento total"], tablefmt="grid"))
    print(f"💰 Rendimento mensal projetado: R$ {total_rendimento:.2f}")

def project_best_yield(conn, target_rendimento, aporte_mensal):
    from datetime import date
    import math
    from calendar import month_name
    from tabulate import tabulate

    c = conn.cursor()

    # 1. Dados iniciais
    c.execute("SELECT ticker, qty FROM fundos")
    fundos = {row[0]: row[1] for row in c.fetchall()}
    
    c.execute("""
    SELECT ticker, AVG(valor_cota) as valor_medio
    FROM proventos
    GROUP BY ticker
    """)
    proventos = {row[0]: row[1] for row in c.fetchall()}
    
    '''
    c.execute("""
        SELECT ticker, valor_cota FROM proventos
        WHERE (ticker, ano, mes) IN (
            SELECT ticker, MAX(ano), MAX(mes)
            FROM proventos GROUP BY ticker
        )
    """)
    proventos = {row[0]: row[1] for row in c.fetchall()}
    '''

    c.execute("SELECT ticker, total_investido, qty FROM fundos")
    cotas_valores = {}
    for row in c.fetchall():
        ticker, total, qtd = row
        if qtd > 0:
            cotas_valores[ticker] = total / qtd

    saldo = 0.0
    meses = 0

    while True:
        meses += 1
        ganhos_mes = sum(fundos[t] * proventos.get(t, 0.0) for t in fundos)
        saldo += ganhos_mes + aporte_mensal

        # 3. Ordenar fundos por melhor rendimento relativo (eficiência)
        fundos_ranking = []
        for t in fundos:
            rendimento = proventos.get(t, 0.0)
            preco = cotas_valores.get(t)
            if rendimento > 0 and preco:
                eficiencia = rendimento / preco
                fundos_ranking.append((eficiencia, t))

        fundos_ranking.sort(reverse=True)

        # 4. Comprar cotas começando pelos mais eficientes
        for eficiencia, ticker in fundos_ranking:
            preco = cotas_valores[ticker]
            if saldo >= preco:
                qtd_novas = math.floor(saldo / preco)
                fundos[ticker] += qtd_novas
                saldo -= qtd_novas * preco

        rendimento_total = sum(fundos[t] * proventos.get(t, 0.0) for t in fundos)
        if rendimento_total >= target_rendimento:
            break

        if meses > 360:
            print("⚠️ Projeção passou de 30 anos. Meta talvez não seja atingível.")
            return

    final_month = (date.today().month + meses - 1) % 12 or 12
    final_year = date.today().year + ((date.today().month + meses - 1) // 12)

    print(f"\n🎯 Investindo nos FIIs mais rentáveis, você atinge R$ {target_rendimento:.2f}/mês em {meses} meses ({month_name[final_month]}/{final_year}).")

    print("📊 Carteira final por fundo:")
    tabela = []
    total_rendimento = 0.0
    for ticker in sorted(fundos):
        qtd = fundos[ticker]
        valor_cota = proventos.get(ticker, 0.0)
        rendimento = qtd * valor_cota
        total_rendimento += rendimento
        tabela.append([ticker, f"{qtd:.1f}", f"R$ {valor_cota:.4f}", f"R$ {rendimento:.2f}"])

    print(tabulate(tabela, headers=["Fundo", "Cotas", "Rendimento/cota", "Rendimento total"], tablefmt="grid"))
    print(f"💰 Rendimento mensal final projetado: R$ {total_rendimento:.2f}")

def report_resumo(conn):
    from tabulate import tabulate

    c = conn.cursor()

    c.execute("SELECT ticker, qty, total_investido FROM fundos")
    fundos = c.fetchall()
    
    c.execute("""
    SELECT ticker, AVG(valor_cota) as valor_medio
    FROM proventos
    GROUP BY ticker
    """)
    proventos = {row[0]: row[1] for row in c.fetchall()}
    
    '''
    c.execute("""
        SELECT ticker, valor_cota FROM proventos
        WHERE (ticker, ano, mes) IN (
            SELECT ticker, MAX(ano), MAX(mes)
            FROM proventos GROUP BY ticker
        )
    """)
    proventos = {row[0]: row[1] for row in c.fetchall()}
    '''


    analise = []
    for ticker, qty, total in fundos:
        valor_cota = proventos.get(ticker, 0.0)
        if qty == 0 or total == 0:
            continue
        rendimento = valor_cota * qty
        rendimento_pct = (rendimento / total) * 100
        analise.append({
            "ticker": ticker,
            "qty": qty,
            "total": total,
            "valor_cota": valor_cota,
            "rendimento": rendimento,
            "retorno_pct": rendimento_pct
        })

    if not analise:
        print("Nenhum dado válido para análise.")
        return

    melhor = max(analise, key=lambda x: x['retorno_pct'])
    pior = min(analise, key=lambda x: x['retorno_pct'])
    mais_cotas = max(analise, key=lambda x: x['qty'])
    menos_cotas = min(analise, key=lambda x: x['qty'])
    maior_inv = max(analise, key=lambda x: x['total'])
    menor_inv = min(analise, key=lambda x: x['total'])

    tabela = [
        ["Melhor retorno (%)", melhor['ticker'], f"{melhor['retorno_pct']:.2f}%"],
        ["Pior retorno (%)", pior['ticker'], f"{pior['retorno_pct']:.2f}%"],
        ["Mais cotas", mais_cotas['ticker'], f"{mais_cotas['qty']:.1f}"],
        ["Menos cotas", menos_cotas['ticker'], f"{menos_cotas['qty']:.1f}"],
        ["Maior investimento", maior_inv['ticker'], f"R$ {maior_inv['total']:.2f}"],
        ["Menor investimento", menor_inv['ticker'], f"R$ {menor_inv['total']:.2f}"]
    ]

    print("📊 Resumo da Carteira:")
    print(tabulate(tabela, headers=["Métrica", "Fundo", "Valor"], tablefmt="grid"))

def report_movimentacoes_fundos(conn):
    from tabulate import tabulate
    c = conn.cursor()

    c.execute("""
        SELECT ticker, strftime('%Y-%m', data), SUM(valor * quantidade)
        FROM compras
        GROUP BY ticker, strftime('%Y-%m', data)
        ORDER BY ticker, data
    """)
    rows = c.fetchall()

    if not rows:
        print("Nenhuma movimentação encontrada.")
        return

    tabela = []
    totais = {}

    for ticker, mes, valor in rows:
        tabela.append([ticker, mes, f"R$ {valor:.2f}"])
        totais[ticker] = totais.get(ticker, 0) + valor

    print("📅 Movimentações Mensais por Fundo:")
    print(tabulate(tabela, headers=["Fundo", "Mês", "Valor Investido"], tablefmt="grid"))

    print("📊 Total Investido por Fundo:")
    total_table = [[t, f"R$ {v:.2f}"] for t, v in totais.items()]
    print(tabulate(total_table, headers=["Fundo", "Total"], tablefmt="grid"))

def report_movimentacoes_proventos(conn):
    from tabulate import tabulate
    c = conn.cursor()

    c.execute("""
        SELECT ticker, ano, mes, valor_cota
        FROM proventos
        ORDER BY ticker, ano, mes
    """)
    rows = c.fetchall()

    if not rows:
        print("Nenhum provento cadastrado.")
        return

    tabela = []
    totais_mensais = {}
    totais_anuais = {}

    for ticker, ano, mes, valor in rows:
        chave_mes = f"{ano}-{mes:02}"
        chave_ano = f"{ano}"
        totais_mensais[chave_mes] = totais_mensais.get(chave_mes, 0) + valor
        totais_anuais[chave_ano] = totais_anuais.get(chave_ano, 0) + valor
        tabela.append([ticker, chave_mes, f"R$ {valor:.4f}"])

    print("📅 Proventos por Fundo e Mês:")
    print(tabulate(tabela, headers=["Fundo", "Mês", "Valor por Cota"], tablefmt="grid"))

    print("📊 Total de Proventos por Ano:")
    tabela_ano = [[ano, f"R$ {valor:.2f}"] for ano, valor in sorted(totais_anuais.items())]
    print(tabulate(tabela_ano, headers=["Ano", "Total"], tablefmt="grid"))

def main():

    parser = argparse.ArgumentParser(description='FiI Provisor de Rendimentos')
    sub = parser.add_subparsers(dest='cmd')

    # Inicialização
    sub.add_parser('init', help='Inicializa o banco e importa carteira inicial')
    sub.add_parser('fetch_two_months', help='Importa proventos de dois meses atrás')

    # Adição de dados
    p_addf = sub.add_parser('add_fundo', help='Cadastra ou atualiza um fundo')
    p_addf.add_argument('ticker')
    p_addf.add_argument('qty', type=float)
    p_addf.add_argument('total', type=float)

    p_addp = sub.add_parser('add_provento', help='Adiciona ou atualiza provento mensal')
    p_addp.add_argument('ticker')
    p_addp.add_argument('ano', type=int)
    p_addp.add_argument('mes', type=int)
    p_addp.add_argument('valor_cota', type=float)

    # Relatórios
    p_ri = sub.add_parser('report_ind', help='Relatório individual de um fundo')
    p_ri.add_argument('ticker')

    sub.add_parser('report_all', help='Relatório consolidado da carteira')
    sub.add_parser('report_resumo', help='Resumo tabulado com destaques de desempenho')
    sub.add_parser('report_mov_fundos', help='Movimentações mensais e totais dos fundos')
    sub.add_parser('report_mov_proventos', help='Proventos mensais e anuais dos fundos')

    # Projeções
    p_proj = sub.add_parser('project', help='Projeção com reinvestimento até meta')
    p_proj.add_argument('target', type=float, help='Meta de rendimento mensal')

    p_proj_aporte = sub.add_parser('project_aporte', help='Projeção com reinvestimento + aporte mensal')
    p_proj_aporte.add_argument('target', type=float)
    p_proj_aporte.add_argument('aporte', type=float)

    p_proj_best = sub.add_parser('project_melhor', help='Projeção investindo nos FIIs mais rentáveis')
    p_proj_best.add_argument('target', type=float)
    p_proj_best.add_argument('aporte', type=float)

    # Execução
    args = parser.parse_args()
    conn = connect()

    if args.cmd == 'init':
        init_db(conn)
        import_wallet(conn)

    elif args.cmd == 'fetch_two_months':
        import_proventos_two_months_ago(conn)

    elif args.cmd == 'add_fundo':
        add_fundo(conn, args.ticker.upper(), args.qty, args.total)

    elif args.cmd == 'add_provento':
        add_provento(conn, args.ticker.upper(), args.ano, args.mes, args.valor_cota)

    elif args.cmd == 'report_ind':
        report_individual(conn, args.ticker.upper())

    elif args.cmd == 'report_all':
        report_all(conn)

    elif args.cmd == 'report_resumo':
        report_resumo(conn)

    elif args.cmd == 'report_mov_fundos':
        report_movimentacoes_fundos(conn)

    elif args.cmd == 'report_mov_proventos':
        report_movimentacoes_proventos(conn)

    elif args.cmd == 'project':
        project_reinvestment(conn, args.target)

    elif args.cmd == 'project_aporte':
        project_with_aporte(conn, args.target, args.aporte)

    elif args.cmd == 'project_melhor':
        project_best_yield(conn, args.target, args.aporte)

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
    
    
"""

python fiiprovisor.py init
python fiiprovisor.py add_fundo MXRF11 100 1000.00
python fiiprovisor.py add_provento MXRF11 2025 7 0.10
python fiiprovisor.py report_all
python fiiprovisor.py report_ind MXRF11
python fiiprovisor.py report_resumo
python fiiprovisor.py report_mov_fundos
python fiiprovisor.py report_mov_proventos
python fiiprovisor.py project 200
python fiiprovisor.py project_aporte 200 300
python fiiprovisor.py project_melhor 200 300


python fiiprovisor.py init

python fiiprovisor.py fetch_two_months
python fiiprovisor.py add_provento RZAT11 2025 5 0.90
python fiiprovisor.py add_provento BTHF11 2025 5 0.12

"""    