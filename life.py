#!/usr/bin/env python3
# life.py

import sqlite3
from datetime import datetime
from colorama import Fore, Style, init

# Inicializa colorama
init(autoreset=True)

# Conexão e criação de tabelas
conn = sqlite3.connect('life.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        color TEXT UNIQUE NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        category_id INTEGER NOT NULL,
        FOREIGN KEY(category_id) REFERENCES categories(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        activity_id INTEGER NOT NULL,
        time_spent INTEGER NOT NULL,        -- minutos
        rating INTEGER NOT NULL CHECK(rating BETWEEN 0 AND 10),
        description TEXT,
        date TEXT NOT NULL,
        FOREIGN KEY(activity_id) REFERENCES activities(id)
    )
''')

conn.commit()

# Mapa de nomes de cores válidas para Fore.<COLOR>
COLOR_OPTIONS = {
    'BLACK': Fore.BLACK,
    'RED': Fore.RED,
    'GREEN': Fore.GREEN,
    'YELLOW': Fore.YELLOW,
    'BLUE': Fore.BLUE,
    'MAGENTA': Fore.MAGENTA,
    'CYAN': Fore.CYAN,
    'WHITE': Fore.WHITE
}

def get_used_colors():
    cursor.execute('SELECT color FROM categories')
    return {row[0] for row in cursor.fetchall()}

def choose_color():
    used = get_used_colors()
    avail = {name: code for name, code in COLOR_OPTIONS.items() if name not in used}
    if not avail:
        print("Nenhuma cor disponível.")
        return None
    print("Cores disponíveis:")
    for i, name in enumerate(avail, 1):
        print(f"{i}. {avail[name]}{name}{Style.RESET_ALL}")
    escolha = input("Escolha o número da cor: ").strip()
    try:
        idx = int(escolha) - 1
        key = list(avail.keys())[idx]
        return key
    except:
        print("Escolha inválida.")
        return None

def colorize(text, color_name):
    code = COLOR_OPTIONS.get(color_name, '')
    return f"{code}{text}{Style.RESET_ALL}"

# --- CRUD CATEGORIES ---
def list_categories():
    cursor.execute('SELECT id, name, color FROM categories')
    rows = cursor.fetchall()
    if not rows:
        print("Nenhuma categoria cadastrada.")
    else:
        print("\nCategorias:")
        for id_, name, color in rows:
            print(f"{id_}. {colorize(name, color)} ({color})")

def create_category():
    name = input("Nome da nova categoria: ").strip()
    color = choose_color()
    if not color: return
    try:
        cursor.execute('INSERT INTO categories(name, color) VALUES(?,?)', (name, color))
        conn.commit()
        print("Categoria criada.")
    except sqlite3.IntegrityError:
        print("Nome ou cor já em uso.")

def update_category():
    list_categories()
    cid = input("ID da categoria a alterar: ").strip()
    cursor.execute('SELECT name, color FROM categories WHERE id=?', (cid,))
    row = cursor.fetchone()
    if not row:
        print("Categoria não encontrada.")
        return
    new_name = input(f"Novo nome [{row[0]}]: ").strip() or row[0]
    print("Escolhendo nova cor (ou Enter para manter)...")
    new_color = choose_color() or row[1]
    try:
        cursor.execute('UPDATE categories SET name=?, color=? WHERE id=?',
                       (new_name, new_color, cid))
        conn.commit()
        print("Categoria atualizada.")
    except sqlite3.IntegrityError:
        print("Nome ou cor já em uso.")

def delete_category():
    list_categories()
    cid = input("ID da categoria a excluir: ").strip()
    # verifica registros vinculados
    cursor.execute('''
        SELECT COUNT(*) FROM records r
        JOIN activities a ON r.activity_id = a.id
        WHERE a.category_id = ?
    ''', (cid,))
    if cursor.fetchone()[0] > 0:
        print("Não é possível excluir: há registros vinculados.")
        return
    cursor.execute('DELETE FROM categories WHERE id=?', (cid,))
    conn.commit()
    print("Categoria excluída.")

# --- CRUD ACTIVITIES ---
def list_activities():
    cursor.execute('''
        SELECT a.id, a.name, c.name, c.color
        FROM activities a
        JOIN categories c ON a.category_id = c.id
    ''')
    rows = cursor.fetchall()
    if not rows:
        print("Nenhuma atividade cadastrada.")
    else:
        print("\nAtividades:")
        for id_, name, cat, color in rows:
            print(f"{id_}. {colorize(name, color)} [{colorize(cat, color)}]")

def create_activity():
    name = input("Nome da nova atividade: ").strip()
    list_categories()
    cid = input("ID da categoria: ").strip()
    cursor.execute('SELECT id FROM categories WHERE id=?', (cid,))
    if not cursor.fetchone():
        print("Categoria inválida.")
        return
    try:
        cursor.execute('INSERT INTO activities(name, category_id) VALUES(?,?)',
                       (name, cid))
        conn.commit()
        print("Atividade criada.")
    except sqlite3.IntegrityError:
        print("Nome já existente.")

def update_activity():
    list_activities()
    aid = input("ID da atividade a alterar: ").strip()
    cursor.execute('SELECT name, category_id FROM activities WHERE id=?', (aid,))
    row = cursor.fetchone()
    if not row:
        print("Atividade não encontrada.")
        return
    new_name = input(f"Novo nome [{row[0]}]: ").strip() or row[0]
    list_categories()
    new_cid = input(f"Nova categoria ID [{row[1]}]: ").strip() or str(row[1])
    cursor.execute('SELECT id FROM categories WHERE id=?', (new_cid,))
    if not cursor.fetchone():
        print("Categoria inválida.")
        return
    try:
        cursor.execute('UPDATE activities SET name=?, category_id=? WHERE id=?',
                       (new_name, new_cid, aid))
        conn.commit()
        print("Atividade atualizada.")
    except sqlite3.IntegrityError:
        print("Nome já existente.")

def delete_activity():
    list_activities()
    aid = input("ID da atividade a excluir: ").strip()
    cursor.execute('SELECT COUNT(*) FROM records WHERE activity_id=?', (aid,))
    if cursor.fetchone()[0] > 0:
        print("Não é possível excluir: há registros vinculados.")
        return
    cursor.execute('DELETE FROM activities WHERE id=?', (aid,))
    conn.commit()
    print("Atividade excluída.")

# --- CRUD RECORDS ---
def list_records():
    cursor.execute('''
        SELECT r.id, a.name, r.time_spent, r.rating, r.description, r.date
        FROM records r
        JOIN activities a ON r.activity_id = a.id
        ORDER BY r.date DESC
    ''')
    rows = cursor.fetchall()
    if not rows:
        print("Nenhum registro encontrado.")
    else:
        print("\nRegistros:")
        for id_, act, time_spent, rating, desc, date in rows:
            print(f"{id_}. [{date}] {act} – {time_spent}min, nota {rating}, \"{desc}\"")

def create_record():
    list_activities()
    aid = input("ID da atividade para registrar: ").strip()
    cursor.execute('SELECT id FROM activities WHERE id=?', (aid,))
    if not cursor.fetchone():
        print("Atividade inválida.")
        return
    try:
        t = int(input("Tempo gasto (minutos): ").strip())
        rating = int(input("Classificação (0-10): ").strip())
        desc = input("Descrição: ").strip()
    except ValueError:
        print("Entrada inválida.")
        return
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO records(activity_id, time_spent, rating, description, date)
        VALUES(?,?,?,?,?)
    ''', (aid, t, rating, desc, date))
    conn.commit()
    print("Registro criado.")

