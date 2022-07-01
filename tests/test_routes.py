from app.models.board import Board
from app.models.card import Card
import pytest

def test_get_boards_no_saved_boards(client):
    response = client.get('/boards')
    response_body = response.get_json()

    assert response.status_code == 200
    assert 'boards' in response_body
    assert response_body['boards'] == []

def test_create_board(client):
    board_params = {'title': 'Inspiration Board', 'owner': 'pytest'}

    response = client.post('/boards', json=board_params)
    response_body = response.get_json()

    assert response.status_code == 201
    assert 'board' in response_body
    assert response_body['board'] == {
        'board_id': 1,
        'title': 'Inspiration Board',
        'owner': 'pytest',
        'cards': []
    }

def test_get_boards_one_board(client, one_board):
    response = client.get('/boards')
    response_body = response.get_json()

    assert response.status_code == 200
    assert 'boards' in response_body
    assert len(response_body['boards']) == 1
    assert response_body['boards'][0] == {
        'board_id': 1,
        'title': 'One Board',
        'owner': 'one_board fixture',
        'cards': []
    }

def test_get_board_by_id(client, one_board):
    response = client.get('/boards/1')
    response_body = response.get_json()

    assert response.status_code == 200
    assert 'board' in response_body
    assert response_body['board'] == {
        'board_id': 1,
        'title': 'One Board',
        'owner': 'one_board fixture',
        'cards': []
    }

def test_get_cards_by_board_id(client, one_board_w_three_cards):
    response = client.get('/boards/1/cards')
    response_body = response.get_json()

    assert response.status_code == 200
    assert 'cards' in response_body
    assert len(response_body['cards']) == 3
