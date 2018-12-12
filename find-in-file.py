from mimetypes import guess_type
from re import match as re_match
from os import scandir
from fire import Fire

MATCH = "Matched Pattern on line {:0=3d} of file {}"

def find(pattern, path=".", recursive=False, regex=False, verbose=False):
    for entry in scandir(path):
        if entry.is_file():
            entry_type, encoding = guess_type(entry.path)
            if entry_type is not None and entry_type.startswith("text/"):
                with open(entry.path, errors="replace") as file:
                    for i, line in enumerate(file):
                        if regex and re_match(pattern, line) or pattern in line:
                            match = MATCH.format(i, entry.path)
                            yield (match, line) if verbose else match
        elif recursive:
            for match in find(pattern, entry.path, recursive, verbose):
                yield match

class ModuleWrapper:
    @staticmethod
    def findstr(pattern, path=".", recursive=False, regex=False, verbose=False):
        print("Searching...")
        if verbose:
            for match, line in find(pattern, path, recursive, regex, verbose):
                print(match)
                print(line)
                print()
        else:
            for match in find(pattern, path, recursive, regex, verbose):
                print(match)
        print("Done!")

if __name__ == "__main__":
    Fire(ModuleWrapper)