def update_record():
    list_records()
    rid = input("ID do registro a alterar: ").strip()
    cursor.execute('SELECT activity_id, time_spent, rating, description FROM records WHERE id=?', (rid,))
    row = cursor.fetchone()
    if not row:
        print("Registro não encontrado.")
        return
    list_activities()
    new_aid = input(f"Nova atividade ID [{row[0]}]: ").strip() or str(row[0])
    try:
        new_t = int(input(f"Novo tempo [{row[1]}]: ").strip() or row[1])
        new_rating = int(input(f"Nova nota [{row[2]}]: ").strip() or row[2])
        new_desc = input(f"Nova descrição [{row[3]}]: ").strip() or row[3]
    except ValueError:
        print("Entrada inválida.")
        return
    cursor.execute('''
        UPDATE records
        SET activity_id=?, time_spent=?, rating=?, description=?
        WHERE id=?
    ''', (new_aid, new_t, new_rating, new_desc, rid))
    conn.commit()
    print("Registro atualizado.")

def delete_record():
    list_records()
    rid = input("ID do registro a excluir: ").strip()
    cursor.execute('DELETE FROM records WHERE id=?', (rid,))
    conn.commit()
    print("Registro excluído.")

# --- RELATÓRIOS ---
def report_activities_summary():
    print("\n--- RELATÓRIOS ---")
    print("1. Tempo total por categoria")
    print("2. Classificação média por categoria")
    print("3. Atividades mais bem classificadas")
    print("4. Atividades com mais tempo investido")
    print("5. Registros com maior tempo")
    print("6. Registros com maior nota")
    print("7. Resumo geral por atividade")
    print("8. Voltar")
    
    escolha = input("Escolha o relatório: ").strip()
    if escolha == "1":
        cursor.execute('''
            SELECT c.name, c.color, COALESCE(SUM(r.time_spent), 0)
            FROM categories c
            JOIN activities a ON a.category_id = c.id
            LEFT JOIN records r ON r.activity_id = a.id
            GROUP BY c.id
            ORDER BY SUM(r.time_spent) DESC
        ''')
        print("\nTempo total por categoria:")
        for nome, cor, total in cursor.fetchall():
            h, m = divmod(total, 60)
            print(colorize(f"{nome}: {h}h{m:02d}", cor))

    elif escolha == "2":
        cursor.execute('''
            SELECT c.name, c.color, AVG(r.rating)
            FROM categories c
            JOIN activities a ON a.category_id = c.id
            JOIN records r ON r.activity_id = a.id
            GROUP BY c.id
            ORDER BY AVG(r.rating) DESC
        ''')
        print("\nClassificação média por categoria:")
        for nome, cor, avg in cursor.fetchall():
            print(colorize(f"{nome}: média {avg:.2f}", cor))

    elif escolha == "3":
        cursor.execute('''
            SELECT a.name, c.color, AVG(r.rating)
            FROM activities a
            JOIN categories c ON a.category_id = c.id
            JOIN records r ON r.activity_id = a.id
            GROUP BY a.id
            HAVING COUNT(r.id) >= 1
            ORDER BY AVG(r.rating) DESC
            LIMIT 10
        ''')
        print("\nTop 10 atividades por nota:")
        for nome, cor, avg in cursor.fetchall():
            print(colorize(f"{nome}: média {avg:.2f}", cor))

    elif escolha == "4":
        cursor.execute('''
            SELECT a.name, c.color, SUM(r.time_spent)
            FROM activities a
            JOIN categories c ON a.category_id = c.id
            JOIN records r ON r.activity_id = a.id
            GROUP BY a.id
            ORDER BY SUM(r.time_spent) DESC
            LIMIT 10
        ''')
        print("\nTop 10 atividades por tempo:")
        for nome, cor, total in cursor.fetchall():
            h, m = divmod(total, 60)
            print(colorize(f"{nome}: {h}h{m:02d}", cor))

    elif escolha == "5":
        cursor.execute('''
            SELECT r.id, a.name, r.time_spent, r.date, c.color
            FROM records r
            JOIN activities a ON a.id = r.activity_id
            JOIN categories c ON c.id = a.category_id
            ORDER BY r.time_spent DESC
            LIMIT 10
        ''')
        print("\nTop 10 registros com mais tempo:")
        for rid, aname, t, date, cor in cursor.fetchall():
            h, m = divmod(t, 60)
            print(colorize(f"#{rid} {aname} - {h}h{m:02d} ({date})", cor))

    elif escolha == "6":
        cursor.execute('''
            SELECT r.id, a.name, r.rating, r.date, c.color
            FROM records r
            JOIN activities a ON a.id = r.activity_id
            JOIN categories c ON c.id = a.category_id
            ORDER BY r.rating DESC
            LIMIT 10
        ''')
        print("\nTop 10 registros com maior nota:")
        for rid, aname, rating, date, cor in cursor.fetchall():
            print(colorize(f"#{rid} {aname} - Nota {rating} ({date})", cor))

    elif escolha == "7":
        cursor.execute('''
            SELECT a.id, a.name, c.color,
                   COALESCE(SUM(r.time_spent),0),
                   AVG(r.rating)
            FROM activities a
            JOIN categories c ON a.category_id=c.id
            LEFT JOIN records r ON r.activity_id = a.id
            GROUP BY a.id, a.name, c.color
        ''')
        print("\nResumo geral por atividade:")
        for aid, name, color, total_time, avg_rating in cursor.fetchall():
            hrs = total_time // 60
            mins = total_time % 60
            avg = f"{avg_rating:.1f}" if avg_rating is not None else "N/A"
            line = f"{aid}. {name} – {hrs}h{mins:02d} (média nota {avg})"
            print(colorize(line, color))

    elif escolha == "8":
        return

    else:
        print("Opção inválida.")
