from app.models.board import Board

def test_get_all_boards_no_boards(client):
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
            "boardId": 1,
            "cards" : [],
            "title" : "A lovely board", 
            "creator" : "Mysterious Being"
        }
    ]


def test_get_boards_three_saved_boards(client, three_boards):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "boardId": 1,
            "cards" : [],
            "title" : "A nice board", 
            "creator" : "Tiffini"
        },
        {
            "boardId": 2,
            "cards" : [],
            "title" : "A grumpy board", 
            "creator" : "Gelly"
        },
        {
            "boardId": 3,
            "cards" : [],
            "title" : "Another lovely board", 
            "creator" : "Danielle"
        }
    ]

def test_get_board_by_id(client, one_board):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
            "boardId": 1,
            "cards" : [],
            "title" : "A lovely board", 
            "creator" : "Mysterious Being"
        }

def test_get_board_not_found(client):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "details" in response_body
    assert response_body["details"] == "No model of type <class 'app.models.board.Board'> with id 1 found"

def test_create_board(client):
    # Act
    response = client.post("/boards", json={
        "title": "A Brand New Board",
        "creator": "A brand new person",
    })

    # Assert
    assert response.status_code == 201
    new_board = Board.query.get(1)
    assert new_board
    assert new_board.title == "A Brand New Board"
    assert new_board.creator == "A brand new person"
    assert new_board.cards == []
