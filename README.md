# Inspiration Board: Back-end Layer

This scaffold includes the following:

## `app/__init__.py`

This file configures the app. It's where:

We expect developers to modify this file by:

- Replacing the database connection string
- Importing all models
- Registering all blueprints

Note that `create_app` also uses CORS. There is no extra action needed to be done with CORS.

## `app/routes.py`

We expect endpoints to be defined here.

The file already imports:

- `Blueprint`
- `request`
- `jsonify`
- `make_response`
- `db`

Feel free to alter these import statements.

This file also has a comment to define a Blueprint. Feel free to delete it.

## `app/models` Directory

This project already includes `app/models/board.py` and `app/models/card.py`, to anticipate the models `Board` and `Card`.

Both files already import `db`, for convenience!

## `requirements.txt`

This file lists the dependencies we anticipate are needed for the project.

## `Procfile`

This file already has the contents needed for a Heroku deployment.

If the `create_app` function in `app/__init__.py` is renamed or moved, the contents of this file need to change. Otherwise, we don't anticipate this file to change.

## `Endpoints`
| Verb  | Path  | Body of Request | Body of Response | What it does  |
|---|---|---|---|---|
| `GET`  | `/boards/<board_id>`  | None | `{ "board": { "board_id": 1, "owner": "Owner 1", "title": "Title 1" } }` | Retrieves a board  |
| `GET`  | `/boards`  | None | `[ { "board_id": boardId, "owner": "ownerText", "title": "titleText" } ] `| Retrieves a list of boards  |
| `POST`  | `/boards`  | `{ "title": "titleText", owner: "ownerText" }`  | `{ "board": { "board_id": boardId, "owner": "ownerText", "title": "titleText" } }` | Creates a new board with title and owner informtion   |
| `GET`  | `/<board_id>/cards`  | None | `{ "board_id": boardId, "owner": "ownerText", "title": "titleText", "cards": [ { "board_id": boardId, "card_id": cardId, "likes_count": likesCount, "message": "messageText" }, { "board_id": boardId, "card_id": cardId, "likes_count": likesCount, "message": "messageText" } ] }` | Retrieves a list of cards under one specific board   |
| `GET`  | `/<board_id>/cards/<card_id>`  | None | `{ "board_id": boardId, "card_id": cardId, "likes_count": likesCount, "message": "messageText" }` | Retrieves one card under one specific board   |
| `POST`  | `/boards/<board_id>/cards`  | `{ "message": "messageText" }` | `{  "board_id": boardId, "card_id": cardId, "likes_count": likesCount, "message": "messageText" }` | Creates a new card   |
| `DELETE`  | `/<card_id>'`  | None | `{ "details": "Card {cardId} {messageText} successfully deleted" }` | Deletes a card |
| `PATCH`  | `/<card_id>/like`  | None | `{ "board_id": boardId, "card_id": cardId, "likes_count": likesCount, "message": "messageText" }` | Updates the like counts of a card by 1|
| `DELETE`  | `/<board_id>'`  | None | `{ "details": "Board {board_id} {board.title} successfully deleted" }` | Deletes a board |
