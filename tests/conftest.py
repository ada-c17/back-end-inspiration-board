import pytest
from app import create_app
from app import db
from app.models.board import Board
from app.models.card import Card


@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

# This fixture gets called in every test that
# references "one_board"
# This fixture creates a board and saves it in the database
@pytest.fixture
def one_board(app):
    new_board = Board(owner="Lulu", title="How to write a joke")
    db.session.add(new_board)
    db.session.commit()


# This fixture gets called in every test that
# references "four_board"
# This fixture creates a board and saves it in the database
@pytest.fixture
def four_board(app):
    db.session.add_all([
        Board(
            owner="First", title="Title 1"),
        Board(
            owner="Second", title="Title 2"),
        Board(
            owner="Third", title="Title 3"),
        Board(
            owner="Fourth", title="Title 4")
    ])
    db.session.commit()


# This fixture gets called in every test that
# references "one_card"
# This fixture creates a card and saves it in the database
@pytest.fixture
def one_card(app, one_board):
    new_card = Card(message="Card 1", likes_count=0, board_id=1)
    db.session.add(new_card)
    db.session.commit()



# This fixture gets called in every test that
# references "four_board"
# This fixture creates a board and saves it in the database
@pytest.fixture
def four_cards(app):
    db.session.add_all([
        Card(message="Card 1", likes_count=0, board_id=1),
        Card(message="Card 2", likes_count=0, board_id=1),
        Card(message="Card 3", likes_count=0, board_id=1),
        Card(message="Card 4", likes_count=0, board_id=1)
    ])
    db.session.commit()
