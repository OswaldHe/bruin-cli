import json
from pathlib import Path

_CURDIRT = Path(__file__).parent
_TASK_FILE = _CURDIRT / 'tasks.json'

def _print_list(task_list : list):
    for i in range(len(task_list)):
        item = task_list[i]
        name = item['name']
        subject = item['subject']
        deadline = item['deadline']
        print(f'{i+1}. {name}({subject}) - {deadline}')

def read_tasks_and_print():
    if not _TASK_FILE.is_file():
        print("No existing tasks! Try to add some.")
        return
    
    with open(_TASK_FILE) as f:
        task_dict = json.load(f)
        todo_list = task_dict['todo']
        review_list = task_dict['review']

        print("Todos: ")
        _print_list(todo_list)
        
        print("\nReviews: ")
        _print_list(review_list)

def add_task(name: str, deadline: str, subject: str):
    data = {
        "todo": [],
        "review": []
    }
    if _TASK_FILE.is_file():
        with open(_TASK_FILE) as json_file:
            data = json.load(json_file)
    
    task = {}
    task['name'] = name
    task['subject'] = subject
    task['deadline'] = deadline
    data['todo'].append(task)

    with open(_TASK_FILE, 'w') as json_file:
        json.dump(data, json_file)

def add_task_from_input():
    name = input("Title of the task: ")
    subject = input("Which course? (default: Misc): ")
    if subject == "" or subject is None:
        subject = "Misc"
    deadline = input("When should you finish it: ")

    add_task(name, deadline, subject)

    print("Task added!")

