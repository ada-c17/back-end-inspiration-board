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

# This fixture creates one board and saves it in the database
@pytest.fixture
def one_board_no_cards(app):
    new_board = Board(
        title="Winter", owner= "Lili"
    )
    db.session.add(new_board)
    db.session.commit()

# This fixture creates two boards with no cards and saves them in the database
@pytest.fixture
def two_boards_no_cards(app):
    new_board_1 = Board(
        title="Winter", owner= "Lili"
    )
    new_board_2 = Board(
        title="Spring", owner="Adriana"
    )
    db.session.add(new_board_1)
    db.session.add(new_board_2)
    db.session.commit()

@pytest.fixture
def one_board_two_cards(app):
    new_board_1 = Board(
        title="Winter", owner="Lili"
    )
    new_board_2 = Board(
        title="Spring", owner="Adriana"
    )
    db.session.add(new_board_1)
    db.session.add(new_board_2)
    db.session.commit()
    
    new_card_1 = Card(
        message="The woods are lovely, dark and deep...",
        likes_count= 0,
        board_id= 1
    )
    new_card_2 = Card(
        message= "Las ramas de los árboles están envueltas en fundas de hielo.",
        likes_count= 0,
        board_id= 1 
    )
    db.session.add(new_card_1)
    db.session.add(new_card_2)
    db.session.commit()