# part 1
class Directory:
    def __init__(self, name, subdirectories=None, files=None):
        self.name = name
        self.subdirectories = subdirectories or {}
        self.files = files or {}

    def size(self):
        return sum(subdir.size() for subdir in self.subdirectories.values()) + sum(
            file.size for file in self.files.values()
        )

    def __str__(self):
        output = [f"- {self.name} (dir, size={self.size()})"]
        for subdir in self.subdirectories.values():
            subdir_output = str(subdir)
            output += ["  " + line for line in subdir_output.split("\n")]
        for file in self.files.values():
            output.append("  " + str(file))
        return "\n".join(output)


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __str__(self):
        return f"- {self.name} (file, size={self.size})"


SIZE_LIMIT = 100000

# bulid file tree
root = Directory("/")
curr_path = [root]
with open("input.txt", "r") as f:
    # skip cd /
    f.readline()
    while f:
        clean_line = f.readline().strip()
        if clean_line == "":
            break
        elif clean_line.startswith("$ cd"):
            target = clean_line.split("cd ")[1]
            if target == "..":
                curr_path.pop()
            elif target == "/":
                curr_path = [root]
            else:
                sub_dir = curr_path[-1].subdirectories[
                    target
                ]  # assume it exists from previous ls calls
                curr_path.append(sub_dir)
        elif clean_line.startswith("$ ls"):
            # keep reading
            pass
        else:
            # assume we're reading ls output
            dir_or_size, name = clean_line.split(" ")
            if dir_or_size == "dir":
                new_dir = Directory(name)
                curr_path[-1].subdirectories[name] = new_dir
            else:
                new_file = File(name, int(dir_or_size))
                curr_path[-1].files[name] = new_file

print(root)

# DFS on the tree
total_size = 0
directory_stack = [root]
while directory_stack:
    curr_dir = directory_stack.pop()
    directory_stack.extend(curr_dir.subdirectories.values())
    size = curr_dir.size()
    if size <= SIZE_LIMIT:
        total_size += size
print(total_size)

# part 2
TOTAL_SPACE = 70000000
SPACE_NEEDED = 30000000
CURR_FREE_SPACE = TOTAL_SPACE - root.size()
FREE_AT_LEAST = SPACE_NEEDED - CURR_FREE_SPACE
print("free at least", FREE_AT_LEAST)

# DFS on the tree
best_size = root.size()
directory_stack = [root]
while directory_stack:
    curr_dir = directory_stack.pop()
    size = curr_dir.size()
    if size >= FREE_AT_LEAST:
        directory_stack.extend(curr_dir.subdirectories.values())
        if size < best_size:
            best_size = size
    # don't check subdirectories of directories that are too small

print(best_size)
