
from app.database import get_connection
from app.schemas.task import TaskCreate,TaskUpdate,TaskPatch


def create_task(task : TaskCreate):
    connection = get_connection()
    task_data = task.model_dump(exclude_unset = True)
    
    if task_data["due_date"] is not None:
        task_data["due_date"] = task_data["due_date"].isoformat()
        
    cursor = connection.execute(""" 
                                INSERT INTO tasks(title,description,status,priority,due_date)
                                VALUES (?,?,?,?,?)
                                """,(
                                    task_data["title"],
                                    task_data["description"],
                                    task_data["status"],
                                    task_data["priority"],
                                    task_data["due_date"]
                                    )
                                )
    connection.commit()
    new_task_id  = cursor.lastrowid
    
    new_task = connection.execute("SELECT * FROM tasks WHERE id =?",
                                  (new_task_id,)
                                  ).fetchone()    
    connection.close()
    return dict(new_task)

def get_all_tasks():
    connection = get_connection()
    
    tasks = connection.execute("SELECT * FROM tasks").fetchall()
    
    connection.close()
    
    return [dict(task) for task in tasks]
     

def get_all_tasks_selected(status=None, priority=None):
    
    connection = get_connection()

    query = "SELECT * FROM tasks WHERE 1=1"
    values = []

    if status:
        query += " AND status = ?"
        values.append(status)

    if priority:
        query += " AND priority = ?"
        values.append(priority)

    tasks = connection.execute(
        query,
        values
    ).fetchall()

    connection.close()

    return [dict(task) for task in tasks]


def get_task_by_id(task_id:int):
    connection = get_connection()
    
    task = connection.execute("select * from tasks where id = ?",
                              (task_id,)).fetchone()
    connection.close()
    if task is None:
        return None
    return dict(task)


def update_task(task_id: int, task: TaskUpdate):
    
    connection = get_connection()

    existing_task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if existing_task is None:
        connection.close()
        return None

    task_data = task.model_dump()

    if task_data["due_date"] is not None:
        task_data["due_date"] = task_data["due_date"].isoformat()

    connection.execute(
        """
        UPDATE tasks
        SET title = ?,
            description = ?,
            status = ?,
            priority = ?,
            due_date = ?
        WHERE id = ?
        """,
        (
            task_data["title"],
            task_data["description"],
            task_data["status"],
            task_data["priority"],
            task_data["due_date"],
            task_id
        )
    )

    connection.commit()

    updated_task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()

    return dict(updated_task)

def patch_task(task_id: int, task: TaskPatch):
    
    connection = get_connection()

    existing_task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if existing_task is None:
        connection.close()
        return None

    task_data = task.model_dump(exclude_unset=True)

    if not task_data:
        connection.close()
        return dict(existing_task)

    if task_data.get("due_date") is not None:
        task_data["due_date"] = task_data["due_date"].isoformat()

    update_fields = ", ".join(
        [f"{key} = ?" for key in task_data]
    )

    values = list(task_data.values())
    values.append(task_id)

    connection.execute(
        f"""
        UPDATE tasks
        SET {update_fields}
        WHERE id = ?
        """,
        values
    )

    connection.commit()

    updated_task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()

    return dict(updated_task)

def delete_task(task_id:int):
    
    connection = get_connection()
    
    existing_task  = connection.execute("SELECT * FROM tasks WHERE id = ?",
                       (task_id,)).fetchone()
    
    if existing_task is None:
        connection.close()
        return None
    
    connection.execute("DELETE FROM tasks WHERE id = ?",(task_id,))
    
    connection.commit()
    connection.close()
    
    return dict(existing_task)  