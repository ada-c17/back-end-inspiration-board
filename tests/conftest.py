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


# This fixture should be called in every test that references "one_board"
# It creates a board and saves it in the database
@pytest.fixture
def one_board(app):
    new_board = Board(title="Motivational Quotes", owner="Nostalgia")
    db.session.add(new_board)
    db.session.commit()


# This fixtue gets called in every test that references "one_card"
# It creates a card and associate it to one_board
@pytest.fixture
def one_card(app, one_board):
    board = Board.query.first()
    new_card = Card(message="Motivation is what gets you started. Habit is what keeps you going", board_id=board.board_id)
    db.session.add(new_card)
    db.session.commit()