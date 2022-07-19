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
    response = client.get("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": "board 1 not found"}

def test_delete_board(client, create_three_boards):
    response = client.delete("/boards/1")
    response_body = response.get_json()

    boards = Board.query.all()

    assert response.status_code == 200
    assert response_body == {"details": "board id:1, title:Brand New Board, owner:User 1 successfully deleted"}
    assert Board.query.get(1) == None
    assert len(boards) == 2

def test_delete_board_that_doesnt_exist(client):
    response = client.delete("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": "board 1 not found"}

def test_create_board(client):
    response = client.post("/boards", json = {"owner": "New User", "title": "My New Inspiration Board"})
    response_body = response.get_json()
    
    boards = Board.query.all()
    new_board = Board.query.get(1)

    assert response.status_code == 201
    assert response_body == {"board":{
            "id": 1,
            "title": "My New Inspiration Board",
            "owner": "New User",
        }}
    assert len(boards) == 1
    assert new_board.title == "My New Inspiration Board"
    assert new_board.owner == "New User"

def test_create_board_must_contain_owner(client):
    response = client.post("/boards", json = {"title": "My New Inspiration Board"})
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"details":"Invalid data"}
    assert Board.query.all() == []

def test_create_board_must_contain_title(client):
    response = client.post("/boards", json = {"owner": "New User"})
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"details":"Invalid data"}
    assert Board.query.all() == []

# Maybe test for creating a new card associated w/ a board
def test_create_card_on_board(client, create_one_board):
    response = client.post("/boards/1/cards", json = {"message": "Keep trying"})
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {
            "id": 1,
            "message": "Keep trying",
            "likes_count": 0,
        }
    assert len(Board.query.get(1).cards) == 1


def test_create_card_on_board_that_doesnt_exist(client):
    response = client.post("/boards/1/cards", json = {"message": "Keep trying"})
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": f"board 1 not found"}

def test_create_card_on_board_must_contain_message(client, create_one_board):
    response = client.post("/boards/1/cards", json = {})
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"details":"Invalid data"}
    assert Board.query.get(1).cards == []

def test_create_card_on_board_already_has_other_card(client, add_card_to_board):
    response = client.post("/boards/1/cards", json = {"message": "Keep trying"})
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {
            "id": 2,
            "message": "Keep trying",
            "likes_count": 0,
        }
    assert len(Board.query.get(1).cards) == 2
