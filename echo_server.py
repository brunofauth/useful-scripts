#!/usr/bin/env python3


import http.server as httpsv
import socketserver as ssv
import fire


class Handler(httpsv.SimpleHTTPRequestHandler):

    def do_GET(self):
        print(self.headers)
        super().do_GET()


def main(host: str="", port: int=8000) -> None:
    ssv.TCPServer((host, port), Handler).serve_forever()


if __name__ == '__main__':
    fire.Fire(main)

