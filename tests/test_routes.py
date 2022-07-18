import pytest 
from app.models.board import Board

def test_get_all_boards_no_records(client):
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_all_boards(client, create_three_boards):
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert {"id": 1, "title": "Brand New Board", "owner": "User 1"} in response_body
    assert {"id": 2, "title": "Another Amazing Board", "owner": "User 2"} in response_body
    assert {"id": 3, "title": "The Best Board", "owner": "User 3"} in response_body

def test_get_one_board(client, create_three_boards):
    response = client.get("/boards/2")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {"id": 2, 
                            "title": "Another Amazing Board",
                            "owner": "User 2", 
                            "cards": []}

def test_get_board_that_doesnt_exist(client):
    response = client.get("/boards/100")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": "board 100 not found"}

def test_delete_board(client, create_three_boards):
    response = client.delete("/boards/1")
    response_body = response.get_json()

    boards = Board.query.all()

    assert response.status_code == 200
    assert response_body == {"details": "board id:1, title:Brand New Board, owner:User 1 successfully deleted"}
    assert Board.query.get(1) == None
    assert len(boards) == 2

def test_delete_board_that_doesnt_exist(client):
    response = client.delete("/boards/100")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": "board 100 not found"}

# Test for deleting one board
    # Test that you get 404 error if board does not exist
# Test for Making a new board (with existing entries, and w/o?)
    # Test that 400 error is raised if invalid data is passed (so missing owner or title)

# Maybe test for creating a new card associated w/ a board
