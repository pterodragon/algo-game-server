import model
from model import Attack

import random


def on_game_state(state: model.GameState, ID: int):
    '''
    Bot that will always attack from left to right for everything

    ID: my pid
    '''
    print('on_game_state')
    print(ID, state.turn)
    if state.turn != ID:
        return
    me = next(p for p in state.players if p.id == ID)
    my_commit = me.picked or next(c for c in me.cards if not c.revealed)
    my_commit_cid = my_commit.id

    for p in state.players:
        if p == me:
            continue
        assert isinstance(p, model.Player)
        for c in p.cards:
            assert isinstance(c, model.Card)
            if not c.revealed:
                return Attack(my_commit_cid, c.id, random.randrange(11))
