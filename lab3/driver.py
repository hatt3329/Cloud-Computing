import requests

BASE_URL = "http://127.0.0.1:8000"


#hello world route
def call_hello():
    res = requests.get(f"{BASE_URL}/hello")
    print("HelloWorld:", res.json())

#create new tasks
def create_task():
    id = int(input("Enter task ID: "))
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    completed = input("Is the task completed? (y/n): ").lower() == "y"
    #task formatting
    task = {
        "id": id,
        "title": title,
        "description": description,
        "completed": completed
    }

    res = requests.post(f"{BASE_URL}/tasks", json=task)
    print("Response:", res.json())

#grab all tasks
def get_all_tasks():
    res = requests.get(f"{BASE_URL}/")
    print("Tasks:", res.json())

#task via ID
def get_task_by_id():
    task_id = input("Enter task ID: ")
    res = requests.get(f"{BASE_URL}/tasks/{task_id}")
    print("Task:", res.json())

#update title of task
def update_task_title():
    task_id = input("Enter task ID: ")
    title = input("Enter new title: ")
    res = requests.put(f"{BASE_URL}/tasks/{task_id}/title", params={"title": title})
    print("Updated Title:", res.json())

#mark complete function
def mark_task_complete():
    task_id = input("Enter task ID: ")
    res = requests.put(f"{BASE_URL}/tasks/{task_id}/complete")
    print("Marked Complete:", res.json())

#search via title
def search_by_title():
    title = input("Enter title to search: ")
    res = requests.get(f"{BASE_URL}/tasks/search", params={"title": title})
    print("Search Results:", res.json())

#count the # of tasks
def count_tasks():
    res = requests.get(f"{BASE_URL}/tasks/count")
    print("Task Count:", res.json())

#Wipe all tasks
def clear_tasks():
    confirm = input("Are you sure you want to clear all tasks? (y/n): ").lower() == "y"
    if confirm:
        res = requests.put(f"{BASE_URL}/tasks/clear", params={"confirm": True})
        print("Clear Tasks:", res.json())
    else:
        print("Canceled.")

#menu UI
def menu():
    while True:
        print("\nTO-Do Menu")
        print("0. print hello world")
        print("1. create new task")
        print("2. grab all tasks")
        print("3. get task by ID")
        print("4. update task title")
        print("5. mark task complete")
        print("6. search by title")
        print("7. task count")
        print("8. clear all tasks")
        print("9. Exit")

        choice = input("select from the following options: ")

        if choice == "0":
            call_hello()
        elif choice == "1":
            create_task()
        elif choice == "2":
            get_all_tasks()
        elif choice == "3":
            get_task_by_id()
        elif choice == "4":
            update_task_title()
        elif choice == "5":
            mark_task_complete()
        elif choice == "6":
            search_by_title()
        elif choice == "7":
            count_tasks()
        elif choice == "8":
            clear_tasks()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()
