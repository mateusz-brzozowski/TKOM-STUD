class ErrorManager:
    errors: list[Exception]

    def __init__(self) -> None:
        self.errors = []

    def add_error(self, error: Exception) -> None:
        """Add error to list."""
        self.errors.append(error)

    def print_errors(self) -> None:
        """Display all errors."""
        for error in self.errors:
            print(error)
