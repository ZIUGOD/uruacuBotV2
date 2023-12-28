from os import system, name
from time import sleep


def clear_terminal():
    """
    Clears the terminal screen based on the operating system.

    Returns:
        None
    """
    system("cls" if name == "nt" else "clear")


def wait_time(duration_in_seconds: int, allow_skip: bool = False):
    """
    Pauses execution for the specified duration, providing a countdown display.

    The terminal screen is cleared upon reaching 0 seconds if ``allow_skip`` is True.
    """
    if not isinstance(duration_in_seconds, int) or duration_in_seconds < 0:
        raise ValueError("Duration must be a non-negative integer.")

    try:
        for i in reversed(range(duration_in_seconds)):
            print(f"{color['yellow']}{i + 1}s remaining.{color['end']}", end="\r")
            sleep(0.99)

            if allow_skip and i == 0:
                clear_terminal()

    except KeyboardInterrupt:
        print("\nWaiting interrupted. Exiting...")


color = {
    "end": "\033[0m",
    "black": "\033[30m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
    # Bright versions
    "bright_black": "\033[90m",
    "bright_red": "\033[91m",
    "bright_green": "\033[92m",
    "bright_yellow": "\033[93m",
    "bright_blue": "\033[94m",
    "bright_magenta": "\033[95m",
    "bright_cyan": "\033[96m",
    "bright_white": "\033[97m",
    # Backgrounds
    "bg_black": "\033[40m",
    "bg_red": "\033[41m",
    "bg_green": "\033[42m",
    "bg_yellow": "\033[43m",
    "bg_blue": "\033[44m",
    "bg_magenta": "\033[45m",
    "bg_cyan": "\033[46m",
    "bg_white": "\033[47m",
}
