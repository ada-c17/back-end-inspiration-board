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
    new_board = Board(
        title="A lovely board", creator="Mysterious Being")
    db.session.add(new_board)
    db.session.commit()

# This fixture gets called in every test that
# references "three_boards"
# This fixture creates three tasks and saves
# them in the database
@pytest.fixture
def three_boards(app):
    db.session.add_all([
        Board(
            title="A nice board", creator="Tiffini"),
        Board(
            title="A grumpy board", creator="Gelly"),
        Board(
            title="Another board", creator="Danielle")
    ])
    db.session.commit()

@pytest.fixture
def one_card(app):
    new_card = Card(message="You in5pire me :')")
    db.session.add(new_card)
    db.session.commit()

@pytest.fixture
def one_card_belongs_to_one_board(app, one_card, one_board):
    board = Board.query.first()
    card = Card.query.first()
    board.cards.append(card)
    db.session.commit()