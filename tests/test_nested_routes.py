# NESTED ROUTE TESTS

def test_get_cards_by_board_id(client, one_board_w_three_cards):
    response = client.get('/boards/1/cards')
    response_body = response.get_json()

    assert response.status_code == 200
    assert 'cards' in response_body
    assert len(response_body['cards']) == 3

def test_delete_cards_by_board_id(client, one_board_w_three_cards):
    response = client.delete('/boards/1/cards')
    response_body = response.get_json()

    assert response.status_code == 200
    assert 'message' in response_body

    board_response = client.get('/boards/1')
    updated_board = board_response.get_json()['board']

    assert board_response.status_code == 200
    assert updated_board['cards'] == []

def test_create_card_by_board_id(client, one_board):
    card_params = {'message': 'The way Hope builds his House'}
    response = client.post('/boards/1/cards', json=card_params)
    response_body = response.get_json()

    assert response.status_code == 201
    assert 'card' in response_body
    assert response_body['card'] == {
        "card_id": 1,
        "message": 'The way Hope builds his House',
        "likes_count": 0,
        "board_id": 1
    }

def test_create_card_by_board_id_fails_w_empty_message(client, one_board):
    card_params = {'message': ''}
    response = client.post('/boards/1/cards', json=card_params)
    response_body = response.get_json()

    assert response.status_code == 400
    assert 'message' in response_body
    assert response_body['message'] == "Invalid data: New card needs a message"