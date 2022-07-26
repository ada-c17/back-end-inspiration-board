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
        title="A lovely board", creator="Mysterious Being")
    db.session.add(new_board)
    db.session.commit()


@pytest.fixture
def three_boards(app):
    db.session.add_all([
        Board(
            title="A nice board", creator="Tiffini"),
        Board(
            title="A grumpy board", creator="Gelly"),
        Board(
            title="Another lovely board", creator="Danielle")
    ])
    db.session.commit()

@pytest.fixture
def one_card(app, one_board):
    board = Board.query.first()
    new_card = Card(message="You in5pire me :')", board_id=board.board_id)
    db.session.add(new_card)
    db.session.commit() 



@pytest.fixture
def three_cards(app, one_board):
    board = Board.query.first()

    db.session.add_all([
        Card(message="Wow!", board_id=board.board_id),
        Card(message="You are amazing!", board_id=board.board_id),
        Card(message="I love you!!!", board_id=board.board_id)
    ])
    db.session.commit()