import threading
import time

import random_bot as bot

from algocli.client import Client
from algocli.model import Attack


def play(cli: Client):
    for state in cli.gen_game_state(freq=0.1):
        action = bot.on_game_state(state, cli.id)
        if not action:
            continue
        me = next(p for p in state.players if p.id == cli.id)
        pick = isinstance(action, Attack) and not me.picked
        cli.do_action(action, pick=pick)


def test_game_finish():
    domain = 'http://127.0.0.1:3000'
    tokens = ['token1', 'token2']
    clients = [Client(t, domain) for t in tokens]
    clients[0].request('create_room')
    clients[1].request('join_room', 1)
    for cli in clients:
        cli.request('ready')
    threads = [threading.Thread(target=play, args=(cli,)) for cli in clients]
    for t in threads:
        t.start()
    time.sleep(5)
    assert all(not t.is_alive() for t in threads)
