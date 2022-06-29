from app.models.board import Board
import pytest

# Test GET Boards returns empty list
# @pytest.mark.skip
def test_get_tasks_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

# Test GET one Board returns Board
# @pytest.mark.skip
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
            "title": "camelCase Inspiration",
            "owner": "Poppy",
            "cards": []
        }
    ]

# Test POST one board returns Board
# @pytest.mark.skip
def test_create_board(client):
    # Act
    response = client.post("/boards", json={
        "title": "Another very inspirational board",
        "owner": "Lindsey",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "board" in response_body
    assert response_body == {
        "board": {
            "board_id": 1,
            "title": "Another very inspirational board",
            "owner": "Lindsey",
            "cards": []
        }
    }
    new_board = Board.query.get(1)
    assert new_board
    assert new_board.title == "Another very inspirational board"
    assert new_board.owner == "Lindsey"
    assert new_board.cards == []

# Test GET Cards from Board
# @pytest.mark.skip
def test_get_cards_for_specific_board(client, one_card_belongs_to_one_board):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "cards" in response_body
    assert len(response_body["cards"]) == 1
    assert response_body == {
        "board_id": 1,
        "title": "camelCase Inspiration",
        "owner": "Poppy",
        "cards": [
            {
                "card_id": 1,
                "message": "Get some sunshine, its good for you!☀️ 😎 ",
                "likes_count": 0,
                "board_id": 1
            }
        ]
    }

# Test POST Cards from Board
# @pytest.mark.skip
def test_post_card_to_board(client, one_board):
    # Act
    response = client.post("/boards/1/cards", json={
        "message": "Hi, this is a test card"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "board_id" in response_body
    assert "card_id" in response_body
    assert "likes_count" in response_body
    assert "message" in response_body
    assert response_body == {
        "board_id": 1,
        "card_id": 1,
        "likes_count": 0,
        "message": "Hi, this is a test card"
    }

    # Check that Board was updated in the db
    assert len(Board.query.get(1).cards) == 1