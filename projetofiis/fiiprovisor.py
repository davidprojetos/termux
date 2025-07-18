#!/usr/bin/env python3
# fiiprovisor.py

import sys
import sqlite3
import argparse
from datetime import date, timedelta
from calendar import month_name

DB_FILE = 'fiis.db'



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
        "RZAT11": 0.90,  # calendário XP mostrando R$0,90 9
        "BTHF11": 0.12,  # calendário XP mostrando R$0,12 10
        "PLAG11": 0.46,  # calendário XP mostrando R$0,46 11
        "SARE11": 0.03,  # calendário XP mostrando R$0,03 12
        "VGHF11": 0.09,  # calendário XP mostrando R$0,09 13
        "VSLH11": 0.04,  # calendário XP mostrando R$0,04 14
        "XPSF11": 0.06,  # calendário XP mostrando R$0,06 15
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
    count = 0
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
        count += 1

    conn.commit()
    print(f"Carteira inicial importada com {count} fundos.")

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

def atualizar_provento(conn, id_mov, novo_ano, novo_mes, novo_valor):
    c = conn.cursor()
    c.execute('''
        UPDATE proventos
        SET ano = ?, mes = ?, valor_cota = ?
        WHERE id = ?
    ''', (novo_ano, novo_mes, novo_valor, id_mov))
    conn.commit()
    print(f"✅ Provento ID {id_mov} atualizado com sucesso.")

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

    # 1. Carteira estática atual (só para custo médio / total geral)
    c.execute("SELECT ticker, total_investido, qty FROM fundos")
    fundos = {r['ticker']: {'total': r['total_investido'], 'qty': r['qty']} for r in c.fetchall()}

    # 2. Últimos proventos por mês
    c.execute("""
        SELECT ticker, ano, mes, valor_cota
        FROM proventos
        ORDER BY ticker, ano DESC, mes DESC
    """)
    provs = {}
    for r in c.fetchall():
        provs.setdefault(r['ticker'], []).append((r['ano'], r['mes'], r['valor_cota']))

    tabela = []
    tot_inv = tot_recv = 0.0

    for ticker, info in fundos.items():
        total = info['total']
        preco_medio = total / info['qty'] if info['qty'] else 0

        if ticker not in provs:
            continue
        ano, mes, valor_cota = provs[ticker][0]  # mais recente
        qty_ate = get_qty_ate(conn, ticker, ano, mes)
        recebido = qty_ate * valor_cota

        pct = (recebido / total * 100) if total else 0

        tabela.append([
            ticker,
            f"{info['qty']:.1f}",
            f"R$ {preco_medio:.2f}",
            f"{ano}-{mes:02}",
            f"{qty_ate:.1f}",
            f"R$ {valor_cota:.4f}",
            f"R$ {recebido:.2f}",
            f"{pct:.2f}% - {(pct*12):.2f}%/12"
        ])
        tot_inv += total
        tot_recv += recebido

    headers = ["Fundo","Cotas","Preço Méd.","Últ Provento","Qtd Até Mês",
               "Valor/Cota","Recebido","% s/ Invest"]
    print("📊 Carteira Atualizada com Cálculo Dinâmico de Proventos")
    print(tabulate(tabela, headers=headers, tablefmt="grid"))
    print(f"Total Investido: R$ {tot_inv:.2f}  |  Recebimento Último Mês: R$ {tot_recv:.2f}")

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

    # 1️⃣ Movimentações mensais por fundo
    c.execute("""
        SELECT ticker, strftime('%Y-%m', data) as mes, SUM(valor * quantidade) as total
        FROM compras
        GROUP BY ticker, mes
        ORDER BY ticker, mes
    """)
    rows = c.fetchall()

    if not rows:
        print("Nenhuma movimentação encontrada.")
        return

    tabela = []
    for ticker, mes, valor in rows:
        tabela.append([ticker, mes, f"R$ {valor:.2f}"])

    print("📅 Movimentações Mensais por Fundo:")
    print(tabulate(tabela, headers=["Fundo", "Mês", "Valor Investido"], tablefmt="grid"))

    # 2️⃣ Total por fundo direto do SQL
    c.execute("""
        SELECT ticker, SUM(valor * quantidade) as total
        FROM compras
        GROUP BY ticker
        ORDER BY ticker
    """)
    total_rows = c.fetchall()
    total_table = [[ticker, f"R$ {total:.2f}"] for ticker, total in total_rows]
    print("📊 Total Investido por Fundo:")
    print(tabulate(total_table, headers=["Fundo", "Total"], tablefmt="grid"))

    # 3️⃣ Total geral também direto do SQL (sem somar no Python!)
    c.execute("""
        SELECT SUM(valor * quantidade) FROM compras
    """)
    soma_total = c.fetchone()[0]
    print(f"\n💰 Total Geral Investido em Todos os Fundos: R$ {soma_total:.2f}")

