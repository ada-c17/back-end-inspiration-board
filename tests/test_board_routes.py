from app.models.board import Board
import pytest

def test_create_board(client):
    response = client.post("/boards", json={
        "title": "My New Goal",
        "owner": "NG"
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {
        "board": {
            "id": 1,
            "title": "My New Goal",
            "owner": "NG"
        }
    }

def test_create_board_missing_title(client):
    response = client.post("/boards", json={
        "owner": "NG"
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {
        "details": "missing required 'title'"}

def test_create_board_missing_owner(client):
    response = client.post("/boards", json={
        "title": "My New Goal",
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {
        "details": "missing required 'owner'"}

def test_get_boards_no_saved_boards(client):
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_boards_one_saved_board(client, one_board):
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "Dad Jokes",
            "owner": "Dad"
        }
    ]

def test_get_cards_for_specfic_board(client, three_cards_of_a_board):
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body["cards"]) == 3
    assert response_body == {
        "id": 1,
        "title": "Dad Jokes",
        "owner": "Dad",
        "cards": [
        {
            "id": 1,
            "message": "Where do fruits go on vacation? Pear-is!",
            "likes_count": 25,
            "board_id": 1
        },
        {
            "id": 2,
            "message": "You can't spell par entry without 'try.'",
            "likes_count": 0,
            "board_id": 1
        },
        {
            "id": 3,
            "message": "Two sheep walk into a—baaaa.",
            "likes_count": 0,
            "board_id": 1
        },
        ]
    }

def test_get_cards_for_specific_board_no_cards(client, one_board):
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body["cards"]) == 0
    assert response_body == {
        "id": 1,
        "title": "Dad Jokes",
        "owner": "Dad",
        "cards": []
    }

def test_get_cards_for_specific_board_no_board(client):
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {
        "details": "Board #1 is not found"
    }

def test_get_cards_for_specific_board_invalid_board(client):
    response = client.get("/boards/abc/cards")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {
        "details": "Board #abc is invalid"
    }

def test_post_one_card_to_specific_board(client, one_board):
    response = client.post("/boards/1/cards", json={"message": "No more jokes."})
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {
        "cards": {
            "id": 1,
            "message": "No more jokes.",
            "likes_count": 0,
            "board_id": 1
        }
    }

def test_post_one_card_to_specific_board_message_too_long(client, one_board):
    response = client.post("/boards/1/cards", json={"message": "How do you make holy water? Boil the hell out of it."})
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {
        "details": "message is longer than 40 characters"
    }

def test_post_one_card_to_specific_board_missing_message(client, one_board):
    response = client.post("/boards/1/cards", json={"likes_count": 1})
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {
        "details": "missing required 'message'"
    }
