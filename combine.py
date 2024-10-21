def read_file(file_path: str) -> str:
    with open(file_path, "r") as file:
        lines = file.readlines()
        i = 0
        while lines[i].strip() == "" or lines[i].strip().startswith("from") \
                or lines[i].strip().startswith("import"):
            i += 1
        return "".join(lines[i:])

def get_config():
    return {
        "initials": "from typing import Literal, List, Tuple\n" \
                    "from copy import deepcopy\n" \
                    "from random import randint\n" \
                    "import math\n" \
                    "from time import time\n" \
                    "height = 7\nwidth = 9\nsteal = True\nconnect = 4\n",
        "files": [
            "board/board.py",
            "algo/node.py",
            "algo/algo.py",
            "codingame.py",
        ]
    }

def combine():
    config = get_config()
    code = config["initials"]
    for file in config["files"]:
        code += read_file(file) + "\n"
    with open("combined.py", "w") as file:
        file.write(code)


if __name__ == "__main__":
    combine()
