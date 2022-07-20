from app.models.board import Board 
from app.models.card import Card 
import pytest 

def test_get_boards_no_saved_boards(client): 
    # Act 
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [] 

# Read all boards
def test_get_boards_one_saved_board(client, one_board): 
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        { 
            "id": 1, 
            "title": "Many Cats", 
            "owner": "Julie"
        }
    ]
    
# @pytest.mark.skip(reason="Not passing - check into later")
def test_get_board(client, one_board, three_cards): 
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body[0] == {
            "board_id": 1, 
            "card_id": 1, 
            "likes_count": 0, 
            "message": "Ink"
        }
    

# Create a board
def test_create_board(client): 
    # Act
    response = client.post("/boards", json={ 
        "title": "Create Board Test", 
        "owner": "Gramtaschie"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
            "id": 1, 
            "owner": "Gramtaschie", 
            "title": "Create Board Test"
        }
    
    new_board = Board.query.get(1)
    assert new_board
    assert new_board.title == "Create Board Test"
    assert new_board.owner == "Gramtaschie"

# Delete a board
def test_delete_board(client, one_board):
    # Act 
    response = client.delete("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "details": 'Board 1 "Many Cats" successfully deleted'
    }
    assert Board.query.get(1) == None 


# Board not found
def test_board_not_found(client): 
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert len(response_body) == 1

# Create a card if there are no boards
def test_create_card_with_no_boards(client): 
    # Act
    response = client.post("/boards/0/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert len(response_body) == 1

# Create a card associated with a board
def test_create_cards_to_specific_board(client, one_board): 
    # Act
    response = client.post("/cards", json={ 
        "message": "Create Card Test", 
        "likes_count": 0, 
        "board_id": 1
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
            "card_id": 1, 
            "message": "Create Card Test", 
            "likes_count": 0, 
            "board_id": 1
        }
    
    new_card = Card.query.get(1)
    assert new_card
    assert new_card.message == "Create Card Test"
    assert new_card.likes_count == 0 

# Read cards associated with a board
# @pytest.mark.skip(reason="Not passing - doesn't like the board_id")
def test_get_cards_one__board(client, one_board,three_cards): 
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0] == { 
            "board_id": 1, 
            "card_id": 1, 
            "likes_count": 0, 
            "message": "Ink"
        }
    

#Increase the number of likes on a card
# @pytest.mark.skip(reason="Not passing - doesn't like the board_id")
def test_update_likes_on_card(client, one_board, three_cards): 
    # Act
    response = client.put("/cards/1/like", json={
        "likes_count": 5
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == {
        'msg': "Successfully updated likes of card with id 1"
    }

# Delete a card
# @pytest.mark.skip(reason="Not passing - doesn't like the board_id")
def test_delete_card(client, one_board, three_cards):
    # Act 
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "details": 'Card 1 successfully deleted'
    }
    assert Card.query.get(1) == None 

