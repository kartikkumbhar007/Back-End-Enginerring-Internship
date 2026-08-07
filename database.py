import sqlite3


def get_connection():
    return sqlite3.connect("tasks.db")


def create_table():
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed BOOLEAN NOT NULL
            )
        """)

        connection.commit()


def seed_tasks():
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM tasks")

        task_count = cursor.fetchone()[0]

        insert_query = """
                INSERT INTO tasks (title, completed)
                VALUES (?, ?)
            """
            
        insert_tasks = [
                ("Learn FastAPI", False),
                ("Build CRUD API", False),
                ("Write README", True)
                ]
        
        if task_count == 0:
            cursor.executemany(insert_query , insert_tasks)

            connection.commit()


create_table()
seed_tasks()
