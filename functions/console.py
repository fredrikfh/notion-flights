from datetime import datetime
import inspect

COLORS = {
    "info": "\033[94m",
    "success": "\033[92m",
    "danger": "\033[91m",
    "warning": "\033[93m",
    None: "",
}


def log(message, status=None):
    time_now = datetime.now().strftime("%H:%M:%S")
    file_name = inspect.stack()[1].filename.split("/")[-1]
    file_name = file_name.ljust(30)[:30]

    color = COLORS.get(status, "")

    print(f"{color}{time_now} | {file_name} | {message}\033[0m")
