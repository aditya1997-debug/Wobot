from fastapi import FastAPI, HTTPException, Depends
from pymongo import ReturnDocument
from bson import ObjectId
from schemas.schemas import task_serializer, tasklist_serializer, user_serializer, userlist_serializer
from database.database import task_collection, client, users_collection
from models.task import Task, User
from auth.auth import AuthHandler

app = FastAPI()

auth_handler = AuthHandler()

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


# Home API
@app.get('/')
async def home():
    return {"result" : "Hello World!"}


# User endpoints
@app.get('/users')
async def users(username=Depends(auth_handler.auth_wrapper)):
    result = users_collection.find()
    return userlist_serializer(result)
 

@app.post('/register')
async def register(user_details: User):
    if " " in user_details.username:
        raise HTTPException(status_code=400, detail="Username should not contain")
    
    check_username = users_collection.find_one({"username" : user_details.username})
    # print(check_username)
    if check_username:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = auth_handler.get_password_hash(user_details.password)
    user_details.password = hashed_password
    users_collection.insert_one(dict(user_details))
    return "User created successfully"

@app.post('/login')
async def login(user_details: User):
    user = users_collection.find_one({"username": user_details.username})
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not auth_handler.verify_password(user_details.password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = auth_handler.encode_token(user['username'])
    return {"username": user['username'], "token" : token}

@app.get('/authentication')
async def authentication(username=Depends(auth_handler.auth_wrapper)):
    return {'name' : username}

# Creating a task
@app.post("/tasks/") 
async def create_task(task: Task, username=Depends(auth_handler.auth_wrapper)):
    get_task_by_name = task_collection.find_one({"task" : task.task})
    if get_task_by_name:
        return {"result" : "Task with this name already exists"}
    
    task_collection.insert_one(dict(task))
    return {"result" : "Task created Successfully"}

# Fetching all tasks from todo list
@app.get("/tasks/")
async def read_tasks(username=Depends(auth_handler.auth_wrapper)):
    all_tasks = tasklist_serializer(task_collection.find())
    if len(all_tasks) == 0:
        return {"result" : "No tasks to show"}
    return all_tasks

# Fetching single task from todo list 
@app.get("/tasks/{task_id}")
async def single_task(task_id, username=Depends(auth_handler.auth_wrapper)):
    try:
        task = task_collection.find_one({"_id": ObjectId(task_id)})
        if task:
            return task_serializer(task)
        else: 
            return {"result" : f"Task with id {task_id} does not exist"}
    except:
        return {"result" : "Task not found"}

# Updating todo list
@app.put("/tasks/{task_id}")
async def update_task(task_id: str, task: Task, username=Depends(auth_handler.auth_wrapper)):
    try:
        result = task_collection.find_one_and_update({"_id" : ObjectId(task_id)}, {"$set" : dict(task)}, return_document=ReturnDocument.AFTER)
        return {"result" : "Task updated successfully", "updated_task" : task_serializer(result)}
    except:
        return {"result" : "Task not found"}

# Deleting an element from todo list
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str, username=Depends(auth_handler.auth_wrapper)):
    try:
        result = task_collection.delete_one({"_id": ObjectId(task_id)})
        if result.deleted_count == 1:
            return {"result": "Task deleted successfully"}
        else:
            return {"result" : f"Task with id {task_id} does not exist"}
    except:
        return {"result" : "Task not found"}

# Fetching all completed tasks
@app.get("/completed_tasks")
async def completed_tasks(username=Depends(auth_handler.auth_wrapper)):
    try:
        result = task_collection.find({"completed" : True})
        return tasklist_serializer(result)
    except:
        return {"result" : "Error while fetching tasks"}

# Fetching all remaining tasks
@app.get("/remaining_tasks")
async def remaining_tasks(username=Depends(auth_handler.auth_wrapper)):
    try:
        result = tasklist_serializer(task_collection.find({"completed": False}))
        if len(result) == 0:
            return {"result" : "No remaining tasks"}
        return result
    except:
        return {"result":"Error while fetching tasks"}


