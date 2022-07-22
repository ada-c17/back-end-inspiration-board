import pytest
from app import create_app
from app.models.card import Card
from app.models.board import Board
from app import db


@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})

    # @request_finished.connect_via(app)
    # def expire_session(sender, response, **extra):
    #     db.session.remove()

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
        title="This is a test board", owner="SSH Conftest")
    db.session.add(new_board)
    db.session.commit()

# This fixture gets called in every test that
# references "one_card"
# This fixture creates a card and saves it in the database
@pytest.fixture
def one_card(app):
    new_card = Card(
        message="This is a test card", likes_count=0)
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
            board_id=1, message="This is a test card", likes_count=0),
        Card(
            board_id=1, message="This is a second test card", likes_count=0),
        Card(
            board_id=1, message="This is a third test card", likes_count=0)
    ])
    db.session.commit()