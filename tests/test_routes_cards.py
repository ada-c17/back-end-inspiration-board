from app.models.card import Card
import pytest

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_update_card(client, one_card):
    # Act
    response = client.put("/cards/1", json={
        "message": "Updated card Title",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "card" in response_body
    assert response_body == {
        "card": {
            "id": 1,
            "message": "Updated card Title",
            "likes_count": 0
        }
    }
    card = Card.query.get(1)
    assert card.message == "Updated card Title"
    assert card.likes_count == 0


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_update_card_not_found(client):
    # Act
    response = client.put("/cards/1", json={
        "title": "Updated card Title"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body=={"message": "card 1 not found"}


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_card(client, one_card):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'card 1 "Be happy" successfully deleted'
    }
    assert Card.query.get(1) == None


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_card_not_found(client):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body=={"message": "card 1 not found"}
    assert Card.query.all() == []



# @pytest.mark.skip(reason="No way to test this feature yet")
def test_update_cards_likes(client, one_card):
    # Act
    response = client.put("/cards/1/like")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "card" in response_body
    assert response_body == {
        "card": {
            "id": 1,
            "message": "Be happy",
            "likes_count": 1
        }
    }
    card = Card.query.get(1)
    assert card.message == "Be happy"
    assert card.likes_count == 1