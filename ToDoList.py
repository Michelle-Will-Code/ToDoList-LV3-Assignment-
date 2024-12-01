from datetime import datetime
import csv
import os
import sys

class Task():
    def __init__(self, task, due_date, completed = False): #initilise
        self.task = task
        self.due_date = datetime.strptime(due_date, "%d/%m/%y")
        self.completed = completed

    def __str__(self): #automated method for printing statements
        status = "Done" if self.completed else "Not Done" #convert True/False into Done/Not Done
        return f"{self.task}, {self.due_date.strftime('%d/%m/%y')}, {status}" #shows user readable result

    def to_csv_rows(self):
        return [self.task, self.due_date.strftime("%d/%m/%y"), str(self.completed)]

    @classmethod
    def from_csv_rows(cls, row):
        task, due_date_str, completed_str = row
        return cls(task, due_date_str, completed_str == "True")

    def mark_complete(self):
        self.completed = True

class Task_Manager(): #contains all methods to manipulate/view tasks
    def __init__(self, filename ="tasks.csv"):
        self.filename = filename
        self.tasks = []

    def load_tasks_file(self):
        try:
            with open(self.filename, mode ='r', newline='') as file:
                reader = csv.reader(file)
                self.tasks = [Task.from_csv_rows(row) for row in reader]
        except FileNotFoundError:
            with open(self.filename, mode='a', newline='') as file:
                pass
            print("No file found. New one created.")
            self.load_tasks_file()

    def save_tasks_file(self):
        with open(self.filename, mode ='w', newline='') as file:
            writer = csv.writer(file)
            for task in self.tasks:
                writer.writerow(task.to_csv_rows())

    def add_task(self):
        task_description = input("Enter the task: ")
        while True:
            deadline = input("Enter the deadline for the task in DD/MM/YY format: ")
            try:
                new_task = Task(task_description, deadline)
                break
            except ValueError:
                print("Invalid date entered. Please try again.")
        self.tasks.append(new_task)
        self.save_tasks_file()
        clear_screen()
        input("Task added. \nPress Enter to return to main menu: ")
        
        
    def view_all_tasks(self):
        if self.tasks:
            print("All tasks on record: \n")
            for task in self.tasks:
                print(task)
        else:
            print("No tasks to display!")

    def view_incomplete_tasks(self):
        incomplete_tasks = [task for task in self.tasks if not task.completed]
        if incomplete_tasks:
            print("List of current incomplete tasks: \n")
            for task in incomplete_tasks:
                print(task)
            return incomplete_tasks
        else:
            print("You're all caught up!")
            return []

    def delete_task(self):

        if not self.tasks:
            print("No tasks available to delete.")
            input("\nPress Enter to return to the main menu.")
            return

        self.view_all_tasks() #display all tasks for clarity
        task_deletion = input("\nEnter the task name you wish to delete: ")
        matching_task = [task for task in self.tasks if task_deletion.lower() in task.task.lower()] #put matching tasks in list
        
        if matching_task:
            for task in matching_task:
                clear_screen()
                print(f"This task was found: {task}")
                confirm = input("\nDo you wish to delete this task? y/n: ")
                if confirm == "y":
                    self.tasks.remove(task)
                    print("\nTask successfully deleted.")
                    self.save_tasks_file()
        else:
            print("No matching task found.")
            return

        input("\nPress Enter to return to main menu.")

    def delete_all_completed(self):
        completed_tasks = [task for task in self.tasks if task.completed]
        if completed_tasks:
            print("Completed tasks: \n\n")
            for task in completed_tasks:
                print(task)
            confirm = input("\nDo you wish to delete all completed tasks on record? y/n ")
            if confirm == "y":
                clear_screen()
                self.tasks = [task for task in self.tasks if not task.completed]
                self.save_tasks_file()
                print("All completed tasks have been successfully removed. ")
            else:
                print("No tasks have been removed.")
        else:
            print("There are no completed tasks currently recorded.")

        input("Press Enter to return to main menu.")

    def delete_all(self):
        print("WARNING !!! This action will delete all contents of the task tracker and cannot be recoverable.\n Are you sure you wish to proceed?\n")
        confirm = input("Select 'y' or 'n' to proceed: ")
        if confirm == "y":
            self.tasks.clear()
            self.save_tasks_file()
            print("Task tracker records have been deleted.")
        else:
            print("No changes were made.")

        input("Press Enter to return to the main menu.")


    def mark_complete(self):
        incomplete_tasks = self.view_incomplete_tasks()
        if not incomplete_tasks:
            input("\nPress Enter to continue...")
            return
        task_completed = input("\nEnter the task name which has been completed: ")
        matching_task = [task for task in incomplete_tasks if task_completed.lower() in task.task.lower()]

        if matching_task:
            for task in matching_task:
                clear_screen()
                print(f"\nThis task was found: {task}")
                confirm = input ("\nDo you wish to mark this task 'complete' ? y/n: ")
                if confirm == "y":
                    task.mark_complete()
                    clear_screen()
                    print("\nTask marked complete.")
                    self.save_tasks_file()
                else:
                    clear_screen()
                    print("Task status is still marked as 'Incomplete'.")
        else:
            clear_screen()
            print("No matching task found.")

        input("\nPress Enter to return to the main menu.")

def clear_screen():
    if os.name == 'nt':
        os.system('cls')  # Windows
    else:
        os.system('clear')  # macOS and Linux

    # Fallback for IDEs
    sys.stdout.write("\033[2J\033[H") #clear screen, move cursor to top
    sys.stdout.flush()

#SUB MENUS#

def view_tasks_menu():
    view_sub_menu = """View Tasks
    
    1. View all incomplete tasks
    2. View all recorded tasks
    """

    print(view_sub_menu)
    selection_view = input("Make a choice and press Enter: ")
    if selection_view == "1": #view incomplete tasks
        clear_screen()
        task_manager.view_incomplete_tasks()
        input("\nPress Enter to continue: ")
    elif selection_view == "2": #view all tasks
        clear_screen()
        task_manager.view_all_tasks()
        input("\nPress Enter to continue: ")
    else:
        print("Invalid choice. Please try again. \n")
        view_sub_menu()

def remove_tasks_menu():
    remove_sub_menu = """Remove Tasks
    
    1. Remove a single task
    2. Remove all completed tasks
    3. Delete all records
    """

    print(remove_sub_menu)
    deletion_choice = input("Make a choice and press Enter: ")
    if deletion_choice == "1":
        clear_screen()
        task_manager.delete_task()
    elif deletion_choice == "2":
        clear_screen()
        task_manager.delete_all_completed()
    elif deletion_choice == "3":
        clear_screen()
        task_manager.delete_all()
    else:
        pass

#MAIN PROGRAM#

if __name__ == "__main__":

    task_manager = Task_Manager() #initilise task manager
    task_manager.load_tasks_file() #load tasks from the csv file

    while True:
        clear_screen()
        main_menu = """WELCOME TO TASK TRACKER

    What would you like to do today? 
    
    1. View Tasks
    2. Add A New Task
    3. Mark Task Complete
    4. Remove Tasks
    5. Exit
    """

        print(main_menu)
        selection = input("Please make a choice and press Enter: ")
        if selection == "1": # View Tasks Menu
            clear_screen()
            view_tasks_menu()
        elif selection == "2": # Add a New Task
            clear_screen()
            task_manager.add_task()
        elif selection == "3": # Mark Task Complete
            clear_screen()
            task_manager.mark_complete()
        elif selection == "4": # Remove a Task
            clear_screen()
            remove_tasks_menu()
        elif selection == "5": # exit app
            sys.exit()
        else:
            pass
