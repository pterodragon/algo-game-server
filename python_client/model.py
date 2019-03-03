from dataclasses import dataclass, field
from enum import Enum
from typing import Tuple

"""
Bot writer should implement the following callback

def on_game_state(state: GameState, my_pid: int):
    '''
    Store the game state and if it's your turn,
    return an action upon analysis of all game states.
    Return None if it's not your turn

    return: Action
    '''
"""


class Color(Enum):
    WHITE = 0
    BLACK = 1

    def __repr__(self):
        return self.name


@dataclass
class Card:
    id: int  # for target use
    value: int  # 0 - 11, None for opponents' unrevealed card
    color: Color = Color.WHITE
    revealed: bool = False

    def _string_helper(self):
        color = self.color.name[0]
        value = '*' if self.value is None else self.value
        value_with_color = f'{color}{value}'
        value_str = f'[{value_with_color}]' if \
            self.revealed else value_with_color
        return value_str

    def __str__(self):
        vs = self._string_helper()
        return vs

    def __repr__(self):
        vs = self._string_helper()
        return f'<{self.id}: {vs}>'


@dataclass
class Player:
    '''
    "picked" is not included in "cards"
    when it's a player's turn, "picked" is a Card, else is None,
    "picked" is inserted into "cards" after that player's turn ends
    '''
    id: str
    cards: Tuple[Card] = field(default_factory=list)  # algo-ordered
    picked: Card = None
    chips: int = 0

    def __str__(self):
        card_str = ''.join(str(c) for c in self.cards)
        s = f'Player(pid: {self.id}, chips: {self.chips}, ' \
            f'picked: {self.picked}, ' \
            f'cards: {card_str})'
        return s


@dataclass
class GameState:
    players: Tuple[Player]
    turn: str  # player id, CAUTION: not the index from the client
    deck_size: int = 0

    '''
    id is not included as it interfers with __eq__ and __hash__
    # id: int  # indicates the state sequence number
    '''

    def __str__(self):
        s = f'GameState(turn: {self.turn}, ' \
            f'deck_size: {self.deck_size}, ' \
            f'players: {[str(x) for x in self.players]})'
        return s


@dataclass
class Action:
    pass


@dataclass
class Attack(Action):
    commit_cid: int  # from the attacker
    target_cid: int  # from the defender
    guess: int  # 0 - 11


@dataclass
class Stay(Action):
    ''' Valid only if player has attacked at least once '''
