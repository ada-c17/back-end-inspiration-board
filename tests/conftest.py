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


#This fixture creates one board and saves it in the database
@pytest.fixture
def one_board(app):
    new_board = Board(title="Many Cats", owner="Julie")
    db.session.add(new_board)
    db.session.commit()


#This fixture creates three cards on board 1 and saves them in the database
@pytest.fixture
def three_cards(app):
    db.session.add_all([
        Card(message="Ink", board_id=1, likes_count=0),
        Card(message="Isaac", board_id=1,likes_count=0),
        Card(message="Annabelle", board_id=1,likes_count=0)
    ])
    db.session.commit()