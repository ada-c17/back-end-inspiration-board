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
    new_board = Board(
        title="Create new board", owner="Emily")
    db.session.add(new_board)
    db.session.commit()


@pytest.fixture
def all_boards(app):
    board1 = Board(
        title="Happy board", owner="Jande")
    board2 = Board(
        title="Winter board", owner="Emily")
    board3 = Board(
        title="Awesome board", owner="Ivana")
    db.session.add_all([board1, board2, board3])
    db.session.commit()


# Fixtures for Cards
@pytest.fixture
def one_card(app):
    new_card = Card(
        message="New card")
    db.session.add(new_card)
    db.session.commit()


@pytest.fixture
def all_cards(app, one_board):
    board = Board.query.first()
    card1 = Card(
        message="Jande's card")
    card2 = Card(
        message="Emily's card")
    card3 = Card(
        message="Ivana's card")
    board.cards.append(card1)
    board.cards.append(card2)
    board.cards.append(card3)
    db.session.commit()


@pytest.fixture
def one_card_belongs_to_one_board(app, one_board, one_card):
    card = Card.query.first()
    board = Board.query.first()
    board.cards.append(card)
    db.session.commit()
