
# TO DO LIST API
This is my submission for the wobot.ai assignment.

I have built a REST API for a to-do list application using the FastAPI framework, Python, and MongoDB database. 

The API allows users to create, read, update, and delete to-do tasks. Authentication is implemented to ensure only authorized users can access the API.


## How to run the file

```
pip install -r requirements.txt
```

## Usage

After installing all the requirements, run the code using this command:

```
uvicorn main:app --reload
```
Then,

```1``` register

```2``` login

After logging in, an authentication token will be generated, allowing users to access the application's functionalities




### User Routes
- `/users`: Fetches all users
- `/register`: Registers a user
- `/login`: Logs in a user and generates an authentication token
- `/authentication`: Checks the authentication of a user

### App Routes

- `/tasks/`: 
  - GET: Fetches all tasks.
  - POST: Creates a task.

- `/tasks/{task_id}/`: 
  - GET: Fetches all the details about a task with the provided task ID.
  - PUT: Updates a task.
  - DELETE: Deletes a task.

- `/completed_tasks`: 
  - **GET**: Fetches all completed tasks.

- `/remaining_tasks`: 
  - **GET**: Fetches all remaining tasks.


# Happy Coding!
All functionalities mentioned in the assignment have been successfully implemented and included in this TO DO LIST API.

Thank you to Wobot.ai for giving me this opportunity!