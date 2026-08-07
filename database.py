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


def get_all_tasks():
    with get_connection() as connection:
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM tasks")
        
        rows = cursor.fetchall()
        
        return[
            {
                "id": row[0],
                "title": row[1],
                "completed": bool(row[2])
            }
            for row in rows
        ]
        
        
def get_task_by_id(task_id):
    with get_connection() as connection:
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM tasks WHERE id = ?",(task_id,))
        
        row = cursor.fetchone()
        
        if (row):
            return{
                    "id": row[0],
                    "title": row[1],
                    "completed": bool(row[2])
                }
        else:
            return None        

create_table()
seed_tasks()
