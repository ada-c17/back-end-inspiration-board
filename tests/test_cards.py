from urllib import response
from app.models.card import Card
import pytest

def test_get_cards_no_saved_cards(client, one_board):
    # Act
    response = client.get("boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        'board_id': 1, 
        'cards': [], 
        'owner': 'Lulu', 
        'title': 'How to write a joke'
    }
    assert len(response_body['cards']) == 0


def test_get_cards_one_saved_card(client, one_board, one_card):
    # Act
    response = client.get("boards/1/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 4
    assert response_body == {
            "card_id": 1,
            "message": "Card 1",
            "likes_count": 0,
            "board_id": 1
    }


def test_get_boards_four_saved_boards(client, one_board, four_cards):
    # Act
    response = client.get("boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body['cards']) == 4
    assert response_body['cards'] == [
        {
            "card_id": 1,
            "message": "Card 1",
            "likes_count": 0,
            "board_id": 1
        },
        {
            "card_id": 2,
            "message": "Card 2",
            "likes_count": 0,
            "board_id": 1
        },
        {
            "card_id": 3,
            "message": "Card 3",
            "likes_count": 0,
            "board_id": 1
        },
        {
            "card_id": 4,
            "message": "Card 4",
            "likes_count": 0,
            "board_id": 1
        }
    ] 
    

def test_get_board_with_first_id(client, one_board, one_card):
    # Act
    response = client.get("/boards/1/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
            "card_id": 1,
            "message": "Card 1",
            "likes_count": 0,
            "board_id": 1
    }


def test_get_board_with_third_id(client, one_board, four_cards):
    # Act
    response = client.get("/boards/1/cards/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
            "card_id": 3,
            "message": "Card 3",
            "likes_count": 0,
            "board_id": 1
    }


def test_get_card_not_found(client, one_board):
    # Act
    response = client.get("boards/1/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "msg": "Could not find card with id 1"
    }


def test_create_card(client, one_board, one_card):
    # Act
    response = client.post("/boards/1/cards", json={
        "message": "Card 2",
        "likes_count": 0,
        "board_id": 1,
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
            "card_id": 2,
            "message": "Card 2",
            "likes_count": 0,
            "board_id": 1
    }
    new_card = Card.query.get(1)
    assert new_card
    assert new_card.message == "Card 1"
    assert new_card.likes_count == 0
    assert new_card.board_id == 1


def test_create_card_missing_message(client, one_board):
    # Act
    response = client.post("/boards/1/cards", json={})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "details": "Please enter a message. "
    }


def test_create_card_long_message(client, one_board):
    # Act
    response = client.post("/boards/1/cards", json={
        "message": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "details": "Please enter a message shorter than 40 characters. "
    }



def test_update_card(client, one_board, one_card):
    # Act
    response = client.patch("cards/1/like", json={})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
            "card_id": 1,
            "message": "Card 1",
            "likes_count": 1,
            "board_id": 1
    }


def test_delete_card(client, one_card):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Card 1 Card 1 successfully deleted'
    }
    assert Card.query.get(1) == None


def test_delete_task_not_found(client):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"msg": f"Could not find card with id 1"}
