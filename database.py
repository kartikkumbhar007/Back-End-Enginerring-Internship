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
        
def search_tasks(search):
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM tasks WHERE title LIKE ?",
            (f"%{search}%",)
        )

        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "title": row[1],
                "completed": bool(row[2])
            }
            for row in rows
        ]


def get_tasks_by_status(completed):
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM tasks WHERE completed = ?",
            (completed,)
        )

        rows = cursor.fetchall()

        return [
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


def add_task(title):
    with get_connection() as connection:
        cursor = connection.cursor()
        
        cursor.execute("INSERT INTO tasks (title,completed) VALUES (?,?)",(title,False))
        
        task_id = cursor.lastrowid
        
        connection.commit()
        
        return get_task_by_id(task_id)
    
    
def update_task(task_id, title, completed):
    with get_connection() as connection:
        cursor = connection.cursor()
        
        cursor.execute(""" 
                       UPDATE tasks
                       SET title = ? , completed = ?
                       WHERE id = ?
                       """, 
                       (title, completed, task_id)
                       )
        
        connection.commit()
        
        if cursor.rowcount == 0:
            return None
        
        return get_task_by_id(task_id)


def delete_task(task_id):
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )

        if cursor.rowcount == 0:
            return False

        connection.commit()

        return True
    
        
create_table()
seed_tasks()
