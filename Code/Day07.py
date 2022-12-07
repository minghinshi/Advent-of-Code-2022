class file:
    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self.size = size

    def get_size(self):
        return self.size

class directory:
    def __init__(self, name) -> None:
        self.directories = []
        self.files = []
        self.name = name
    
    def add_directory(self, directory):
        self.directories.append(directory)
        directory.set_parent(self)

    def add_file(self, file):
        self.files.append(file)

    def find_directory(self, name):
        for dir in self.directories:
            if dir.get_name() == name:
                return dir

    def get_size(self):
        total = 0
        for file in self.files:
            total += file.get_size()
        for dir in self.directories:
            total += dir.get_size()
        return total

    def get_all_directories(self):
        list = []
        for dir in self.directories:
            list.extend(dir.get_all_directories())
        list.append(self)
        return list

    def get_name(self):
        return self.name

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

root_directory: directory = directory("/")
current_directory: directory = root_directory

def set_current_directory(name: str):
    global current_directory
    if name == "..":
        current_directory = current_directory.get_parent()
    elif name == "/":
        current_directory = root_directory
    else:
        current_directory = current_directory.find_directory(name)

def parse_command(keywords: list[str]):
    if keywords[0] == "cd":
        set_current_directory(keywords[1])
    elif keywords[0] == "ls":
        pass

def add_directory(name: str):
    new_directory = directory(name)
    current_directory.add_directory(new_directory)

def add_file(name: str, size: int):
    new_file = file(name, size)
    current_directory.add_file(new_file)

def parse_line(line: str):
    keywords = line.split()
    if keywords[0] == "$":
        parse_command(keywords[1:])
    elif keywords[0] == "dir":
        add_directory(keywords[1])
    elif keywords[0].isnumeric():
        add_file(keywords[1], int(keywords[0]))

with open("Inputs/Day07.txt") as input_file:
    for line in input_file:
        parse_line(line)

directory_sizes = list(map(directory.get_size, root_directory.get_all_directories()))
target = root_directory.get_size() - 40000000
print(sum(filter(lambda x: x <= 100000, directory_sizes)))
print(min(filter(lambda x: x >= target, directory_sizes)))