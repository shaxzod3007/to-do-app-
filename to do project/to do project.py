import json
import os


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.tasks = []

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'tasks': [task.to_dict() for task in self.tasks],
        }


class Task:
    def __init__(self, text, completed=False, id=None):
        self.id = id
        self.text = text
        self.completed = completed

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'completed': self.completed,
        }


class UserManager:
    def __init__(self, data_file='users.json'):
        self.data_file = data_file
        self.users = []
        if not os.path.exists(self.data_file):
            self.register_user_test()
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                for user_data in data:
                    user = User(
                        username=user_data['username'],
                        password=user_data.get('password', ''),
                    )
                    user.tasks = [Task(**task_data) for task_data in user_data.get('tasks', [])]

                    for i, task in enumerate(user.tasks, start=1):
                        task.id = i
                    self.users.append(user)

    def save_data(self):
        data = [user.to_dict() for user in self.users]
        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=2)

    def register_user(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        # username zanyat yoki yoqligini tekshirish
        if any(user.username == username for user in self.users):
            print(f"User '{username}' is already registered.")
        else:
            user = User(username=username, password=password)
            self.users.append(user)
            self.save_data()
            print(f"User '{username}' has been registered.")

    def authenticate_user(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        # Check if the username and password match
        current_user = next((user for user in self.users if user.username == username and user.password == password),
                            None)

        if current_user:
            print(f"User '{username}' is authenticated.")
            self.perform_user_actions(current_user)
        else:
            print("Invalid username or password.")

    def perform_user_actions(self, user):
        while True:
            print("\n1. Add task")
            print("2. View tasks")
            print("3. Mark task as completed")
            print("4. Mark task as not completed")
            print("5. Logout")

            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                self.add_task(user)
            elif choice == '2':
                self.view_tasks(user)
            elif choice == '3':
                self.mark_task_completed(user, True)
            elif choice == '4':
                self.mark_task_completed(user, False)
            elif choice == '5':
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 5.")

    def add_task(self, user):
        task_text = input("Enter the task text: ")
        task = Task(text=task_text)
        task.id = len(user.tasks) + 1
        user.tasks.append(task)
        self.save_data()
        print(f"Task added: {task_text}")

    def view_tasks(self, user):
        if user.tasks:
            print("Tasks:")
            for task in user.tasks:
                status = "Completed" if task.completed else "Not Completed"
                print(f"{task.id}. {task.text} - {status}")
        else:
            print("No tasks found.")

    def mark_task_completed(self, user, completed):
        self.view_tasks(user)
        task_id = input("Enter the ID of the task you want to mark: ")

        try:
            task_id = int(task_id)
            task = next((task for task in user.tasks if task.id == task_id), None)

            if task:
                task.completed = completed
                self.save_data()
                status = "Completed" if completed else "Not Completed"
                print(f"Task {task_id} marked as {status}.")
            else:
                print(f"Task with ID {task_id} not found.")
        except ValueError:
            print("Invalid task ID. Please enter a number.")

    def register_user_test(self):
        # Test ma'lumotlarini qo'shish
        user1 = User(username='testuser1', password='testpassword1')
        task1_user1 = Task(text='Test task 1 for User 1')
        task2_user1 = Task(text='Test task 2 for User 1', completed=True)
        user1.tasks.extend([task1_user1, task2_user1])

        user2 = User(username='testuser2', password='testpassword2')
        task1_user2 = Task(text='Test task 1 for User 2')
        task2_user2 = Task(text='Test task 2 for User 2', completed=True)
        user2.tasks.extend([task1_user2, task2_user2])

        user3 = User(username='testuser3', password='testpassword3')
        task1_user3 = Task(text='Test task 1 for User 3')
        task2_user3 = Task(text='Test task 2 for User 3', completed=True)
        user3.tasks.extend([task1_user3, task2_user3])

        self.users.extend([user1, user2, user3])
        self.save_data()



user_manager = UserManager()

while True:
    print("\n1. Register new user")
    print("2. Authenticate user")
    print("3. Exit")

    choice = input("Enter your choice (1, 2, or 3): ")

    if choice == '1':
        user_manager.register_user()
    elif choice == '2':
        user_manager.authenticate_user()
    elif choice == '3':
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
