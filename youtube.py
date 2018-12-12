# coding: UTF-8

import pygame.mixer
import webbrowser
import requests
import ctypes
import fire

YOUTUBE_API = r"https://www.googleapis.com/youtube/v3/search"
YOUTUBE_GUI = r"https://www.youtube.com/watch"

def search(query, api_key="AIzaSyC1kkAql9FQLq8lyETMCu29scm3bsbuHUg"):
    query_data = {"part": "id", "q": query, "key": api_key, "type": "video"}
    response = requests.get(YOUTUBE_API, params=query_data)
    try:
        videos = [item["id"]["videoId"] for item in response.json()["items"]]
    except KeyError:
        raise requests.HTMLResponseError(response.json()["message"])
    webbrowser.open(f"{YOUTUBE_GUI}?v={videos[0]}")

if __name__ == "__main__":
    fire.Fire(search)