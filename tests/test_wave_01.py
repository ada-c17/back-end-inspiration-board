from app.models.card import Card
import pytest


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_cards_no_saved_cards(client):
    # Act
    response = client.get("/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_cards_one_saved_cards(client, one_card):
    # Act
    response = client.get("/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "message": "You can do it!",
            "likes_count": 0,
        }
    ]


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_card(client, one_card):
    # Act
    response = client.get("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "card" in response_body
    assert response_body == {
        {
            "id": 1,
            "message": "You can do it!",
            "likes_count": 0,
        }
    }


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_card_not_found(client):
    # Act
    response = client.get("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == 'Card 1 not found'

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_card(client):
    # Act
    response = client.post("/cards", json={
        "message": "I believe in you!",
        "likes_count": 0,
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "message": "I believe in you!",
        "likes_count": 0,
        }
    
    new_card = Card.query.get(1)
    assert new_card
    assert new_card.title == "I believe in you!"
    assert new_card.likes_count == 0


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_update_card(client, one_card):
    # Act
    response = client.put("/cards/1", json={
        "message": "I believe in you!",
        "likes_count": 1,
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "card" in response_body
    assert response_body == {
        "id": 1,
        "message": "I believe in you!",
        "likes_count": 1,
        }
    card = Card.query.get(1)
    assert card.message == "I believe in you!"
    assert card.likes_count == 1

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_update_card_not_found(client):
    # Act
    response = client.put("/cards/1", json={
        "message": "This card is magic. It has disappeared!",
        "likes_count": "0",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == 'Card 1 not found'

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_card(client, one_card):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "message": 'Card "I believe in you!" successfully deleted'
    }
    assert Card.query.get(1) == None


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_card_not_found(client):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == 'Card 1 not found'

    assert Card.query.all() == []


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_card_must_contain_message(client):
    # Act
    response = client.post("/cards", json={
        "message": "I still believe in you!"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "message": "You must include a message"
    }
    assert Card.query.all() == []


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_card_must_contain_likes_count(client):
    # Act
    response = client.post("/cards", json={
        "message": "I still believe in you!"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "message": "Invalid data. Likes count needed."
    }
    assert Card.query.all() == []

# Added test to cover Bad Requests
def test_get_card_bad_data(client):
    # Act
    response = client.get("/cards/SSH")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        'message': 'Invalid data. ID must be numeric.'
    }