# --- MENUS ---
def menu_categories():
    while True:
        print("\n--- CATEGORIES ---")
        print("1. Listar")
        print("2. Criar")
        print("3. Atualizar")
        print("4. Excluir")
        print("5. Voltar")
        op = input("Opção: ").strip()
        if op == "1": list_categories()
        elif op == "2": create_category()
        elif op == "3": update_category()
        elif op == "4": delete_category()
        elif op == "5": break

def menu_activities():
    while True:
        print("\n--- ACTIVITIES ---")
        print("1. Listar")
        print("2. Criar")
        print("3. Atualizar")
        print("4. Excluir")
        print("5. Voltar")
        op = input("Opção: ").strip()
        if op == "1": list_activities()
        elif op == "2": create_activity()
        elif op == "3": update_activity()
        elif op == "4": delete_activity()
        elif op == "5": break

def menu_records():
    while True:
        print("\n--- RECORDS ---")
        print("1. Listar")
        print("2. Criar")
        print("3. Atualizar")
        print("4. Excluir")
        print("5. Voltar")
        op = input("Opção: ").strip()
        if op == "1": list_records()
        elif op == "2": create_record()
        elif op == "3": update_record()
        elif op == "4": delete_record()
        elif op == "5": break

def main_menu():
    while True:
        print("\n" + Fore.WHITE + "==== SISTEMA LIFE ====")
        print("1. Gerenciar Categorias")
        print("2. Gerenciar Atividades")
        print("3. Gerenciar Registros")
        print("4. Relatório de Atividades")
        print("5. Sair")
        escolha = input("Escolha uma opção: ").strip()
        if escolha == "1": menu_categories()
        elif escolha == "2": menu_activities()
        elif escolha == "3": menu_records()
        elif escolha == "4": report_activities_summary()
        elif escolha == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    try:
        main_menu()
    finally:
        conn.close()