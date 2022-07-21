from app.models.card import Card
import pytest

def test_delete_card(client, one_card):
    response = client.delete("/cards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Card #1 "Live every day like it is your last." successfully deleted'
    }

    response = client.get("/goals/1")
    assert response.status_code == 404

def test_delete_card_not_found(client):
    response = client.delete("/cards/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"details": "Card #1 is not found"}
    assert Card.query.all() == []
