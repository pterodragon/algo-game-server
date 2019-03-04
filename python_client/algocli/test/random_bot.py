import random

import algocli.model as model


def on_game_state(state: model.GameState, ID: int):
    '''
    Bot that will choose an opponent randomly
    , chooses a card randomly to attack
    and also chooses a random card from itself
    when the deck is empty
    '''
    if state.turn != ID:
        return
    me = next(p for p in state.players if p.id == ID)
    random.shuffle(me.cards)
    my_commit = me.picked or next(c for c in me.cards if not c.revealed)
    my_commit_cid = my_commit.id

    random.shuffle(state.players)
    for p in (p for p in state.players if p != me):
        assert isinstance(p, model.Player)
        random.shuffle(p.cards)
        for c in p.cards:
            assert isinstance(c, model.Card)
            if not c.revealed:
                return model.Attack(my_commit_cid, c.id, random.randrange(11))
