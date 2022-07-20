from urllib import response
from app.models.board import Board
import pytest


def test_get_boards_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_boards_one_saved_boards(client, one_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "board_id": 1,
            "owner": "Lulu",
            "title": "How to write a joke"
        }
    ]


def test_get_boards_four_saved_boards(client, four_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 4
    assert response_body == [
        {
            "board_id": 1,
            "owner": "First",
            "title": "Title 1"
        },
        {
            "board_id": 2,
            "owner": "Second",
            "title": "Title 2"
        },
        {
            "board_id": 3,
            "owner": "Third",
            "title": "Title 3"
        },
        {
            "board_id": 4,
            "owner": "Fourth",
            "title": "Title 4"
        }
    ]


def test_get_board_with_first_id(client, one_board): #this test were falling
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    print(response_body)
    assert "board" in response_body
    assert response_body == {
        "board": {
            "board_id": 1,
            "owner": "Lulu",
            "title": "How to write a joke"
        }
    }

def test_get_board_with_third_id(client, four_board): #this test were falling
    # Act
    response = client.get("/boards/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    print(response_body)
    assert "board" in response_body
    assert response_body == {
        "board": {
            "board_id": 3,
            "owner": "Third",
            "title": "Title 3"
        }
    }

def test_get_board_not_found_id_with_empty_db(client):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "msg" in response_body
    assert response_body ==  {"msg": "Could not find board with id 1"}
    assert Board.query.all() == []


def test_get_board_not_found_id_with_populated_db(client, one_board):
    # Act
    response = client.get("/boards/11111")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "msg" in response_body
    assert response_body ==  {"msg": "Could not find board with id 11111"}


def test_get_board_with_invalid_id_with_populated_db(client, one_board):
    # Act
    response = client.get("/boards/my_board")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "msg" in response_body
    assert response_body ==  {"msg": "Invalid id my_board"}


def test_create_board(client):
    # Act
    response = client.post("/boards", json={
        "title": "My New Board",
        "owner": "New Owner"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "board" in response_body
    assert response_body == {
        "board": {
            "board_id": 1,
            "owner": "New Owner",
            "title": "My New Board"
        }
    }


def test_create_board_missing_title(client):
    # Act
    response = client.post("/boards", json={})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }

# testing for delete one board

def test_delete_board(client, one_board):
    # Act
    response = client.delete("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Board 1 "How to write a joke" successfully deleted'
    }
    assert Board.query.get(1) == None

    # Check that the board was deleted
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 404
    assert "msg" in response_body
    assert response_body ==  {"msg": "Could not find board with id 1"}

def test_delete_board_not_found_with_empty_db(client):

    # Act
    response = client.delete("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "msg" in response_body
    assert response_body ==  {"msg": "Could not find board with id 1"}
    assert Board.query.all() == []


def test_delete_board_not_found_with_id_with_populated_db(client, one_board):
    # Act
    response = client.delete("/boards/12121")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "msg" in response_body
    assert response_body ==  {"msg": "Could not find board with id 12121"}


def test_delete_goal_not_found_invalid_id_with_populated_db(client, one_board):
    # Act
    response = client.delete("/boards/bad_board")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "msg" in response_body
    assert response_body ==  {"msg": "Invalid id bad_board"}
    