import argparse
import logging
import time

from algocli.client import Client
from algocli.model import Attack

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--room-id', required=False, type=int)
    parser.add_argument('--bot-module', default='bot')
    parser.add_argument('--freq', default=1, type=float)
    parser.add_argument('--domain', default='http://127.0.0.1:3000')
    parser.add_argument('--token', required=True)
    args = parser.parse_args()

    cli1 = Client(args.token, args.domain)
    cli1.logger.setLevel(logging.INFO)
    bot = __import__(args.bot_module)

    cli1.request('me')
    room_id = args.room_id
    freq = args.freq
    if room_id:
        cli1.request('join_room', room_id)
    else:
        cli1.request('create_room')
    cli1.request('ready')
    while not next(cli1.gen_game_state(), None):
        cli1.logger.info('game not started')
        time.sleep(1)

    for state in cli1.gen_game_state(freq=freq):
        action = bot.on_game_state(state, cli1.id)
        if not action:
            continue
        me = next(p for p in state.players if p.id == cli1.id)
        pick = isinstance(action, Attack) and not me.picked
        cli1.do_action(action, pick=pick)
