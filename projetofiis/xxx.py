import sqlite3
from datetime import datetime

# Cores fixas (sem repetições)
CATEGORY_COLORS = {
    'Espiritual': 'CYAN',
    'Acadêmico': 'BLUE',
    'Profissional': 'YELLOW',
    'Relacionamento': 'MAGENTA',
    'Lazer': 'GREEN',
    'Pessoal': 'RED',
}

# Categorias e atividades padrão
DEFAULT_ACTIVITIES = {
    'Espiritual': [
        "Estudar a Bíblia",
        "Estudar a lição da Escola Sabatina",
        "Ir à igreja"
    ],
    'Acadêmico': [
        "Estudar na universidade",
        "Estudar livros",
        "Ler livros novos",
        "Ler artigos",
        "Fazer cursos livres",
        "Estudar marketing",
        "Estudar marketing digital"
    ],
    'Profissional': [
        "Trabalhar",
        "Estagiar",
        "Verificar vagas de estágio",
        "Verificar e-mails",
        "Verificar tendências",
        "Utilizar sistemas",
        "Testar sistemas",
        "Desenvolver sistemas",
        "Desenvolver aplicativos"
    ],
    'Relacionamento': [
        "Interagir com a namorada"
    ],
    'Lazer': [
        "Assistir séries",
        "Assistir filmes",
        "Assistir vídeos no YouTube",
        "Assistir vídeos no Instagram"
    ],
    'Pessoal': [
        "Treinar",
        "Fazer compras",
        "Verificar boletos atrasados",
        "Construir minha casa"
    ]
}

# Conectar ao banco de dados
conn = sqlite3.connect('life.db')
cursor = conn.cursor()

def get_category_id(name, color):
    cursor.execute('SELECT id FROM categories WHERE name = ?', (name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    cursor.execute('INSERT INTO categories (name, color) VALUES (?, ?)', (name, color))
    conn.commit()
    return cursor.lastrowid

def create_activity_if_not_exists(name, category_id):
    cursor.execute('SELECT id FROM activities WHERE name = ?', (name,))
    if not cursor.fetchone():
        cursor.execute('INSERT INTO activities (name, category_id) VALUES (?, ?)', (name, category_id))
        print(f'Atividade adicionada: {name}')
        conn.commit()

def import_defaults():
    for category, activities in DEFAULT_ACTIVITIES.items():
        color = CATEGORY_COLORS[category]
        category_id = get_category_id(category, color)
        for activity in activities:
            create_activity_if_not_exists(activity, category_id)

if __name__ == '__main__':
    import_defaults()
    conn.close()
    print("\n✅ Categorias e atividades padrão importadas com sucesso!")