def report_movimentacoes_proventos(conn):
    from tabulate import tabulate

    c = conn.cursor()
    c.execute("SELECT DISTINCT ticker FROM proventos")
    tickers = [r['ticker'] for r in c.fetchall()]

    tabela = []
    for ticker in tickers:
        provs = c.execute("""
            SELECT ano, mes, valor_cota
            FROM proventos
            WHERE ticker = ?
            ORDER BY ano, mes
        """, (ticker,)).fetchall()
        for r in provs:
            ano, mes, valor_cota = r['ano'], r['mes'], r['valor_cota']
            qty_ate = get_qty_ate(conn, ticker, ano, mes)
            recebido = qty_ate * valor_cota
            tabela.append([
                ticker,
                f"{ano}-{mes:02}",
                f"{qty_ate:.1f}",
                f"R$ {valor_cota:.4f}",
                f"R$ {recebido:.2f}"
            ])

    headers = ["Fundo","Mês","Qtd Até Mês","Valor/Cota","Recebido"]
    print("📅 Histórico de Proventos (Dinâmico)")
    print(tabulate(tabela, headers=headers, tablefmt="grid"))

def add_compra(conn, ticker, data, quantidade, valor_unitario):
    c = conn.cursor()
    ticker = ticker.upper()

    valor_total = quantidade * valor_unitario

    # Insere a nova compra na tabela de compras
    c.execute('''
    INSERT INTO compras (ticker, data, quantidade, qtd_disponivel, valor)
    VALUES (?, ?, ?, ?, ?)
    ''', (ticker, data, quantidade, quantidade, valor_total))

    # Verifica se o fundo já existe
    c.execute('SELECT qty, total_investido FROM fundos WHERE ticker = ?', (ticker,))
    row = c.fetchone()

    if row:
        # Quantidade e valor acumulados do fundo
        quantidade_atual = row['qty']
        total_atual = row['total_investido']

        # Soma de todas as compras do fundo, até a data da nova compra (inclusive)
        c.execute('''
            SELECT SUM(quantidade) AS soma_qty, SUM(valor) AS soma_valor
            FROM compras
            WHERE ticker = ? AND data <= ?
        ''', (ticker, data))
        acumulado = c.fetchone()

        nova_qty = acumulado['soma_qty'] or 0
        novo_total = acumulado['soma_valor'] or 0

        # Só atualiza se a nova soma for maior que a atual
        if nova_qty > quantidade_atual:
            c.execute('''
                UPDATE fundos SET qty = ?, total_investido = ? WHERE ticker = ?
            ''', (nova_qty, novo_total, ticker))
            print(f"🛒 Compra registrada e fundo {ticker} atualizado.")
        else:
            print(f"🛒 Compra registrada, mas fundo {ticker} **não atualizado** (compra passada ou já contabilizada).")
    else:
        # Fundo ainda não existe, cria novo com a primeira compra
        c.execute('''
            INSERT INTO fundos (ticker, qty, total_investido)
            VALUES (?, ?, ?)
        ''', (ticker, quantidade, valor_total))
        print(f"🆕 Compra registrada e fundo {ticker} criado.")

    conn.commit()

def atualizar_compra(conn, id_mov, nova_data, nova_quantidade, novo_valor):
    c = conn.cursor()

    # Descobre qual é o ticker dessa compra
    c.execute('SELECT ticker FROM compras WHERE id = ?', (id_mov,))
    row = c.fetchone()
    if not row:
        print(f"❌ Compra ID {id_mov} não encontrada.")
        return

    ticker = row['ticker']

    # Atualiza a compra
    c.execute('''
        UPDATE compras
        SET data = ?, quantidade = ?, valor = ?
        WHERE id = ?
    ''', (nova_data, nova_quantidade, novo_valor, id_mov))
    conn.commit()

    # Recalcula o fundo
    recalcular_fundo(conn, ticker)
    print(f"✅ Compra ID {id_mov} atualizada e fundo {ticker} recalculado.")

def add_venda(conn, ticker, data, quantidade, valor_total):
    from decimal import Decimal
    c = conn.cursor()
    ticker = ticker.upper()

    # Busca as compras FIFO com saldo disponível
    c.execute('''
        SELECT id, quantidade, valor, qtd_disponivel
        FROM compras
        WHERE ticker = ? AND qtd_disponivel > 0
        ORDER BY data, id
    ''', (ticker,))
    compras = c.fetchall()

    qtd_restante = quantidade
    valor_investido_proporcional = Decimal('0.00')

    for comp in compras:
        if qtd_restante <= 0:
            break

        qtd_disp = comp['qtd_disponivel']
        if qtd_disp == 0:
            continue

        usar = min(qtd_disp, qtd_restante)
        preco_unit = Decimal(comp['valor']) / Decimal(comp['quantidade'])
        valor_investido_proporcional += preco_unit * Decimal(usar)
        nova_disponivel = qtd_disp - usar

        # Atualiza apenas qtd_disponivel
        c.execute('''
            UPDATE compras
            SET qtd_disponivel = ?
            WHERE id = ?
        ''', (nova_disponivel, comp['id']))

        qtd_restante -= usar

    if qtd_restante > 0:
        print(f"❌ Venda não registrada: tentando vender mais cotas ({quantidade}) do que possui.")
        conn.rollback()
        return

    # Insere a venda
    c.execute('''
        INSERT INTO vendas (ticker, data, quantidade, valor)
        VALUES (?, ?, ?, ?)
    ''', (ticker, data, quantidade, valor_total))

    # Atualiza o fundo com base em qtd_disponivel e valor proporcional
    c.execute('''
        SELECT SUM(qtd_disponivel) AS soma_qty,
               SUM((valor / quantidade) * qtd_disponivel) AS soma_valor
        FROM compras
        WHERE ticker = ?
    ''', (ticker,))
    row = c.fetchone()
    nova_qtd = row['soma_qty'] or 0
    novo_total = row['soma_valor'] or 0.0

    c.execute('''
        UPDATE fundos SET qty = ?, total_investido = ? WHERE ticker = ?
    ''', (nova_qtd, novo_total, ticker))

    conn.commit()
    print(f"💸 Venda registrada, cotas ajustadas e fundo {ticker} atualizado.")

