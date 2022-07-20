from urllib import response
from app.models.board import Board
from app.models.card import Card
import pytest


def test_get_all_boards(client, all_boards):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [
        {'board_id': 1, 'owner': 'Jande', 'title': 'Happy board'},
        {'board_id': 2, 'owner': 'Emily', 'title': 'Winter board'},
        {'board_id': 3, 'owner': 'Ivana', 'title': 'Awesome board'}]


def test_get_one_board(client, one_board):
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "board" in response_body
    assert response_body == {
        "board": {
            "board_id": 1,
            "title": "Create new board",
            "owner": "Emily",
        }
    }


def test_get_board_not_found(client):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "message": "<class 'app.models.board.Board'> 1 not found"}


def test_create_board(client):
    # Act
    response = client.post("/boards", json={
        "title": "Created a New Board",
        "owner": "Emily",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "board" in response_body
    assert response_body == {
        "board": {
            "board_id": 1,
            "title": "Created a New Board",
            "owner": "Emily",
        }
    }


def test_create_board_missing_title(client):
    # Act
    response = client.post("/boards", json={})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "details": "Invalid data"
    }


def test_update_board(client, one_board):
    # Act
    response = client.put("/boards/1", json={
        "title": "Updated Board Title",
        "owner": "Jande"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "board" in response_body
    assert response_body == {
        "board": {
            "board_id": 1,
            "title": "Updated Board Title",
            "owner": "Jande"
        }
    }
    board = Board.query.get(1)
    assert board.title == "Updated Board Title"


def test_update_board_not_found(client):
    # Act
    response = client.put("/boards/1", json={
        "title": "Updated Board Title"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "message": "<class 'app.models.board.Board'> 1 not found"}


def test_delete_board(client, one_board):
    # Act
    response = client.delete("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Board 1 "Create new board" successfully deleted'
    }


def test_delete_board_not_found(client):
    # Act
    response = client.delete("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "message": "<class 'app.models.board.Board'> 1 not found"}
    assert Board.query.all() == []


# TESTS FOR CARDS
def test_get_all_cards_for_specific_board(client, one_card_belongs_to_one_board):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [
        {
            "card_id": 1,
            "message": "New card",
            "like_count": None,
            "board_id": 1,
        }
    ]


def test_get_cards_for_specific_board_without_cards(client, one_board):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_card_for_non_existent_board(client):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "message": "<class 'app.models.board.Board'> 1 not found"}


def test_create_card_for_board_with_cards(client, one_card_belongs_to_one_board):
    # Act
    response = client.post("/boards/1/cards", json={"message": "New card"})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        'card': {
            "board": 'Create new board',
            "board_id": 1,
            "id": 2,
            "like_count": 0,
            "message": "New card"
        }
    }


def test_create_card_for_board_with_no_cards(client, one_board):
    # Act
    response = client.post("/boards/1/cards", json={"message": "New card"})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        'card': {
            "board": 'Create new board',
            "board_id": 1,
            "id": 1,
            "like_count": 0,
            "message": "New card"
        }
    }


def test_update_card_from_board(client, one_card_belongs_to_one_board):
    # Act
    response = client.patch(
        "/cards/1", json={"message": "Updated card"})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "card" in response_body
    assert response_body == {
        "card": {
            "board": 'Create new board',
            "board_id": 1,
            "id": 1,
            "like_count": None,
            "message": "Updated card",
        }
    }

    card = Card.query.get(1)
    assert card.message == "Updated card"


def test_update_card_from_board_card_not_found(client):
    # Act
    response = client.patch(
        "/cards/1", json={"message": "Updated card"})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "message": "<class 'app.models.card.Card'> 1 not found"}


def test_delete_card_from_board(client, all_cards):
    # Act
    response = client.delete("cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": "Card 1 successfully deleted"
    }
    assert Card.query.get(1) == None


def test_delete_card_from_board_card_not_found(client):
    # Act
    response = client.delete("cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "message": "<class 'app.models.card.Card'> 1 not found"}
    assert Card.query.all() == []
