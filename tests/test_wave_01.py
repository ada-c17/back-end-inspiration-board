from app.models.card import Card
from app.models.board import Board
import pytest


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_boards_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


# # @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_boards_one_saved_board(client, one_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "board_id": 1,
            "title": "This is a test board",
            "owner": "SSH Conftest",
        }
    ]

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_board(client):
    # Act
    response = client.post("/boards", json={
        "title": "A Brand New Board",
        "owner": "SSH Conftest",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "board" in response_body
    assert response_body == {
        "board": {
            "board_id": 1,
            "title": "A Brand New Board",
            "owner": "SSH Conftest"
        }
    }
    new_board = Board.query.get(1)
    assert new_board
    assert new_board.title == "A Brand New Board"
    assert new_board.owner == "SSH Conftest"

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_specific_board(client, one_board):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "board" in response_body
    assert response_body == {
        "board": {
            "board_id": 1,
            "title": "This is a test board",
            "owner": "SSH Conftest"
        }
    }

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_specific_board(client, one_board):
    # Act
    response = client.delete("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {'details': 'Board 1 "This is a test board" successfully deleted'}

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_card_for_board(client, one_board):
    # Act
    response = client.post("/boards/1/cards", json={
        "message": "A New Card for this Board",
        "likes_count": 0
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "board_id": '1',
        "title": "This is a test board",
        "owner": "SSH Conftest",
        "card_id": 1,
        "message": "A New Card for this Board",
        "likes_count": 0
        }

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_cards_for_board(client, one_board, three_cards):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response_body == [
    {
        "card_id": 1,
        "likes_count": 0,
        "message": "This is a test card"
    },
    {
        "card_id": 2,
        "likes_count": 0,
        "message": "This is a second test card"
    },
    {
        "card_id": 3,
        "likes_count": 0,
        "message": "This is a third test card"
    }
]

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_board_not_found(client):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == "board not found"

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_board_bad_data(client):
    # Act
    response = client.get("/boards/ssh")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        'details': 'invalid id: ssh'
    }

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_patch_card_update_likes(client, one_card):
    # Act
    response = client.patch("cards/1?likes_count=5")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
            "card_id": 1, 
            "likes_count": 5,
            "message": "This is a test card"
    }

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_patch_card_bad_data(client, one_card):
    # Act
    response = client.patch("/cards/ssh")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        'details': 'invalid id: ssh'
    }

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_specific_card(client, one_card):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {'details': 'Card 1 "This is a test card" successfully deleted'}