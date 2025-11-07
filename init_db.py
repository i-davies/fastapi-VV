"""
Script de inicialização do banco de dados SQLite
"""

import sqlite3
import os

# Caminho do banco de dados
DB_PATH = "database.db"


def criar_banco():
    """Cria o banco de dados e tabelas"""

    # Remover banco existente
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Banco {DB_PATH} removido")

    # Criar conexão
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Criar tabela de usuários
    cursor.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            active INTEGER DEFAULT 1
        )
    """
    )

    # Criar tabela de produtos
    cursor.execute(
        """
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            category TEXT
        )
    """
    )

    # Criar tabela de pedidos
    cursor.execute(
        """
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            total REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    """
    )

    print("Tabelas criadas com sucesso!")

    # Popular dados de exemplo
    popular_dados(cursor)

    # Commit e fechar
    conn.commit()
    conn.close()
    print(f"\nBanco de dados '{DB_PATH}' criado com sucesso!")


def popular_dados(cursor):
    """Insere dados de exemplo"""

    # Usuários
    usuarios = [
        ("admin", "admin123", "admin@example.com", "admin", 1),
        ("joao", "senha123", "joao@example.com", "user", 1),
        ("maria", "maria456", "maria@example.com", "user", 1),
        ("pedro", "pedro789", "pedro@example.com", "user", 1),
        ("ana", "ana2024", "ana@example.com", "user", 0),
    ]

    cursor.executemany(
        "INSERT INTO users (username, password, email, role, active) VALUES (?, ?, ?, ?, ?)",
        usuarios,
    )
    print(f"✓ {len(usuarios)} usuários inseridos")

    # Produtos
    produtos = [
        (
            "Notebook Dell",
            "Notebook 15 polegadas, 8GB RAM",
            3500.00,
            10,
            "Eletrônicos",
        ),
        ("Mouse Logitech", "Mouse sem fio", 85.00, 50, "Eletrônicos"),
        ("Teclado Mecânico", "Teclado RGB", 450.00, 25, "Eletrônicos"),
        ("Livro Python", "Aprenda Python em 30 dias", 59.90, 100, "Livros"),
        ("Cadeira Gamer", "Cadeira ergonômica", 1200.00, 15, "Móveis"),
        ("Webcam HD", "Webcam 1080p", 280.00, 30, "Eletrônicos"),
        ("Headset Gamer", "Headset com microfone", 320.00, 20, "Eletrônicos"),
    ]

    cursor.executemany(
        "INSERT INTO products (name, description, price, stock, category) VALUES (?, ?, ?, ?, ?)",
        produtos,
    )
    print(f"✓ {len(produtos)} produtos inseridos")

    # Pedidos
    pedidos = [
        (2, 1, 1, 3500.00, "completed"),
        (3, 2, 2, 170.00, "completed"),
        (2, 4, 3, 179.70, "pending"),
        (4, 3, 1, 450.00, "completed"),
        (3, 5, 1, 1200.00, "shipped"),
    ]

    cursor.executemany(
        "INSERT INTO orders (user_id, product_id, quantity, total, status) VALUES (?, ?, ?, ?, ?)",
        pedidos,
    )
    print(f"✓ {len(pedidos)} pedidos inseridos")


if __name__ == "__main__":
    print("=" * 60)
    print("Iniciando criação do banco de dados...")
    print("=" * 60)
    criar_banco()
    print("=" * 60)
