"""Minimal local subset of colorama used by this project."""


def init(autoreset=False):
    """Provide a compatible init function for terminal color support."""
    return autoreset


class Fore:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[39m"


class Style:
    RESET_ALL = "\033[0m"
