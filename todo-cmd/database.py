import sqlite3
import datetime
from model import Todo

conn = sqlite3.connect('todos.db')
c = conn.cursor()

def create_table():
    c.execute("""
              CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY,
                task TEXT,
                category TEXT,
                date_added TEXT,
                date_completed TEXT,
                position INTEGER
              )
              """)
    print("Table created successfully.")

def insert_todo(todo: Todo):
    c.execute('select count(*) FROM todos')
    count = c.fetchone()[0]
    todo.position = count if count else 0
    try:
        with conn:
            c.execute("INSERT INTO todos VALUES (:task, :category, :date_added, :date_completed, :position)",
                  {'task':todo.task, 'category':todo.category,'data_added':todo.date_added, 'date_completed':todo.date_completed,'status': todo.status ,'position':todo.position})
            conn.commit()
            print("Todo inserted successfully.")
    except Exception as e:
        print(f"Error inserting todo: {e}")



def get_all_todos() -> List[Todo]:
    c.execute("SELECT * from todos")
    rows = c.fetchall()
    todos = []
    for row in rows:
        todos.append(Todo(*row))

    return todos

def delete_todo(position):
    c.execute ('select count(*) from todos')
    count = c.fetchall()[0]

    with conn:
        c.execute("DELETE from todos WHERE position=: position", {"position": position})
        for pos in range(position+1, count):
            change_position(pos, pos-1, False)


def change_position(old_position: int, new_position:int, commit=True):
    c.execute('UPDATE todos SET position = :position_new WHERE position = :position_old',
              {'position_old':old_position, 'position_new': new_position}
              )
    

    if commit:
        conn.commit()








create_table()
# Example usage of insert_todo()
new_todo = Todo(task="Sample Task", category="Sample Category", date_added=str(datetime.datetime.now()), date_completed=None, position=1)
insert_todo(new_todo)
