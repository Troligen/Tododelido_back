import json
from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from ...schema.schemas import Todo_in, Todo_out

router = APIRouter()

test =  {"me": "hello"}

@router.get("/todo/", tags=["todo"], response_model=Dict[str, Todo_out])
def get_todo_list() -> Any:
    """
    Endpoint to get the todo list
    Will raise an HTTPError if something goes wrong
    """
    try:
        with open("../../task.json", "r") as f:
            todo_list = json.load(f)
        return {"data": todo_list["tasks"]}
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="couldn't find todo list pleace try again later")


@router.post("/todo/new_task", tags=["todo"], response_model=Dict[str, Todo_out])
def add_todo_task(task: Todo_in) -> Any:
    """
    Endpoint to add to the todo list
    Will send HTTPError 500 if something goes wrong
    """
    try:
        with open("../../task.json", "r+") as f:
            todo_list = json.load(f)
            todo_list["tasks"].append(task)
            f.seek(0)
            json.dump(todo_list, f, indent=4)
            f.truncate
        return {"data": todo_list["tasks"]}
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Couldn't write to the database pleace try again later")


@router.post("/todo/task_status", tags=["todo"], response_model=Dict[str, Todo_out])
def update_todo_tast_status(task: Todo_in) -> Any:
    """
    Endpoint to update the status of a task
    Will raise HTTPError 400 if task cant be found in the database
    Will raise HTTPError 500 if something goes wrong
    """
    try:
        with open("../../task.json", "r+") as f:
            todo_list =  json.load(f)
            for todo in todo_list["tasks"]:
                if todo["task"] == task.task:
                    todo["status"] = task.status
                    f.seek(0)
                    json.dump(todo_list, f, indent=4)
                    return {"data": todo_list["tasks"]}
        raise HTTPException(status_code=400, detail="task does not exist in the database")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="couln't reach the databse, try again later") 


@router.delete("/todo/delete_tasks", tags=["todo"], response_model=Dict[str, Todo_out])
def delete_todo_tasks() -> Any:
    """
    Endpoint that takes in a list of task dictionaries/objects for deletion
    Will raise HTTPError 400 if a task can't be found in the database
    Will raise HTTPError 500 if something regarding the database connection goes wrong
    """ 
    with open("../../task.json", "r+") as f:
        todo_list = json.load(f)
        new_todo_list = []
        for todo in todo_list["tasks"]:
            if todo["status"] == False:
                new_todo_list.append(todo)
        todo_list["tasks"] = new_todo_list
        json.dump(todo_list, f, indent=4)
    return {"data": todo_list["tasks"]}










