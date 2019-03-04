import requests
import json
import logging
import time

from .model import Card, Player, GameState, Color, Action, Attack, Stay


class Client:
    def __init__(self, token, domain):
        self.token = token
        self.domain = domain
        ep = {
            'join_room': (requests.post, '/rooms/join'),
            'create_room': (requests.post, '/rooms'),
            'leave_room': (requests.delete, '/rooms/join'),
            'ready': (requests.put, '/rooms/ready'),
            'unready': (requests.delete, '/rooms/ready'),
            'pick': (requests.post, '/games/action/pick'),
            'attack': (requests.post, '/games/action/attack'),
            'keep': (requests.post, '/games/action/keep'),
            'games': (requests.get, '/games'),
            'me': (requests.get, '/users/me')
        }
        self.end_points = {
            k: (v[0], f'{domain}{v[1]}') for k,
            v in ep.items()}

        self.state_history = []

        self.get_id_username()

        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            'l%(asctime)s | %(name)s | %(levelname)s | %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_id_username(self):
        jr = self.request('me')
        user = jr['user']
        self.name = user['name']
        self.id = user['id']

    def request(self, action, param='', json_payload=None):
        '''
        assume this is always successful otherwise blame the server or
        your network connection
        '''
        method, url = self.end_points[action]
        if action == 'join_room':
            assert param
            param = str(param)
            url += ('/' + param)
        elif action in ('pick', 'attack'):
            assert json_payload

        r = method(url, headers={
            'authorization': f'Bearer {self.token}'
        }, json=json_payload)
        try:
            if r.status_code != requests.codes.ok:
                self.logger.warning(f'[{action}] {r}: {r.text}')
                return

            r = json.loads(r.text)
            self.logger.debug(f'[{action}] {r}')
        except AttributeError:
            pass

        return r

    def gen_game_state(self, freq=1):
        '''
        assume the game has started

        generator to return the states
        '''
        def state_from_json(j):
            j_board_state = j['boardState']

            j_metadata = j_board_state['metadata']
            j_current_turn = j_metadata['currentTurn']
            j_deck_size = j_metadata['deckSize']

            j_scores = j_board_state['scores']
            j_players = j_board_state['players']
            j_hands = j_board_state['hands']

            players = []
            for pid, hand, score in zip(j_players, j_hands, j_scores):
                card_picked = None
                'id' 'color' 'isPicked' 'isRevealed' 'value'
                cards = []
                for c in hand:
                    cid = c['id']
                    cvalue = c.get('value', None)
                    ccolor = Color.WHITE if \
                        c['color'] == 'white' else Color.BLACK
                    crevealed = c['isRevealed']
                    card_ = Card(cid, cvalue, ccolor, crevealed)
                    cards.append(card_)
                    if c['isPicked']:
                        card_picked = card_

                p = Player(pid, cards, card_picked, score)
                players.append(p)

            turn = players[j_current_turn - 1].id
            s = GameState(players, turn, j_deck_size)
            return s

        self.game_state_id = 0  # 0-indexed

        jr = self.request('games')
        if not jr:
            return
        curr_state = state_from_json(jr)
        self.logger.info(repr(curr_state))
        yield curr_state
        time.sleep(freq)
        while True:
            jr = self.request('games')
            if not jr:
                return
            state = state_from_json(jr)
            if state == curr_state:
                time.sleep(freq)
                continue
            curr_state = state
            self.logger.info(repr(curr_state))
            yield curr_state
            self.game_state_id += 1

    def do_action(self, action: Action, pick=False):
        if isinstance(action, Attack):
            assert isinstance(action, Attack)
            com_cid = action.commit_cid
            target_cid = action.target_cid
            guess = action.guess
            if pick:
                self.request(
                    'pick',
                    json_payload={
                        'card_id': com_cid})
            self.request(
                'attack',
                json_payload={
                    'card_id': target_cid,
                    'value': guess})
        else:
            assert isinstance(action, Stay)
            self.request('keep')
