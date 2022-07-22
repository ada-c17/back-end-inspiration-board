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
def one_board(app):
    new_board = Board(title="Dad Jokes", owner="Dad")
    db.session.add(new_board)
    db.session.commit()

@pytest.fixture
def three_cards(app):
    db.session.add_all([
        Card(message="Where do fruits go on vacation? Pear-is!", likes_count=25),
        Card(message="You can't spell par entry without 'try.'"),
        Card(message="Two sheep walk into a—baaaa.")
    ])
    db.session.commit()

@pytest.fixture
def three_cards_of_a_board(app, one_board, three_cards):
    board = Board.query.first()
    cards = Card.query.all()
    for card in cards:
        board.cards.append(card)
    db.session.commit()

@pytest.fixture
def one_card(app):
    new_card = Card(message="Live every day like it is your last.")
    db.session.add(new_card)
    db.session.commit()

@pytest.fixture
def one_popular_card(app):
    new_card = Card(message="Where do fruits go on vacation? Pear-is!", likes_count=25)
    db.session.add(new_card)
    db.session.commit()