def atualizar_venda(conn, id_mov, nova_data, nova_quantidade, novo_valor):
    c = conn.cursor()

    # Descobre qual é o ticker dessa venda
    c.execute('SELECT ticker FROM vendas WHERE id = ?', (id_mov,))
    row = c.fetchone()
    if not row:
        print(f"❌ Venda ID {id_mov} não encontrada.")
        return

    ticker = row['ticker']

    # Atualiza a venda
    c.execute('''
        UPDATE vendas
        SET data = ?, quantidade = ?, valor = ?
        WHERE id = ?
    ''', (nova_data, nova_quantidade, novo_valor, id_mov))
    conn.commit()

    # Recalcula o fundo
    recalcular_fundo(conn, ticker)
    print(f"✅ Venda ID {id_mov} atualizada e fundo {ticker} recalculado.")
    
def recalcular_fundo(conn, ticker):
    c = conn.cursor()
    ticker = ticker.upper()

    c.execute('''
        SELECT SUM(quantidade) AS qty, SUM(valor * 1.0) AS total
        FROM compras
        WHERE ticker = ?
    ''', (ticker,))
    row = c.fetchone()

    nova_qtd = row['qty'] or 0
    novo_total = row['total'] or 0.0

    c.execute('''
        UPDATE fundos SET qty = ?, total_investido = ? WHERE ticker = ?
    ''', (nova_qtd, novo_total, ticker))

    conn.commit()
    print(f"🔁 Fundo {ticker} recalculado.")

def reportar_pendencias_compras(conn):
    from tabulate import tabulate

    c = conn.cursor()

    # Dados consolidados da tabela fundos
    c.execute("SELECT ticker, qty AS qty_fundo, total_investido FROM fundos")
    dados_fundos = {row['ticker']: {'qty': row['qty_fundo'], 'total': row['total_investido']} for row in c.fetchall()}

    # Soma das compras por fundo
    c.execute('''
        SELECT ticker, SUM(quantidade) AS qty_compras, SUM(valor) AS total_compras
        FROM compras
        GROUP BY ticker
    ''')
    compras = {row['ticker']: {'qty': row['qty_compras'] or 0, 'total': row['total_compras'] or 0} for row in c.fetchall()}

    # Unir todos os tickers
    tickers = sorted(set(dados_fundos.keys()).union(compras.keys()))

    tabela = []
    inconsistentes = False

    for ticker in tickers:
        qty_f = dados_fundos.get(ticker, {}).get('qty', 0)
        total_f = dados_fundos.get(ticker, {}).get('total', 0)

        qty_c = compras.get(ticker, {}).get('qty', 0)
        total_c = compras.get(ticker, {}).get('total', 0)

        diff_qty = qty_c - qty_f
        diff_total = total_c - total_f

        alerta = ''
        if abs(diff_qty) > 0.001 or abs(diff_total) > 0.01:
            alerta = '⚠️'
            inconsistentes = True

        tabela.append([
            ticker,
            f"{qty_f:.2f}", f"R$ {total_f:.2f}",
            f"{qty_c:.2f}", f"R$ {total_c:.2f}",
            f"{diff_qty:+.2f}", f"R$ {diff_total:+.2f}",
            alerta
        ])

    headers = [
        "Fundo",
        "Qtd. (fundos)", "Total (fundos)",
        "Qtd. (compras)", "Total (compras)",
        "Δ Qtd.", "Δ Valor",
        "Status"
    ]

    print("🔍 Verificação de Pendências entre Compras e Fundos:")
    print(tabulate(tabela, headers=headers, tablefmt="grid"))

    if inconsistentes:
        print("⚠️  Há divergências entre os dados de compras e o total registrado em 'fundos'. Verifique!")
    else:
        print("✅ Todos os fundos estão consistentes com os registros de compras.")

