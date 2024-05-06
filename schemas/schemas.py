def task_serializer(item) -> dict:
    return {
        "id" : str(item["_id"]),
        "task" : item["task"],
        "completed" : item["completed"]
    }

def tasklist_serializer(items) -> list:
    return [task_serializer(item) for item in items]


def user_serializer(user) -> dict:
    return {
        "id" : str(user["_id"]),
        "username" : str(user["username"]),
        "password" : str(user["password"])
    }

def userlist_serializer(users) -> list:
    return [user_serializer(user) for user in users]