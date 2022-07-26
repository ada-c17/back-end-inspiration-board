from app.models.card import Card
from app.models.board import Board

def test_get_cards_no_cards(client,one_board):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["cards"] == []


def test_get_cards(client, one_card):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert  response_body["cards"] == [{'cardId': 1, 'likesCount': 0, 'message': "You in5pire me :')"}]

def test_create_card(client, one_card):
    # Act
    response = client.post("/boards/1/cards", json={
        "message": "You in5pire me :')"
    })
    new_card = Card.query.get(1)

    # Assert
    assert response.status_code == 201
    assert new_card
    assert new_card.message == "You in5pire me :')"


def test_create_card_missing_message(client,one_board):
    # Act
    response = client.post("/boards/1/cards", json={
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body["details"] == "Missing key: 'message'"

def test_delete_card(client, three_cards):
    # Act
    response = client.delete("/boards/1/cards/1")

    # Assert
    assert response.status_code == 200
    assert len(Board.query.get(1).cards) == 2

def test_like_card(client, one_card):
    # Act
    response = client.patch("/boards/1/cards/1/like")

    # Assert
    assert response.status_code == 200
    assert Card.query.get(1).likes_count == 1