def reportar_pendencias_proventos(conn):
    from datetime import date
    from calendar import monthrange
    from tabulate import tabulate

    c = conn.cursor()

    # 1) Lista de FIIs com data da primeira compra
    c.execute("""
      SELECT ticker, MIN(data) AS primeira_compra
      FROM compras
      GROUP BY ticker
    """)
    primeiros = {row['ticker']: row['primeira_compra'] for row in c.fetchall()}

    # 2) Todos os proventos registrados
    c.execute("SELECT ticker, ano, mes, valor_cota FROM proventos")
    provs = {}
    for row in c.fetchall():
        key = (row['ticker'], row['ano'], row['mes'])
        provs.setdefault(row['ticker'], {})[(row['ano'], row['mes'])] = row['valor_cota']

    hoje = date.today()
    pendencias = []
    for ticker, primeira in primeiros.items():
        ano0, mes0 = map(int, primeira.split('-')[:2])
        ano, mes = ano0, mes0

        # itera mês a mês até mês/ano atuais
        while (ano, mes) <= (hoje.year, hoje.month):
            # só verifica a partir do mês seguinte à compra
            if (ano, mes) != (ano0, mes0):
                if (ticker not in provs) or ((ano, mes) not in provs[ticker]):
                    pendencias.append([ticker, f"{ano}-{mes:02}", "Falta provento", "⚠️"])
            # incrementa mês
            if mes == 12:
                ano += 1
                mes = 1
            else:
                mes += 1

    # Monta relatório
    if not pendencias:
        print("✅ Nenhuma pendência de proventos encontrada.")
        return

    headers = ["Fundo", "Mês", "Observação", "Status"]
    print("🔍 Pendências de Proventos Desde a Primeira Compra:")
    print(tabulate(pendencias, headers=headers, tablefmt="grid"))

def get_qty_ate(conn, ticker, ano, mes):
    c = conn.cursor()
    # último dia do mês
    ultimo = date(ano, mes, 1).replace(
        day=month_name.__len__()  # substituir pela forma correta de obter último dia
    )
    # mas SQLite não tem monthrange; usamos string <= “YYYY-MM-31”
    lim = f"{ano}-{mes:02}-31"
    c.execute("""
        SELECT SUM(quantidade) AS qty
        FROM compras
        WHERE ticker = ?
          AND data <= ?
    """, (ticker, lim))
    row = c.fetchone()
    return row['qty'] or 0.0

def report_historico_movimentacoes(conn, ticker=None):
    from tabulate import tabulate
    c = conn.cursor()

    if ticker:
        ticker = ticker.upper()
        query = '''
            SELECT id, ticker, data, 'Compra' AS tipo, quantidade, valor / quantidade AS valor_unitario, valor
            FROM compras
            WHERE ticker = ?
            UNION ALL
            SELECT id, ticker, data, 'Venda' AS tipo, quantidade, valor / quantidade AS valor_unitario, valor
            FROM vendas
            WHERE ticker = ?
            ORDER BY data
        '''
        params = (ticker, ticker)
    else:
        query = '''
            SELECT id, ticker, data, 'Compra' AS tipo, quantidade, valor / quantidade AS valor_unitario, valor
            FROM compras
            UNION ALL
            SELECT id, ticker, data, 'Venda' AS tipo, quantidade, valor / quantidade AS valor_unitario, valor
            FROM vendas
            ORDER BY ticker, data
        '''
        params = ()

    c.execute(query, params)
    rows = c.fetchall()

    if not rows:
        print("Nenhuma movimentação registrada.")
        return

    tabela = []
    for r in rows:
        tabela.append([
            r['id'],
            r['ticker'],
            r['data'],
            r['tipo'],
            f"{r['quantidade']:.2f}",
            f"R$ {r['valor_unitario']:.2f}" if r['valor_unitario'] is not None else "—",
            f"R$ {r['valor']:.2f}"
        ])

    headers = ["ID", "Fundo", "Data", "Tipo", "Quantidade", "Valor Unitário", "Valor Total"]
    print("📜 Histórico de Compras e Vendas:")
    print(tabulate(tabela, headers=headers, tablefmt="grid"))

