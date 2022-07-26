from app.models.board import Board
from app.models.card import Card
import pytest


#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_boards_no_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_board_one_board(client, one_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "Share your support", 
            "owner":"Shari",
            "cards": []
        }
    ]


#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_specific_board(client, one_board):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
            "id": 1,
            "title": "Share your support", 
            "owner":"Shari",
            "cards": []
        }
    


#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_board_not_found(client):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == 'Board 1 not found'


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_board(client):
    # Act
    response = client.post("/boards", json={
        "title": "It's a new board",
        "owner": "Ada Lovelace",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
            "id": 1,
            "title": "It's a new board",
            "owner": "Ada Lovelace",
        }
    
    new_board = Board.query.get(1)
    assert new_board
    assert new_board.title == "It's a new board"
    assert new_board.owner== "Ada Lovelace"

def test_adding_likes_to_card(client,one_card):
    # Act
    response = client.patch("/cards/1/like")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {'board_id': 1, 'id': 1, 'likes': 1, 'message': 'You can do it!'}

def test_create_board_with_invalid_data_returns_error(client):
    # Act
    response = client.post("/boards", json={})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"details": "Invalid data"}

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_card(client, one_card):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {'details': 'Card 1 You can do it! successfully deleted'}
    assert Card.query.get(1) == None

def test_delete_board(client, one_board):
    # Act
    response = client.delete("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {'details': 'Board 1 successfully deleted'}
    assert Board.query.get(1) == None


#@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_card_not_found(client):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == 'Card 1 not found'
    assert Card.query.all() == []


#@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_card_must_contain_message(client):
    # Act
    response = client.post("/cards", json={
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert Card.query.all() == []


#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_cards_for_specific_board(client, one_card_belongs_to_one_board):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [{'board_id': 1, 'id': 1, 'likes': 0, 'message': 'You can do it!'}]

    