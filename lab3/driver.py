import requests

BASE_URL = "http://127.0.0.1:8000"

# Create task
new_task = {
    "id": 1,
    "title": "Shower",
    "description": "Take a shower",
    "completed": False
}
res = requests.post(f"{BASE_URL}/tasks", json=new_task)
print("Create Task:", res.json())



# HelloWorld route
res = requests.get(f"{BASE_URL}/hello")
print("HelloWorld:", res.json())



# Get all tasks
res = requests.get(f"{BASE_URL}/")
print("All Tasks:", res.json())



# Update task title using query param
res = requests.put(f"{BASE_URL}/tasks/1/title", params={"title": "Shower Updated"})
print("Update Title:", res.json())



# Update task description using query param
res = requests.put(f"{BASE_URL}/tasks/1/description", params={"description": "Updated description"})
print("Update Description:", res.json())



# Mark task complete
res = requests.put(f"{BASE_URL}/tasks/1/complete")
print("Mark Complete:", res.json())



# Get completed tasks
res = requests.get(f"{BASE_URL}/tasks/status", params={"completed": True})
print("Completed Tasks:", res.json())


# Search by title
res = requests.get(f"{BASE_URL}/tasks/search", params={"title": "Shower"})
print("Search Title:", res.json())


# Get count of tasks
res = requests.get(f"{BASE_URL}/tasks/count")
print("Task Count:", res.json())


# Get count of completed tasks
res = requests.get(f"{BASE_URL}/tasks/count/completed")
print("Completed Count:", res.json())



# Add a second task
second_task = {
    "id": 2,
    "title": "Code",
    "description": "Work on lab",
    "completed": False
}
res = requests.post(f"{BASE_URL}/tasks", json=second_task)
print("Add Second Task:", res.json())



# Mark all tasks complete
res = requests.put(f"{BASE_URL}/tasks/complete-all")
print("Mark All Complete:", res.json())


# Reset all tasks to incomplete
res = requests.put(f"{BASE_URL}/tasks/reset-all")
print("Reset All Tasks:", res.json())



# Clear all tasks using body input
res = requests.put(f"{BASE_URL}/tasks/clear", params={"confirm": True})
print("Clear All Tasks:", res.json())
