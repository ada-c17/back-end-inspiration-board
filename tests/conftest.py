import pytest
from app import create_app
from app import db
from app.models.board import Board
from app.models.card import Card
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


# This fixture gets called in every test that
# references "one_card"
# This fixture creates a card and saves it in the database
@pytest.fixture
def one_card(app):
    new_card = Card(
        message="Be happy", likes_count=0)
    db.session.add(new_card)
    db.session.commit()


# This fixture gets called in every test that
# references "three_cards"
# This fixture creates three cards and saves
# them in the database
@pytest.fixture
def three_cards(app):
    db.session.add_all([
        Card(
            message="You are otterly amazing", likes_count=0),
        Card(
            message="Life is beautiful", likes_count=1),
        Card(
            message="You can do it", likes_count=2)
    ])
    db.session.commit()



# This fixture gets called in every test that
# references "one_board"
# This fixture creates a board and saves it in the database
@pytest.fixture
def one_board(app):
    new_board = Board(title= "Ada is great", owner= "Nina")
    db.session.add(new_board)
    db.session.commit()


# This fixture gets called in every test that
# references "one_card_belongs_to_one_board"
# This fixture creates a card and a board
# It associates the board and card, so that the
# board has this card, and the card belongs to one board
@pytest.fixture
def one_card_belongs_to_one_board(app, one_board, one_card):
    card = Card.query.first()
    board = Board.query.first()
    board.cards.append(card)
    db.session.commit()