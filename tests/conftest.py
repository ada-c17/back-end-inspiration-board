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
    new_board = Board(title = 'One Board', owner = 'one_board fixture')

    db.session.add(new_board)
    db.session.commit()

@pytest.fixture
def one_board_w_three_cards(app):
    new_board = Board(title = 'One Board', owner = 'one_board fixture')
    db.session.add(new_board)
    db.session.commit()
    
    for i in range(3):
        new_card = Card(message = f'Card {i}', board_id = new_board.id)
        db.session.add(new_card)
    db.session.commit()