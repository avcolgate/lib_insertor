class Library:
    def __init__(self, path):
        with open(file=path, mode='rt') as file:
            lines = file.read().split('\n')
        self.body = lines
        self.cells = []
        self.templates = []
        self.name = path[path.replace('\\','/').rfind("/")+1:path.rfind(".")]

class Template:
    def __init__(self) -> None:
        self.name = ''
        self.body = []

class Cell:
    def __init__(self) -> None:
        self.name = ''
        self.body = []

class File:
    def __init__(self) -> None:
        self.body = []