#! /usr/bin/env python3

import contextlib as cl
import aiomcrcon as rc
import asyncio as aio
import getpass as gp
import fire
import sys
import os


def supports_color():
    plat = sys.platform
    valid_plat = plat != 'Pocket PC' and (plat != 'win32' or 'ANSICON' in os.environ)
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    return supported_platform and is_a_tty


def alt_codes_to_ansi(string):
    # Ugly, but faster than looping through a dict
    return (string
        .replace("§0", "\033[30m") # Black
        .replace("§1", "\033[34m") # Dark Blue
        .replace("§2", "\033[32m") # Dark Green
        .replace("§3", "\033[36m") # Dark Aqua
        .replace("§4", "\033[31m") # Dark Red
        .replace("§5", "\033[35m") # Purple
        .replace("§6", "\033[33m") # Gold
        .replace("§7", "\033[37m") # Gray
        .replace("§8", "\033[90m") # Dark Gray
        .replace("§9", "\033[94m") # Indigo
        .replace("§a", "\033[92m") # Bright Green
        .replace("§b", "\033[96m") # Aqua
        .replace("§c", "\033[91m") # Red
        .replace("§d", "\033[95m") # Pink
        .replace("§e", "\033[93m") # Yellow
        .replace("§f", "\033[97m") # White
        .replace("§l", "\033[1m") # Bold
        .replace("§n", "\033[4m") # Underline
        .replace("§o", "\033[3m") # Itallic
        .replace("§k", "\033[8m") # Magic
        .replace("§m", "\033[9m") # Strike
        .replace("§r", "\033[0m") # Reset
    ) + "\033[0m"


def strip_alt_codes(string):
    it = iter(string)
    return "".join(c for c in it if c != "§" or (next(it) and False))


@cl.asynccontextmanager
async def get_client(*args, **kwargs):
    client = rc.Client(*args, **kwargs)
    try:
        yield client
    except rc.ConnectionFailedError:
        print("Connection failed", file=sys.stderr)
    except rc.InvalidAuthError:
        print("Invalid password", file=sys.stderr)
    except EOFError:
        pass
    finally:
        await client.close()


async def rcon_loop(host, port=25575):
    ip = f"{host}:{port}"
    pw = os.environ.get("MC_RCON_PW", None) or gp.getpass()
    async with get_client(ip, pw) as client:
        await client.setup()
        for line in iter(lambda: input(">>> "), "quit"):
            print( format_output((await client.send_cmd(line))[0]) )


def main(host, port=25575, no_ansi=False):
    global format_output
    format_output = strip_alt_codes if no_ansi else alt_codes_to_ansi
    aio.run(rcon_loop(host, port))


if __name__ == "__main__":
    fire.Fire(main)

