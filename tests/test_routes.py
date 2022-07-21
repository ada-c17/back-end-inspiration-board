import pytest
from app.models.board import Board
from app.models.card import Card

#Board tests:

def test_get_one_saved_board_no_cards(client, one_board_no_cards):
    #Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert "board" in response_body

def test_get_board_not_found(client):
    #Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 404
    assert response_body == {"details": "Board id: 1 not found"}

def test_get_boards_no_boards(client):
    #Act
    response = client.get("/boards")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_one_board_with_cards(client, one_board_no_cards):
    #Arrange
    card_1 = {
            "message": "The woods are lovely, dark and deep..."
        }
    card_2 = {
            "message": "Las ramas de los árboles están envueltas en fundas de hielo."
        }

    #Act
    client.post("/boards/1/cards", json=card_1)
    client.post("/boards/1/cards", json=card_2)

    response = client.get("/boards/1")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert response_body["board"]["title"] == "Winter"
    assert response_body["board"]["owner"] == "Lili"
    assert response_body["board"]["cards"] == [
        {
            "board_id": 1,
            "card_id": 1,
            "likes_count": 0,
            "message": "The woods are lovely, dark and deep..."
        },
        {
            "board_id": 1,
            "card_id": 2,
            "likes_count": 0,
            "message": "Las ramas de los árboles están envueltas en fundas de hielo."
        }
    ]

def test_get_two_boards_no_cards(client, two_boards_no_cards):
    response = client.get("/boards")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["title"] == "Winter"
    assert response_body[0]["owner"] == "Lili"
    assert response_body[0]["cards"] == []
    assert response_body[1]["title"] == "Spring"
    assert response_body[1]["owner"] == "Adriana"
    assert response_body[1]["cards"] == []

def test_get_cards_for_board_with_no_cards_returns_empty_list(client, one_board_no_cards):
    response = client.get("/boards/1")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert response_body["board"]["cards"] == []

def test_get_cards_for_board_with_2_cards(client, one_board_no_cards):
    #Arrange
    card_1 = {
            "message": "The woods are lovely, dark and deep..."
        }
    card_2 = {
            "message": "Las ramas de los árboles están envueltas en fundas de hielo."
        }

    #Act
    client.post("/boards/1/cards", json=card_1)
    client.post("/boards/1/cards", json=card_2)

    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert "cards" in response_body
    assert len(response_body["cards"]) == 2
    assert response_body["cards"] == [
        {
            "board_id": 1,
            "card_id": 1,
            "likes_count": 0,
            "message": "The woods are lovely, dark and deep..."
        },
        {
            "board_id": 1,
            "card_id": 2,
            "likes_count": 0,
            "message": "Las ramas de los árboles están envueltas en fundas de hielo."
        }
    ]

def test_get_cards_from_nonexistant_board_returns_error_board_id_not_found(client):
    #Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    #Assert
    assert "details" in response_body
    assert response_body["details"] == "Board id: 1 not found"

def test_get_cards_with_invalid_id_returns_error(client):
    #Act
    response = client.get("/boards/a/cards")
    response_body = response.get_json()

    #Assert
    assert "details" in response_body
    assert response_body["details"] == "Invalid id: a"

#Card tests
def test_create_card(client, one_board_no_cards):
    #Act
    response = client.post("/boards/1/cards", json={
        "message": "Peppermint mocha, yum"
    })
    response_body = response.get_json()

    #Assert
    assert response.status_code == 201
    assert response_body == "Card created successfully"

    new_card = Card.query.get(1)
    assert new_card
    assert new_card.message == "Peppermint mocha, yum"
    assert new_card.likes_count == 0

def test_create_card_invalid_data(client, one_board_no_cards):
    #Act
    response = client.post("/boards/1/cards", json={
        "messag": "Peppermint mocha, yum"
    })
    response_body = response.get_json()

    #Assert
    assert response.status_code == 400
    assert response_body == {"details": "Message not found"}

def test_increase_card_likes(client, one_board_no_cards):
    #Arrange
    card_1 = {
            "message": "The woods are lovely, dark and deep..."
        }
    client.post("/boards/1/cards", json=card_1)
    #Act
    patch_request_body = {"likes_count":3}
    response = client.patch("/cards/1", json=patch_request_body)

    response_body = response.get_json()

    assert "card" in response_body
    assert response_body == {
        "card" : {
            "board_id": 1,
            "card_id": 1,
            "likes_count": 3,
            "message": "The woods are lovely, dark and deep..."
        }
    }

def test_delete_card(client, one_board_two_cards):
    #Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert response_body == {'details': 'Card 1 "The woods are lovely, dark and deep..." successfully deleted'}

    assert Card.query.get(1) == None