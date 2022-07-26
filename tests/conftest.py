import pytest
from app import create_app
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
import pytest
from app import create_app
from app.models.board import Board
from app.models.card import Card
from app import db
from flask.signals import request_finished

@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

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
def one_card(app):
    db.session.add_all([
        Board(title="Share your support", owner="Shari"),
        Card(message="You can do it!", likes=0, board_id=1),
    ])
    db.session.commit()

@pytest.fixture
def three_cards(app):
    db.session.add_all([
        Board(title="Share your support", owner="Shari"),
        Card(
            message="You can do it!", likes=0, board_id=1),
        Card(
            message = "It's not that hard!", likes=0, board_id=1),
        Card(
            message = "I believe in you!", likes=0, board_id=1),
    ])
    db.session.commit()

@pytest.fixture
def one_board(app):
    new_board = Board(title="Share your support", owner="Shari")
    db.session.add(new_board)
    db.session.commit()

@pytest.fixture
def one_card_belongs_to_one_board(app, one_card):
    card = Card.query.first()
    board = Board.query.first()
    board.cards.append(card)
    db.session.commit()


