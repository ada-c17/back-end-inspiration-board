from app.models.board import Card
import pytest

# Test DELETE a card
# @pytest.mark.skip
def test_delete_card(client, one_card):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Card 1 successfully deleted'
    }
    assert Card.query.get(1) == None

# Test UPDATE a cards like count
# @pytest.mark.skip
def test_update_likes_on_card(client, one_card):
    # Act
    response = client.put("/cards/1/like", json={
        "likes_count": 4
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert "card" in response_body
    assert response_body == {
        "card": {
            "board_id": None,
            "card_id": 1,
            "likes_count": 4,
            "message": "Get some sunshine, its good for you!☀️ 😎 "
        }
    }