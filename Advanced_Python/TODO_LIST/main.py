tasks=[]
completed_tasks=set()

def add_task():
    task=input("Enter a new task: ")
    tasks.append(task)
    print(f"New task: {task} has been added to the list.\n")

def view_tasks():
    if not tasks:
        print("No tasks in the list.\n")

    print("\n====== TODO LIST ======\n")
    for idx, task in enumerate(tasks, start=1):
        status="✅ Completed" if task in completed_tasks else "❌ Not Completed"
        print(f"{idx}. {task} - {status}")

def mark_task_completed(task_number):
    if 1<=task_number<=len(tasks):
        task=tasks[task_number-1]
        completed_tasks.add(task)
        print(f"Task: {task} has been marked as completed.\n")
    else:
        print("Invalid task number. Please try again.\n")


def delete_task(task_number):
    if 1<=task_number<=len(tasks):
        task_item=tasks.pop(task_number-1)
        completed_tasks.discard(task_item)

        print(f"Task: {task_item} has been deleted from the list.\n")
    else:
        print("Invalid task number. Please try again.\n")


print(""" ====== TODO LIST ======
        1. Add a new task
        2. View all tasks  
        3. Mark a task as completed
        4. Delete a task
        5. Exit
        """)

while True:
        choice =int(input("Enter your choice (1-5): "))
        if choice==1:
            add_task()
        elif choice==2:
            view_tasks()
        elif choice==3:
            task_number=int(input("Enter the task number to mark as completed: "))
            mark_task_completed(task_number)
        elif choice==4:
            task_number=int(input("Enter the task number to delete: "))
            delete_task(task_number)
        elif choice==5:
            print("Exiting the TODO list application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__=="__main__":
    main()

    
        
