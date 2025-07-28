class InvalidCredentials(Exception):
    """Raised when try to login with invalid credentials."""

    def __init__(self):
        self.message = "Invalid credentials."
        super().__init__(self.message)


class TaskDoesNotExists(Exception):
    """Raised when the task does not exits."""

    def __init__(self, task_id):
        self.task_id = task_id
        self.message = f"The task with id:{self.task_id} does not exists."
        super().__init__(self.message)


class TaskListDoesNotExists(Exception):
    """Raised when the task does not exits."""

    def __init__(self, task_list_id):
        self.task_list_id = task_list_id
        self.message = f"The task with id:{self.task_list_id} does not exists."
        super().__init__(self.message)


class EmailAlreadyExists(Exception):
    """Raised when the email already exits."""

    def __init__(self, email):
        self.email = email
        self.message = f"The User with email:{self.email} already exits."
        super().__init__(self.email)
