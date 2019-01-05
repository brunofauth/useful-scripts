import mimetypes
import fire
import re
import os


MATCH = "Matched Pattern on line {:0=3d} of file {}"


def _find(dirpath, files, pattern, regex):
    for file in files:
        file_type, enc = mimetypes.guess_type(file)
        if file_type is not None and file_type.startswith("text"):
            with open(os.path.join(dirpath, file), encoding=enc) as text:
                for i, line in enumerate(text):
                    if regex and re.match(pattern, line) or pattern in line:
                        yield i, line, os.path.join(dirpath, file)


def find(pattern, path=".", recursive=False, regex=False):
    old_mans_cane = os.walk(path)
    dirpath, dirs, files = next(old_mans_cane)
    
    for match in _find(dirpath, files, pattern, regex):
        yield match
    
    if not recursive:
        return
    
    for dirpath, dirs, files in old_mans_cane:
        for match in _find(dirpath, files, pattern, regex):
            yield match


def main(pattern, path=".", recursive=False, regex=False, verbose=False):
    print("Searching...")
    if verbose:
        for i, line, path in find(pattern, path, recursive, regex, verbose):
            print(f"Matched pattern on line {i:0=3d} of file {path}.")
            print(line)
            print()
    else:
        for match in find(pattern, path, recursive, regex, verbose):
            print(f"Matched pattern on line {i:0=3d} of file {path}.")
    print("Done!")


if __name__ == "__main__":
    fire.Fire(main)
