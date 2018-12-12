# coding: UTF-8

import fire
import tqdm
import re
import os

def find(pattern: str, rootdir: str=".", recursive: bool=True) -> str:
    for dirpath, _, files in tqdm.tqdm(os.walk(rootdir)):
        matches = filter(lambda x: re.match(pattern, x), files)
        for file in matches:
            yield os.path.join(dirpath, file)

def finder(pattern: str, rootdir: str=".", recursive: bool=True) -> None:
    for match in find(pattern, rootdir, recursive):
        print(match)

if __name__ == "__main__":
    fire.Fire(finder)
