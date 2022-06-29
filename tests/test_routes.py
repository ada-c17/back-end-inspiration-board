from app.models.board import Board
from app.models.card import Card
import pytest


def test_get_board_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []



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
            "title": "Go on my daily walk 🏞",
            "owner": "Morgan"
        }
    ]


def test_get_board_not_found(client):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message":f"item 1 not found"}
    


def test_create_board(client):
    # Act
    response = client.post("/boards", json={
        "title": "A Brand New Board",
        "owner": "Emily"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == "New board #1 successfully created"
    new_board = Board.query.get(1)
    assert new_board


def test_update_board(client, one_board):
    # Act
    response = client.put("/boards/1", json={
        "title": "Updated Board Title",
        "owner": "Gaby",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        'msg': 'Successfully updated board 1'
    }
    board = Board.query.get(1)
    assert board

def test_update_board_not_found(client):
    # Act
    response = client.put("/boards/1", json={
        "title": "Updated Board Title",
        "owner": "Team Sunshine Member",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        'message': 'item 1 not found'
    }



def test_delete_board(client, one_board):
    # Act
    response = client.delete("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Board 1 "Go on my daily walk 🏞" successfully deleted'
    }
    assert Board.query.get(1) == None


def test_delete_board_not_found(client):
    # Act
    response = client.delete("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        'message': 'item 1 not found'
    }
    assert Board.query.all() == []


# #@pytest.mark.skip(reason="No way to test this feature yet")
# def test_create_board_must_contain_title(client):
#     # Act
#     response = client.post("/boards", json={
#         "owner": "Test Description"
#     })
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 400
#     assert "details" in response_body
#     assert response_body == {
#         "details": "Invalid data"
#     }
#     assert Board.query.all() == []


# #@pytest.mark.skip(reason="No way to test this feature yet")
# def test_create_board_must_contain_owner(client):
#     # Act
#     response = client.post("/boards", json={
#         "title": "A Brand New Board"
#     })
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 400
#     assert "details" in response_body
#     assert response_body == {
#         "details": "Invalid data"
#     }
#     assert Board.query.all() == []
