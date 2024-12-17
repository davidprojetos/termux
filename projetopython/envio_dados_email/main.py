import sqlite3
from davidsousa import enviar_email

def converter_para_sql(items):
    sql_commands = []
    for item in items:
        if isinstance(item, dict):
            item_name = item['item'].replace("'", "''")
            item_id = item['id']
            item_sql = f"INSERT INTO item (id, item) VALUES ({item_id}, '{item_name}');"
            sql_commands.append(item_sql)
    return "\n".join(sql_commands)

def obter_dados():
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, item FROM item")
    rows = cursor.fetchall()

    items = []
    for row in rows:
        item = {'id': row[0], 'item': row[1]}
        items.append(item)

    conn.close()
    return items

def main():
    items = obter_dados()
    sql_data = converter_para_sql(items)

    nome_remetente = "David Sousa - backup items"
    remetente = "davidk1k3kk@gmail.com"
    senha = "pfqlcemdaotxppiw"
    destinatarios = ["davidk1k3k@gmail.com"]
    assunto = "Dados exemplo de dados"

    for destinatario in destinatarios:
        corpo = f"<h1>Dados em formato SQL</h1><pre>{sql_data}</pre>"
        print(corpo)
        #enviar_email(nome_remetente, remetente, senha, destinatario, assunto, corpo, importante=True, html=True)

if __name__ == "__main__":
    main()