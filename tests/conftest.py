
from email import message
import pytest
from app import create_app
from app.models.board import Board
from app.models.card import Card
from app import db


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

# This fixture creates a single card and saves it in the database
# References "one_card"
@pytest.fixture
def one_card(app):
    new_card = Card(
        message="Get some sunshine, its good for you!☀️ 😎 ")
    db.session.add(new_card)
    db.session.commit()


# This fixture creates a single board and saves it in the database
# References "one_board"
@pytest.fixture
def one_board(app):
    new_board = Board(
        title='camelCase Inspiration', owner="Poppy")
    db.session.add(new_board)
    db.session.commit()

# This fixture creates a single board and a single card and saves it in the database
# References "one_card_belongs_to_one_goal"
@pytest.fixture
def one_card_belongs_to_one_board(app, one_board, one_card):
    card = Card.query.first()
    board = Board.query.first()
    board.cards.append(card)
    db.session.commit()