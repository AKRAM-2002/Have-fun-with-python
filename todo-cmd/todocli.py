import typer
from rich.console import Console
from rich.table import Table
import json
import os
from model import Todo
from typing import Optional


console = Console()
app = typer.Typer()


TODO_FILE = "todos.json"
CATEGORY_COLORS_FILE = "category_colors.json"
todos = []
category_colors = {}  



if os.path.exists(TODO_FILE) and os.path.getsize(TODO_FILE) > 0:
    try:
        with open(TODO_FILE, "r") as file:
            todos = json.load(file) #Load from JSON FILE
    except (FileNotFoundError, json.JSONDecodeError) as e:
        console.print(f"Error loading todos: {e}", style="bold red")

if os.path.exists(CATEGORY_COLORS_FILE) and os.path.getsize(CATEGORY_COLORS_FILE) > 0:
    try:
        with open(CATEGORY_COLORS_FILE, "r") as file:
            category_colors = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        console.print(f"Error loading category colors: {e}", style="bold red")


#Save todos in json file
def save_todos():
    try:
        with open(TODO_FILE, "w") as file:
            json.dump(todos, file)
        console.print("Todos saved successfully.", style="bold green")
    except Exception as e:
        console.print(f"Error saving todos: {e}", style="bold red")


#Get User Input
def get_task_info():
    task = typer.prompt("Enter the task:")
    category = typer.prompt("Enter the category:")
    return task, category


#add function that save the todos entered by the user
@app.command(short_help='adds an item')
def add():
    typer.echo("Adding a new task:")
    task, category = get_task_info()
    todos.append({"Todo": task, "Category": category, "Status": "Not Yet"})
    save_todos()


#Remove todo that the user requested to delete
@app.command()
def delete(category: Optional[str] = None, task: Optional[str] = None):
    global todos

    if not category and not task:
        typer.echo("Please provide either a category or a task to delete.")
        return

    if not category:
        category = typer.prompt("Enter the category:")

    if not task:
        task = typer.prompt("Enter the task:")

    typer.echo(f"Deleting task '{task}' in the category: {category}")
    todos = [todo for todo in todos if not (todo["Category"] == category and todo["Todo"] == task)]
    save_todos()


#Change the status of your todo list(Done or Undone)
@app.command()
def update():
    typer.echo("Updating a task:")
    task, category = get_task_info()
    status = typer.prompt("Enter the new status (e.g., Done, Not Yet):")
    
    for todo in todos:
        if todo["Todo"] == task and todo["Category"] == category:
            todo["Status"] = status
            typer.echo(f"Task '{task}' in category '{category}' updated to status: {status}")
            save_todos()
            return

    typer.echo(f"Task '{task}' in category '{category}' not found in your todos.")


@app.command()
def complete(position: int):
    typer.echo(f"Completing task at position {position}")
    show()



#Displaying the list of todos by show command
@app.command()
def show():
    console.print("[bold magenta]Todos[/bold magenta]!", "***")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=5)
    table.add_column("Todo", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")

    for i, todo in enumerate(todos, start=1):
        c = get_category_color(todo["Category"])
        table.add_row(str(i), todo["Todo"], f'[{c}]{todo["Category"]}[/{c}]', todo['Status'])

    console.print(table)


#Get the color specified for category
def get_category_color(category):
    return category_colors.get(category, 'white')


if __name__ == "__main__":
    app()
