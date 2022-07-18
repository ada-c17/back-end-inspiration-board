import pytest 

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


# Test for Get one board
    # Test that you get 404 error if board does not exist
# Test for deleting one board
    # Test that you get 404 error if board does not exist
# Test for Making a new board (with existing entries, and w/o?)
    # Test that 400 error is raised if invalid data is passed (so missing owner or title)

# Maybe test for creating a new card associated w/ a board
