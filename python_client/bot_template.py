import model
import requests
import json

TOKEN = 'replace your token here'
DOMAIN = 'http://127.0.0.1:3000'  # <- replace the domain here

r = requests.get(f'{DOMAIN}/users/me', headers={
            'authorization': f'Bearer {TOKEN}'
        })

jr = json.loads(r.text)

'''
your user id.
refer to this pid in the state to find your cards
'''
id = jr['user']['id']
name = jr['user']['name']  # your user name


def on_game_state(state: model.GameState):
    '''
    TODO: implement your bot here
    '''
