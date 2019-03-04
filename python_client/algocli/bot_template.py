from algocli.model import model


def on_game_state(state: model.GameState, ID: int):
    '''
    state: new state passed in
    ID: my pid

    return: model.Action or None

    TODO: implement your bot here.
        Store the state passed and return an action if it's your turn.
        Return None if it's not your turn
    '''
