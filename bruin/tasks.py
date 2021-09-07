import json
from pathlib import Path
from datetime import datetime
from termcolor import colored, cprint

_CURDIRT = Path(__file__).parent
_TASK_FILE = _CURDIRT / 'tasks.json'

def _print_list(task_list : list):
    for i in range(len(task_list)):
        item = task_list[i]
        name = item['name']
        subject = item['subject']
        deadline = item['deadline']
        log_string = f'{i+1}. {name}({subject}) - {deadline}'
        date_obj = datetime.strptime(deadline, '%Y-%m-%d').date()
        if date_obj == datetime.today().date():
            print(colored(log_string, 'red', attrs=['bold']))
        else:
            print(log_string)

    print("")

def read_tasks_and_print():
    if not _TASK_FILE.is_file():
        print("No existing tasks! Try to add some.")
        return
    
    with open(_TASK_FILE) as f:
        task_dict = json.load(f)
        todo_list = task_dict['todo']
        review_list = task_dict['review']

        cprint("Todos:", 'grey', 'on_yellow', end='\n')
        _print_list(todo_list)
        
        cprint("Reviews:", 'white', 'on_blue', end='\n')
        _print_list(review_list)

def _add_task(name: str, deadline: str, subject: str):
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
    try:
        datetime.strptime(deadline, "%Y-%m-%d")
    except ValueError:
        print("Invalid deadline format: please use YYYY-MM-DD format!")
        return

    _add_task(name, deadline, subject)

    print("Task added!")

def complete_task(index: int):
    if not _TASK_FILE.is_file():
        print("You don't have a task yet.")
    else:
        data = {}
        with open(_TASK_FILE) as json_file:
            data = json.load(json_file)
        todo_list : list = data['todo']
        if len(todo_list) >= index:
            data['review'].append(todo_list.pop(index-1))
            with open(_TASK_FILE, 'w') as json_file:
                json.dump(data, json_file)
            print("Task completed and wait for review later.")
        else:
            print("You typed a wrong task index")

def _terminate_task(type: str, index: int):
    if not _TASK_FILE.is_file():
        print("You don't have a task yet.")
    else:
        data = {}
        with open(_TASK_FILE) as json_file:
            data = json.load(json_file)

        if type in data:
            task_list = data[type]
            if len(task_list) >= index:
                task_list.pop(index-1)
                with open(_TASK_FILE, 'w') as json_file:
                    json.dump(data, json_file)
                print("Task closed.")
            else:
                print("You typed a wrong task index")
        else:
            print("You can only close task from either TODO or REVIEW bucket.")

def _validate_index_string(index_string: str) -> bool:
    '''
    a string should be in format 't{%d}' or 'r{%d}'
    '''
    if len(index_string) < 2:
        print("Invalid index string length!")
        return False
    elif index_string[0] != 't' and index_string[0] != 'r':
        print("Invalid index string prefix!")
        return False
    elif not index_string[1:].isnumeric():
        print("Index need to have a number suffix!")
        return False
    else:
        return True

def terminate_task_by_string(index_string: str):
    
    if _validate_index_string(index_string):
        list_type = 'todo' if index_string[0] == 't' else 'review'
        index = int(index_string[1:])
        _terminate_task(list_type, index)