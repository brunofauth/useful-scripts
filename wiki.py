import wikipedia as wiki

from textwrap import fill
from pprint import pformat
import fire


def search_wikipedia(query, lang="en"):
    if lang not in wiki.languages():
        raise ValueError(f"Available 'lang' values:\n{pformat(wiki.languages())}")
    wiki.set_lang(lang)
    results = wiki.search(query)
    if not results:
        raise RuntimeError("Wikipedia has no articles on the entered topic.")
    print("\nPick a disambiguition:\n")
    for i, result in enumerate(results):
        print(f"{i+1:0=2d}) {result}")
    choice = int(input(">>> ")) - 1
    if choice > len(results) or choice < 0:
        raise ValueError("Invalid article identifier.")
    print("\n" + fill(wiki.summary(results[choice]).strip("\n")))


if __name__ == "__main__":
    fire.Fire(search_wikipedia)
