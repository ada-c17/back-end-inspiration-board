# CARD ROUTE TESTS

def test_create_card(client, one_board):

    card_params = {'message': 'i love broccoli', 'board_id': 1}

    response = client.post('/cards', json=card_params)
    response_body = response.get_json()

    assert response.status_code == 201
    assert 'card' in response_body
    assert response_body['card'] == {
        'card_id' : 1,
        'message' : 'i love broccoli',
        'likes_count' : 0,
        'board_id' : 1
    }


def test_edit_card(client, one_board_w_three_cards):

    card_params = {'message': 'i hate broccoli', 'likes_count': 1}

    response = client.patch('/cards/1', json=card_params)
    response_body = response.get_json()

    assert response.status_code == 200
    assert 'card' in response_body
    assert response_body['card'] == {
        'card_id' : 1,
        'message' : 'i hate broccoli',
        'likes_count' : 1,
        'board_id' : 1
    }



def test_delete_card(client, one_board_w_three_cards):

    response = client.delete('/cards/1')
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        'message' : "Card 1 'Card 1' successfully deleted"
    }

def test_edit_only_likes_card(client, one_board_w_three_cards):

    card_params = {'likes_count': 1}

    response = client.patch('/cards/1', json=card_params)
    response_body = response.get_json()

    assert response.status_code == 200
    assert 'card' in response_body
    assert response_body['card'] == {
        'card_id' : 1,
        'message' : 'Card 1',
        'likes_count' : 1,
        'board_id' : 1
    }

def test_edit_card_by_missing_id(client, one_board_w_three_cards):

    card_params = {'likes_count': 1}

    response = client.patch('/cards/4', json=card_params)
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {
        'message' : 'Card with id of 4 was not found'
    }


def test_edit_card_by_invalid_id(client, one_board_w_three_cards):

    card_params = {'likes_count': 1}

    response = client.patch('/cards/four', json=card_params)
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {
        'message' : 'four is not a valid id'
    }


def test_create_card_with_missing_data(client, one_board):

    card_params = {'message': 'i love broccoli'}

    response = client.post('/cards', json=card_params)
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {
        'message' : 'Invalid data: New card needs a message and a board id'
    }


def test_create_card_with_invalid_data(client, one_board):

    card_params = {'message': 'i love broccoli', 'board_id' : 'four'}

    response = client.post('/cards', json=card_params)
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {
        'message' : 'four is not a valid id'
    }

def test_get_card_by_id(client, one_board_w_three_cards):
    response = client.get('/cards/2')
    response_body = response.get_json()

    assert response.status_code == 200
    assert 'card' in response_body
    assert response_body['card'] == {
        'card_id' : 2,
        'message' : 'Card 2',
        'likes_count' : 0,
        'board_id' : 1
    }