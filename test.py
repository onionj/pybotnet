


def _cat(command: list[str]) -> str:
    if len(command) >= 2:
        path = command[1]
    else:
        path = " "

    try:
        with open(path, "r") as file:
            return file.read()

    except FileNotFoundError as error:
        return error
    except Exception as error:
        return error  


print(_cat(["cat", "/home/onion/.zshrc"]))