# Simple command-line to-do list application using Typer and Rich libraries


Todocli is a simple command-line to-do list application built with Python, Typer, and Rich.

## Features

- Add new tasks with categories
- Delete tasks by category or specific task
- Update task status
- View and complete tasks

## Getting Started

### Prerequisites

- Python 3.x
- Dependencies: Typer, Rich

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/TodoCLI.git
   cd TodoCLI ```

#### Install dependencies:
```bash
  pip install -r requirements.txt
 ```

## Usage

#### Add a new task:
```bash
python todocli.py add
```

#### Delete a task:
```bash
python todocli.py delete
```

#### Update a task status:
```bash
python todocli.py update
```

#### Complete a task (same with update, but works different)

```bash
python todocli.py complete {position}
```

#### View tasks:

```bash 
python todocli.py show
```
