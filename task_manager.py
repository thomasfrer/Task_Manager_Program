import datetime  # Used later for displaying current time

def user_info(username, password):  # Function creates .txt with saved user data
    filename = f"{username}_tasks.txt"  # Names .txt file with user-entered name
    with open(filename, 'a') as f:
        f.write(password)
        f.write('\n')
        f.write('\n')

def signup():  # User signup function
    print("Please enter a username in which you will access your account.")
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    user_info(username, password)
    print("Proceed to log in.")
    login()

def task_update(username):
    filename = f"{username}_tasks.txt"

    try:
        with open(filename, 'r') as fr:
            existing_content = fr.read()
    except FileNotFoundError:
        existing_content = ''

    # Prompt user for the number of completed tasks
    num_completed = get_integer_input("How many tasks have been completed? ")
    completed_tasks = get_tasks(num_completed, "completed")

    # Prompt user for the number of ongoing tasks
    num_ongoing = get_integer_input("How many tasks are ongoing? ")
    ongoing_tasks = get_tasks(num_ongoing, "ongoing")

    # Prompt user for the number of incomplete tasks
    num_incomplete = get_integer_input("How many tasks are incomplete? ")
    incomplete_tasks = get_tasks(num_incomplete, "incomplete")

    # Append new tasks to existing content only if tasks are entered for a category
    new_content = "\n---------------\n"
    DT = str(datetime.datetime.now())
    new_content += DT + "\n\n"

    if completed_tasks:
        new_content += "COMPLETED TASK(S):\n" + "\n".join(completed_tasks) + "\n\n"

    if ongoing_tasks:
        new_content += "ONGOING TASK(S):\n" + "\n".join(ongoing_tasks) + "\n\n"

    if incomplete_tasks:
        new_content += "YET-TO-DO:\n" + "\n".join(incomplete_tasks) + "\n"

    # Combine existing content and new content
    updated_content = existing_content + new_content

    # Write back the updated content along with new tasks
    with open(filename, 'w') as fw:
        fw.write(updated_content)

    print("Tasks updated successfully!")

def get_tasks(num_tasks, task_type):
    tasks = []
    for i in range(1, num_tasks + 1):
        task_description = input(f"Enter {task_type} task {i}: ")
        due_date = input(f"Enter due date for {task_type} task {i} (YYYY-MM-DD): ") if num_tasks > 0 else ""
        tasks.append(f"{task_description} - {due_date}")
    return tasks if num_tasks > 0 else []

def get_integer_input(prompt, max_attempts=10):
    attempts = 0
    while attempts < max_attempts:
        try:
            user_input = int(input(prompt))
            return user_input
        except ValueError:
            print("Invalid input! Please enter an integer.")
            attempts += 1

    print("Maximum attempts reached. Returning to the main menu.")
    return 0

def login():
    attempts = 5  # Set the number of login attempts
    while attempts > 0:
        print("Please enter your username and password to log in.")
        username = input("Username: ")
        password = input("Password: ")

        try:
            filename = f"{username}_tasks.txt"  # Accesses the users saved file for login
            with open(filename, 'r') as f:
                stored_password = f.readline().strip()

                if password == stored_password:  # Checks if login info is correct
                    user_logged_in = True
                    while user_logged_in:
                        print("1 - Add new task \n2 - Update existing tasks \n3 - View tasks \n4 - Log out")  # Menu popup
                        choice = input("Enter here: ")

                        if choice.isdigit() and 1 <= int(choice) <= 4:
                            # Requires user to input 1-5
                            if choice == '1':
                                task_new(username)
                            elif choice == '2':
                                task_update(username)
                            elif choice == '3':
                                view_tasks(username)
                            elif choice == '4':
                                print("Logged out.")
                                user_logged_in = False
                        else:
                            print("Invalid input! Please enter an integer between 1 and 5.")

                    break  # Break out of the login loop

                else:
                    print("USERNAME OR PASSWORD IS INCORRECT")
                    attempts -= 1  # Decrement the number of login attempts

        except FileNotFoundError:
            print("User not found. Please try again.")
            attempts -= 1  # Decrement the number of login attempts
        except Exception as e:
            print(f"An error occurred: {e}")

    if attempts == 0:
        print("Maximum login attempts reached. Exiting.")
        return False  # Return False to indicate unsuccessful login

def task_new(username):  # New task function
    print("How many tasks would you like to add?")
    count = int(input("Enter here: "))
    filename = f"{username}_tasks.txt"

    with open(filename, 'a') as f:  # Loop to add specified # of tasks
        for i in range(1, count + 1):
            task = input(f"Enter task {i}: ")
            date = input(f"Enter due date {i} (YYYY-MM-DD): ")

            f.write(f"{task} - {date}\n")

    print("Tasks added successfully!")

def view_tasks(username):
    filename = f"{username}_tasks.txt"
    try:
        with open(filename, 'r') as f:  # Accesses user saved file for view
            lines = f.readlines()
            for line in lines[1:]:  # Skip the first line (password)
                if "due date" in line.lower():
                    print(line, end="")
                else:
                    print(line, end="")
        print("\n---------------\n")
    except FileNotFoundError:
        print("No tasks found for this user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':  # Intro/menu screen pop-up
    print("THOMAS'S TASK MANAGER")
    print("Are you new?")

    choice = int(input("Type 1 to sign up, otherwise type 0 to login: "))

    if choice == 1:
        signup()
    elif choice == 0:
        login()
    else:
        print("Invalid input!")
