#! /usr/bin/env python
# coding: UTF-8

import fire
import tqdm
import re
import os


def find(pattern: str, rootdir: str=".", all=True, recursive: bool=True) -> str:
    for dirpath, _, files in tqdm.tqdm(os.walk(rootdir)):
        for match in (x for x in files if re.match(pattern, x)):
            if not all:
                return os.path.join(dirpath, match)
            yield os.path.join(dirpath, match)


def finder(pattern: str, rootdir: str=".", recursive: bool=True) -> None:
    for match in find(pattern, rootdir, recursive):
        print(match)


if __name__ == "__main__":
    fire.Fire(finder)
