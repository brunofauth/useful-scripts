import mimetypes as mt
import fire
import tqdm
import re
import os


MATCH = "Matched Pattern on line {:0=3d} of file {}"


def _find(dirpath, files, pattern, regex):
    for file in files:
        file_type, enc = mt.guess_type(file)
        if file_type is None or not file_type.startswith("text"):
            continue
        with open(os.path.join(dirpath, file), encoding=enc) as text:
            for i, line in enumerate(text):
                if regex and re.match(pattern, line) or pattern in line:
                    yield i, line, os.path.join(dirpath, file)


def find(pattern, path=".", recursive=False, regex=False):
    old_mans_cane = os.walk(path)
    dirpath, dirs, files = next(old_mans_cane)
    
    yield from _find(dirpath, files, pattern, regex):
    
    if not recursive:
        return
    
    for dirpath, dirs, files in old_mans_cane:
        yield from _find(dirpath, files, pattern, regex):


def main(pattern, path=".", recursive=False, regex=False): 
    print("Searching...")
    for i, line, path in tqdm.tqdm(find(pattern, path, recursive, regex)):
        print(f"Matched pattern on line {i:0=3d} of file {path}.")
        print(line)
        print()
    print("Done!")


if __name__ == "__main__":
    fire.Fire(main)