def calcular_reducao_preco_medio_para_ultimo_preco(conn):
    c = conn.cursor()

    # Obtém todos os fundos registrados
    c.execute("SELECT ticker, qty, total_investido FROM fundos")
    fundos = c.fetchall()

    if not fundos:
        print("Nenhum fundo encontrado na base de dados.")
        return

    print("\n=== Análise de Redução de Preço Médio ===")

    for fundo in fundos:
        ticker = fundo["ticker"]
        qtd_atual = fundo["qty"]
        total_investido = fundo["total_investido"]
        preco_medio = total_investido / qtd_atual

        # Pega o preço da última compra (mais recente) do fundo
        c.execute("""
            SELECT valor, quantidade FROM compras 
            WHERE ticker = ? 
            ORDER BY data DESC, id DESC LIMIT 1
        """, (ticker,))
        ultima_compra = c.fetchone()

        if not ultima_compra:
            print(f"{ticker}: Sem histórico de compras.")
            continue

        preco_ultima_compra = ultima_compra["valor"] / ultima_compra["quantidade"]

        if preco_ultima_compra >= preco_medio:
            print(f"{ticker}: Preço atual R$ {preco_ultima_compra:.2f} >= preço médio R$ {preco_medio:.2f}. Nenhuma ação necessária.")
            continue

        # Calcula quantas cotas precisam ser compradas ao preço da última compra
        qtd_necessaria = (qtd_atual * (preco_medio - preco_ultima_compra)) / preco_ultima_compra
        novo_total_investido = total_investido + (qtd_necessaria * preco_ultima_compra)
        nova_qtd = qtd_atual + qtd_necessaria
        novo_preco_medio = novo_total_investido / nova_qtd

        print(f"\n{ticker}:")
        print(f"- Preço médio atual: R$ {preco_medio:.2f}")
        print(f"- Preço da última compra: R$ {preco_ultima_compra:.2f}")
        print(f"- Para ajustar o preço médio para R$ {preco_ultima_compra:.2f}, você precisa comprar ~{qtd_necessaria:.2f} cotas")
        print(f"- Novo preço médio após compra: R$ {novo_preco_medio:.2f}")

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

    # Tabela de compras (agora com qtd_disponivel)
    c.execute('''
        CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            data DATE NOT NULL,
            quantidade REAL NOT NULL,
            qtd_disponivel REAL NOT NULL,
            valor REAL NOT NULL,
            FOREIGN KEY(ticker) REFERENCES fundos(ticker)
        )
    ''')

    # Tabela de vendas
    c.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            data DATE NOT NULL,
            quantidade REAL NOT NULL,
            valor REAL NOT NULL,  -- valor total da venda, não por cota
            FOREIGN KEY(ticker) REFERENCES fundos(ticker)
        )
    ''')

    conn.commit()

def menu_interativo(conn):
    while True:
        print("\n=== MENU FIIs ===")
        print("1. Inicializar base de dados")
        print("2. Importar proventos (2 meses)")
        print("3. Adicionar fundo")
        print("4. Adicionar provento")
        print("5. Relatório individual")
        print("6. Relatório consolidado")
        print("7. Relatório resumo")
        print("8. Movimentações de fundos")
        print("9. Movimentações de proventos")
        print("10. Projeção simples")
        print("11. Projeção com aporte")
        print("12. Projeção melhor investimento")
        print("13. Adicionar compra")
        print("14. Adicionar venda")
        print("15. Verificar pendências")
        print("16. Verificar pendências de proventos")
        print("17. Histórico de movimentações")
        print("18. Atualizar movimentação (provento, compra ou venda)")
        print("19. Calcular cotas para reduzir preço médio")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            init_db(conn)
            import_wallet(conn)
        elif opcao == "2":
            import_proventos_two_months_ago(conn)
        elif opcao == "3":
            ticker = input("Ticker: ").upper()
            qty = float(input("Quantidade: "))
            total = float(input("Valor total: "))
            add_fundo(conn, ticker, qty, total)
        elif opcao == "4":
            ticker = input("Ticker: ").upper()
            ano = int(input("Ano: "))
            mes = int(input("Mês: "))
            valor = float(input("Valor por cota: "))
            add_provento(conn, ticker, ano, mes, valor)
        elif opcao == "5":
            ticker = input("Ticker: ").upper()
            report_individual(conn, ticker)
        elif opcao == "6":
            report_all(conn)
        elif opcao == "7":
            report_resumo(conn)
        elif opcao == "8":
            report_movimentacoes_fundos(conn)
        elif opcao == "9":
            report_movimentacoes_proventos(conn)
        elif opcao == "10":
            target = float(input("Meta de rendimento mensal: "))
            project_reinvestment(conn, target)
        elif opcao == "11":
            target = float(input("Meta: "))
            aporte = float(input("Aporte mensal: "))
            project_with_aporte(conn, target, aporte)
        elif opcao == "12":
            target = float(input("Meta: "))
            aporte = float(input("Aporte mensal: "))
            project_best_yield(conn, target, aporte)
        elif opcao == "13":
            ticker = input("Ticker: ").upper()
            data = input("Data (YYYY-MM-DD): ")
            quantidade = float(input("Quantidade: "))
            valor = float(input("Valor total: "))
            add_compra(conn, ticker, data, quantidade, valor)
        elif opcao == "14":
            ticker = input("Ticker: ").upper()
            data = input("Data (YYYY-MM-DD): ")
            quantidade = float(input("Quantidade: "))
            valor = float(input("Valor total: "))
            add_venda(conn, ticker, data, quantidade, valor)
        elif opcao == "15":
            reportar_pendencias_compras(conn)
        elif opcao == "16":
            reportar_pendencias_proventos(conn)
        elif opcao == "17":
            ticker = input("Ticker (opcional, Enter para todos): ").upper()
            if not ticker:
                ticker = None
            report_historico_movimentacoes(conn, ticker)
        elif opcao == "18":
            print("\nQual tipo deseja atualizar?")
            print("1. Provento")
            print("2. Compra")
            print("3. Venda")
            tipo = input("Escolha: ")

            id_mov = int(input("ID da movimentação: "))

            if tipo == "1":
                novo_valor = float(input("Novo valor por cota: "))
                atualizar_provento(conn, id_mov, novo_valor)
            elif tipo == "2":
                nova_data = input("Nova data (YYYY-MM-DD): ")
                nova_qtd = float(input("Nova quantidade: "))
                novo_valor = float(input("Novo valor total: "))
                atualizar_compra(conn, id_mov, nova_data, nova_qtd, novo_valor)
            elif tipo == "3":
                nova_data = input("Nova data (YYYY-MM-DD): ")
                nova_qtd = float(input("Nova quantidade: "))
                novo_valor = float(input("Novo valor total: "))
                atualizar_venda(conn, id_mov, nova_data, nova_qtd, novo_valor)
            else:
                print("Tipo inválido.")
        
        elif opcao == "19":
          calcular_reducao_preco_medio_para_ultimo_preco(conn)
        
        
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

def main():
    conn = connect()

    # Exibe menu interativo se nenhum argumento for passado
    if len(sys.argv) == 1:
        menu_interativo(conn)
        return

    parser = argparse.ArgumentParser(description='FiI Provisor de Rendimentos')
    sub = parser.add_subparsers(dest='cmd', required=True)

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

    sub.add_parser('report_all', help='Relatório consolidado (dinâmico proventos)')
    sub.add_parser('report_resumo', help='Resumo tabulado com destaques de desempenho')
    sub.add_parser('report_mov_fundos', help='Movimentações mensais e totais dos fundos')
    sub.add_parser('report_mov_proventos', help='Histórico de proventos (dinâmico)')

    # Projeções
    p_proj = sub.add_parser('project', help='Projeção com reinvestimento até meta')
    p_proj.add_argument('target', type=float)

    p_proj_aporte = sub.add_parser('project_aporte', help='Projeção com reinvestimento + aporte mensal')
    p_proj_aporte.add_argument('target', type=float)
    p_proj_aporte.add_argument('aporte', type=float)

    p_proj_best = sub.add_parser('project_melhor', help='Projeção investindo nos FIIs mais rentáveis')
    p_proj_best.add_argument('target', type=float)
    p_proj_best.add_argument('aporte', type=float)

    # Adição de compra
    p_addc = sub.add_parser('add_compra', help='Adiciona uma nova compra de FII')
    p_addc.add_argument('ticker')
    p_addc.add_argument('data')
    p_addc.add_argument('quantidade', type=float)
    p_addc.add_argument('valor', type=float)

    # Adição de venda
    p_addv = sub.add_parser('add_venda', help='Adiciona uma nova venda de FII')
    p_addv.add_argument('ticker')
    p_addv.add_argument('data')
    p_addv.add_argument('quantidade', type=float)
    p_addv.add_argument('valor', type=float)

    # Verificações
    sub.add_parser('check_pendencias', help='Verifica inconsistências entre compras e dados dos fundos')
    sub.add_parser('check_pendencias_proventos', help='Verifica meses sem proventos desde a 1ª compra')

    p_rhvi = sub.add_parser('report_hist_mov', help='Mostra o histórico completo de compras e vendas')
    p_rhvi.add_argument('--ticker', help='Ticker do fundo (opcional)')

    args = parser.parse_args()

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
    elif args.cmd == 'add_compra':
        add_compra(conn, args.ticker, args.data, args.quantidade, args.valor)
    elif args.cmd == 'add_venda':
        add_venda(conn, args.ticker, args.data, args.quantidade, args.valor)
    elif args.cmd == 'check_pendencias':
        reportar_pendencias_compras(conn)
    elif args.cmd == 'check_pendencias_proventos':
        reportar_pendencias_proventos(conn)
    elif args.cmd == 'report_hist_mov':
        report_historico_movimentacoes(conn, args.ticker)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()




"""

# Rodando os comandos de exemplo

python fiiprovisor.py report_all
python fiiprovisor.py report_ind MXRF11
python fiiprovisor.py report_hist_mov
python fiiprovisor.py report_hist_mov --ticker MXRF11
python fiiprovisor.py report_resumo
python fiiprovisor.py report_mov_fundos
python fiiprovisor.py report_mov_proventos
python fiiprovisor.py project 200
python fiiprovisor.py project_aporte 200 300
python fiiprovisor.py project_melhor 200 300
python fiiprovisor.py check_pendencias
python fiiprovisor.py check_pendencias_proventos

#Modificadores de dados

rm -rf fiis.db
python fiiprovisor.py init

python fiiprovisor.py fetch_two_months

python fiiprovisor.py add_compra MXRF11 2025-07-08 10 99.50

python fiiprovisor.py add_fundo MXRF11 100 1000.00

python fiiprovisor.py add_provento MXRF11 2025 7 0.10


# Operações validas de compras: 

python fiiprovisor.py add_compra BBRC11 2022-10-18 5  100.00
python fiiprovisor.py add_compra BBRC11 2022-10-04 5  101.93
python fiiprovisor.py add_compra BBRC11 2023-02-13 1  92.88

python fiiprovisor.py add_compra BLMG11 2023-07-19 2  68.29
python fiiprovisor.py add_compra BLMG11 2023-07-10 2  68.00
python fiiprovisor.py add_compra BLMG11 2023-06-19 1  68.00
python fiiprovisor.py add_compra BLMG11 2023-06-05 3  66.72
python fiiprovisor.py add_compra BLMG11 2023-01-25 3  71.69

python fiiprovisor.py add_compra BRCR11 2022-12-19 5  57.84
python fiiprovisor.py add_compra BRCR11 2022-11-25 4  59.58
python fiiprovisor.py add_compra BRCR11 2022-11-18 1  62.40
python fiiprovisor.py add_compra BRCR11 2022-08-29 7  66.05
python fiiprovisor.py add_compra BRCR11 2022-07-29 3  55.06
python fiiprovisor.py add_compra BRCR11 2023-02-16 1  54.31
python fiiprovisor.py add_compra BRCR11 2025-07-08 4  42.25

python fiiprovisor.py add_compra BTHF11 2024-12-01 70 11.257428571

python fiiprovisor.py add_compra GGRC11 2022-08-29 50  11.42

python fiiprovisor.py add_compra HCTR11 2022-11-25 2  98.85
python fiiprovisor.py add_compra HCTR11 2022-11-04 2  102.685
python fiiprovisor.py add_compra HCTR11 2022-09-29 5  103.04
python fiiprovisor.py add_compra HCTR11 2023-01-24 6  98.98

python fiiprovisor.py add_compra KNCR11 2023-01-25 5  98.42

python fiiprovisor.py add_compra MFII11 2023-04-24 5  88.68
python fiiprovisor.py add_compra MFII11 2023-01-24 10  95.49

python fiiprovisor.py add_compra MXRF11 2022-12-22 2  9.89
python fiiprovisor.py add_compra MXRF11 2022-12-19 22  9.83
python fiiprovisor.py add_compra MXRF11 2022-11-29 11  10.04
python fiiprovisor.py add_compra MXRF11 2022-11-25 7  10.05
python fiiprovisor.py add_compra MXRF11 2022-11-23 38  10.10
python fiiprovisor.py add_compra MXRF11 2022-11-11 1  10.25
python fiiprovisor.py add_compra MXRF11 2022-11-10 1  10.26
python fiiprovisor.py add_compra MXRF11 2022-10-28 1  10.25
python fiiprovisor.py add_compra MXRF11 2022-10-26 1  10.25
python fiiprovisor.py add_compra MXRF11 2022-10-18 2  10.29
python fiiprovisor.py add_compra MXRF11 2022-09-30 1  10.27
python fiiprovisor.py add_compra MXRF11 2022-08-24 43 10.02
python fiiprovisor.py add_compra MXRF11 2022-08-03 2  9.78
python fiiprovisor.py add_compra MXRF11 2022-07-21 5  9.74
python fiiprovisor.py add_compra MXRF11 2023-12-01 31 9.082903226
python fiiprovisor.py add_compra MXRF11 2024-10-31 8  9.60
python fiiprovisor.py add_compra MXRF11 2024-10-16 9  9.79
python fiiprovisor.py add_compra MXRF11 2024-09-05 15  10.01
python fiiprovisor.py add_compra MXRF11 2025-06-23 10  9.36
python fiiprovisor.py add_compra MXRF11 2025-06-11 20  9.40
python fiiprovisor.py add_compra MXRF11 2025-07-08 20  9.48

python fiiprovisor.py add_compra PLAG11 2022-12-29 2  42.93
python fiiprovisor.py add_compra PLAG11 2022-11-11 7  46.82
python fiiprovisor.py add_compra PLAG11 2022-09-21 8  46.586
python fiiprovisor.py add_compra PLAG11 2022-09-15 3  46.79
python fiiprovisor.py add_compra PLAG11 2022-08-29 2  46.58
python fiiprovisor.py add_compra PLAG11 2022-08-26 4  46.46
python fiiprovisor.py add_compra PLAG11 2022-08-25 1  46.47
python fiiprovisor.py add_compra PLAG11 2022-08-11 1  45.53
python fiiprovisor.py add_compra PLAG11 2022-07-29 4  45.45
python fiiprovisor.py add_compra PLAG11 2023-04-27 1  42.56
python fiiprovisor.py add_compra PLAG11 2023-03-20 2  41.19

python fiiprovisor.py add_compra RZAT11 2024-07-01 12  99.3225
python fiiprovisor.py add_compra RZAT11 2024-07-01 03  91.36

python fiiprovisor.py add_compra SARE11 2024-07-01 145 5.684068966
python fiiprovisor.py add_compra SARE11 2025-07-08 5 4.62

python fiiprovisor.py add_compra VGHF11 2022-12-05 11  9.05
python fiiprovisor.py add_compra VGHF11 2022-12-01 11  9.03
python fiiprovisor.py add_compra VGHF11 2022-11-11 19  9.32
python fiiprovisor.py add_compra VGHF11 2022-11-04 8  9.38
python fiiprovisor.py add_compra VGHF11 2022-10-18 22  9.35
python fiiprovisor.py add_compra VGHF11 2022-09-21 3  9.87
python fiiprovisor.py add_compra VGHF11 2022-09-20 3  9.86
python fiiprovisor.py add_compra VGHF11 2022-09-16 12  9.83
python fiiprovisor.py add_compra VGHF11 2022-09-15 10  9.88
python fiiprovisor.py add_compra VGHF11 2022-08-22 6  9.802
python fiiprovisor.py add_compra VGHF11 2022-08-16 24  9.79
python fiiprovisor.py add_compra VGHF11 2022-08-11 11  9.765
python fiiprovisor.py add_compra VGHF11 2022-08-03 15  9.78
python fiiprovisor.py add_compra VGHF11 2022-07-21 4  9.88
python fiiprovisor.py add_compra VGHF11 2023-12-13 5  9.24
python fiiprovisor.py add_compra VGHF11 2023-12-05 3  9.23
python fiiprovisor.py add_compra VGHF11 2023-11-14 4  9.31
python fiiprovisor.py add_compra VGHF11 2023-08-03 8  9.45
python fiiprovisor.py add_compra VGHF11 2023-07-31 2  9.56
python fiiprovisor.py add_compra VGHF11 2023-06-19 7  9.27
python fiiprovisor.py add_compra VGHF11 2023-06-05 3  9.29
python fiiprovisor.py add_compra VGHF11 2023-04-12 2  8.79
python fiiprovisor.py add_compra VGHF11 2024-06-18 4  8.82
python fiiprovisor.py add_compra VGHF11 2024-04-04 4  9.09
python fiiprovisor.py add_compra VGHF11 2023-03-20 2  9.07
python fiiprovisor.py add_compra VGHF11 2023-03-15 1  9.05
python fiiprovisor.py add_compra VGHF11 2023-02-27 6  9.09
python fiiprovisor.py add_compra VGHF11 2023-02-16 5  9.00
python fiiprovisor.py add_compra VGHF11 2023-02-13 15  9.02
python fiiprovisor.py add_compra VGHF11 2023-02-06 14  9.01
python fiiprovisor.py add_compra VGHF11 2024-06-18 4  8.82
python fiiprovisor.py add_compra VGHF11 2024-04-04 4  9.09
python fiiprovisor.py add_compra VGHF11 2025-06-10 5  7.63
python fiiprovisor.py add_compra VGHF11 2025-07-08 5  7.75

python fiiprovisor.py add_compra VSLH11 2022-07-21 5  9.20
python fiiprovisor.py add_compra VSLH11 2023-08-23 4  3.88
python fiiprovisor.py add_compra VSLH11 2023-08-16 3  3.99
python fiiprovisor.py add_compra VSLH11 2023-08-10 12  3.93
python fiiprovisor.py add_compra VSLH11 2023-07-31 1  4.29
python fiiprovisor.py add_compra VSLH11 2023-07-19 1  4.67
python fiiprovisor.py add_compra VSLH11 2023-07-17 10  4.76
python fiiprovisor.py add_compra VSLH11 2023-06-05 1  5.41
python fiiprovisor.py add_compra VSLH11 2023-03-24 5  6.95
python fiiprovisor.py add_compra VSLH11 2023-03-20 1  7.12
python fiiprovisor.py add_compra VSLH11 2023-03-15 4  6.97
python fiiprovisor.py add_compra VSLH11 2023-01-25 100 8.74
python fiiprovisor.py add_compra VSLH11 2025-06-11 8  2.94
python fiiprovisor.py add_compra VSLH11 2025-07-08 50 2.93

python fiiprovisor.py add_compra XPSF11 2022-12-23 2  7.14
python fiiprovisor.py add_compra XPSF11 2022-12-19 15  7.08
python fiiprovisor.py add_compra XPSF11 2022-12-12 4  7.23
python fiiprovisor.py add_compra XPSF11 2022-12-05 1  7.23
python fiiprovisor.py add_compra XPSF11 2022-08-29 6  7.57
python fiiprovisor.py add_compra XPSF11 2022-08-26 19  7.58
python fiiprovisor.py add_compra XPSF11 2022-08-11 12  7.01
python fiiprovisor.py add_compra XPSF11 2022-08-03 16  7.058
python fiiprovisor.py add_compra XPSF11 2022-07-21 7  7.01
python fiiprovisor.py add_compra XPSF11 2023-04-24 50  6.92
python fiiprovisor.py add_compra XPSF11 2023-01-13 8  7.18
python fiiprovisor.py add_compra XPSF11 2023-01-10 13  7.20
python fiiprovisor.py add_compra XPSF11 2025-06-25 15  6.10
python fiiprovisor.py add_compra XPSF11 2025-07-08 5  6.07
python fiiprovisor.py add_compra XPSF11 2025-07-09 30  6.08

"""    

"""


python fiiprovisor.py add_venda MXRF11 2023-01-25 2 10.07

python fiiprovisor.py add_venda RECT11 2023-01-24 35 52.355

python fiiprovisor.py add_venda XPSF11 2023-01-24 103 7.40

"""