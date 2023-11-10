import typer
from rich.console import Console
from rich.table import Table
import json 
import os


console = Console()

app = typer.Typer()

#let's store the todos in  a JSON file 
TODO_FILE = "todos.json"
# Initialize the todos list from the JSON file
todos = []


if os.path.exists(TODO_FILE) and os.path.getsize(TODO_FILE) > 0:
    try:
        with open(TODO_FILE, "r") as file:
            todos = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        pass


@app.command(short_help='adds an item')
def add(task: str, category: str):
    typer.echo(f"adding {task}, {category}")
    todos.append({"Todo": task, "Category": category, "Status": "Not Yet"})

    # Save the updated todos list to the JSON file
    with open(TODO_FILE, "a") as file:
        json.dump(todos, file)
    
    


@app.command()
def delete(category: str = None, task: str = None):
    global todos
    
    if category and task:
        typer.echo(f"deleting task '{task}' in the category: {category}")
        todos = [todo for todo in todos if not (todo["Category"] == category and todo["Todo"] == task)]
    elif category:
        typer.echo(f"deleting all tasks in the category: {category}")
        todos = [todo for todo in todos if not (todo["Category"] == category)]
    elif task:
        typer.echo(f"deleting task: {task}")
        todos = [todo for todo in todos if not (todo["Todo"] == task)]
    else:
        typer.echo("Please provide either a category or a task to delete.")

    # Save the updated todos list to the JSON file
    with open(TODO_FILE, "w") as file:
        json.dump(todos, file)





@app.command()
def update(task: str, status: str):
    typer.echo(f"updating task: {task} to status: {status}")
    for todo in todos:
        if todo["Todo"] == task:
            todo["Status"] = status
            break
    else:
        typer.echo(f"Task '{task}' not found in your todos.")

    # Save the updated todos list to the JSON file
    with open(TODO_FILE, "w") as file:
        json.dump(todos, file)



@app.command()
def complete(position: int):
    typer.echo(f"completing {position}")
    show()

@app.command()
def show():
    #tasks = [{"Todo": "Todo1", "Category": "Study"}, {"Todo": "Todo2", "Category": "Sports"}]
    console.print("[bold magenta]Todos[/bold magenta]!", "***")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=5)
    table.add_column("Todo", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")

    def get_category_color(category):
        COLORS = {'Learn': 'cyan', 'Youtube': 'red', 'Sports': 'cyan', 'Study': 'green'}

        if category in COLORS:
            return COLORS[category]

        return 'white'

    for i, todo in enumerate(todos, start=1):
        c = get_category_color(todo["Category"])
        #is_done_str = 'Done' if True == 2 else 'Not Yet'
        table.add_row(str(i), todo["Todo"], f'[{c}]{todo["Category"]}[/{c}]',todo['Status'] )

    console.print(table)




if __name__ == "__main__":
    app()