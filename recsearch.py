import os
import datetime
import platform

supported_platforms = ("Windows", "Linux", "Darwin")


class COLORS:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Filesearcher:
    PATH_DIVIDER = '\t'
    IGNORED_FILES = ("recsearch.py",)
    IGNORED_DIRS = ("venv", "__pycache__", ".idea")
    EXPORT_FILENAME = f"Recsearcher{datetime.datetime.strftime(datetime.datetime.now(), '%H %M %S %f')}.txt"

    def __init__(self, word, print_failed=False, absolute_find=False, export_to_file=False):
        self.print_failed = print_failed
        self.absolute_find = absolute_find
        self.export_to_file = export_to_file
        if self.export_to_file:
            self.file = open(self.EXPORT_FILENAME, 'x', encoding='utf-8')
        self.recursive_search(word, os.getcwd(), 0)

    def __del__(self):
        if self.export_to_file:
            self.file.close()

    def colorprint(self, color, *data):
        if self.export_to_file:
            print(*data, file=self.file)
        if color:
            print(f"{color}{' '.join(data)}{COLORS.ENDC}")
        else:
            print(*data)

    def search(self, word, path):
        lines = []
        try:
            with open(path, 'r') as f:
                counter = 0
                for line in f:
                    counter += 1
                    if self.absolute_find:
                        if word in line.split():
                            lines.append((line, counter))
                    else:
                        if word in line:
                            lines.append((line, counter))
        except Exception:
            return []
        else:
            return lines

    def recursive_search(self, word, path, deep):
        self.colorprint(COLORS.OKBLUE, f"{self.PATH_DIVIDER * deep}\u00ac{self.get_filename(path)}")
        subfolders, subfiles = [], []
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir():
                    subfolders.append(entry.path)
                elif entry.is_file():
                    subfiles.append(entry.path)
        for subfile in subfiles:
            if self.get_filename(subfile) not in self.IGNORED_FILES and "Recsearcher" not in subfile:
                finded = self.search(word, subfile)
                if finded:
                    for line, counter in finded:
                        line.replace('\n', '').replace('\r', '').strip()
                        if len(str(line)) > 256:
                            line = "LONG LINE"
                        self.colorprint(COLORS.OKGREEN, f"{self.PATH_DIVIDER * (deep + 1)}On line: {counter} in {line}")
                    self.colorprint(COLORS.OKGREEN, f"{self.PATH_DIVIDER * (deep + 1)}{self.get_filename(subfile)}")
                elif self.print_failed:
                    self.colorprint(COLORS.FAIL, f"{self.PATH_DIVIDER * (deep + 1)}{self.get_filename(subfile)}")
        for subfolder in subfolders:
            if self.get_filename(subfolder) not in self.IGNORED_DIRS:
                self.recursive_search(word, subfolder, deep + 1)
        return None

    @staticmethod
    def get_filename(path):
        return os.path.basename(path)


def main():
    cli_platform = str(platform.system())
    if cli_platform not in supported_platforms:
        print("This program is not supported on your platform")
        print(platform)
        return
    if cli_platform == "Windows":
        os.system('cls')
        os.system('color')
    else:
        os.system('clear')
    while True:
        word = input("Enter a word to search for: ")
        if word.lower() == "exit":
            break
        print_failed = input("Print failed files? (y/n) ") == "y"
        absolute_find = input("Absolute find? (y/n): ") == "y"
        export_result = input("Export result to file? (y/n): ") == "y"
        Filesearcher(word, print_failed, absolute_find, export_result)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Bye!")
    exit(0)
