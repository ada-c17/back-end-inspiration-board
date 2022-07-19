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

@pytest.fixture
def create_one_board(app):
    board_1 = Board(title = "My Amazing Board", owner = "User 1")

    db.session.add(board_1)
    db.session.commit()

@pytest.fixture
def create_three_boards(app):
    board_1 = Board(title = "Brand New Board", owner = "User 1")
    board_2 = Board(title = "Another Amazing Board", owner = "User 2")
    board_3 = Board(title = "The Best Board", owner = "User 3")

    db.session.add_all([board_1, board_2, board_3])
    db.session.commit()

@pytest.fixture
def add_card_to_board(app, create_one_board):
    board_1 = Board.query.get(1)
    board_1.cards.append(Card(message = "A new inspirational message"))

    db.session.commit()
