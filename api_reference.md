
*API Reference*

- [*Board routes*](#board-routes)
  - [Create New Board](#create-new-board)
  - [Get All Boards](#get-all-boards)
  - [Get One Board](#get-one-board)
  - [Update Board Details](#update-board-details)
  - [Delete Board](#delete-board)
- [*Card Routes*](#card-routes)
  - [Create New Card](#create-new-card)
  - [Update Card Details](#update-card-details)
  - [Delete Card](#delete-card)
  - [Delete All Cards of Board (?)](#delete-all-cards-of-board-)

---

# *Board routes*

## Create New Board

**Endpoint:** POST '/boards'

**Request body:** JSON object 

`{ "title": string, "owner": string }`

| *Both title and owner are required to not be empty for successful creation.*

**Response body:** JSON object
```
{
    "message": string (success/error message),
    "board": {
        "id": integer,
        "title": string,
        "owner": string
    }
}
```  

---

## Get All Boards

**Endpoint:** GET '/boards'

**Request body:** N/A

**Response body:** JSON array 
```
{
    "boards": array [ 
        {
            "id": integer,
            "title": string,
            "owner": string,
            "cards": array [
                {
                    "id": integer,
                    "message": string,
                    "likes_count": integer
                },
                ...
            ]
        }, 
        ...
    ]
}
```

---

## Get One Board 

**Endpoint:** GET '/boards/(id)'

**Request body:** N/A

**Response body:** JSON object
```
{
    "board": {
        "id": integer,
        "title": string,
        "owner": string,
        "cards": array [
            {
                "id": integer,
                "message": string,
                "likes_count": integer
            },
            ...
        ]
    }
}
```

---

## Update Board Details

**Endpoint:** PATCH '/boards/(id)'

**Request body:** JSON object 

`{ "title": string, "owner": string }`

| *JSON can contain one of 'title' or 'owner' keys, or both.*

**Response body:** JSON object
```
{
    "message": string (success/error message),
    "board": {
        "id": integer,
        "owner": string,
        "title": string
        "cards": array [
            {
                "id": integer,
                "likes_count": integer,
                "message": string
            },
            ...
        ]
    }
}
```

---

## Delete Board

**Endpoint:** DELETE '/boards/(id)'

**Request body:** N/A

**Response body:** JSON object

`{ "message": string (success/error message) }`

---

# *Card Routes*

## Create New Card

**Endpoint:** POST '/boards/(board_id)/cards'

**Request body:** JSON object 

`{ "message": string }`

**Response body:** JSON object

```
{
    "message": string (success/error message),
    "card": {
        "id": integer,
        "message": string,
        "likes_count": integer
    }
}
```

---

## Update Card Details

**Endpoint:** PATCH '/boards/(board_id)/cards/(card_id)'

**Request body:** JSON object 

`{ "message": string, "likes_count": integer }`

| *JSON can contain one of 'message' or 'likes_count' keys, or both*

**Response body:** JSON object
```
{
    "message": string (success/error message),
    "card": {
        "id": integer,
        "likes_count": integer,
        "message": string
    }
}
```

---

## Delete Card

**Endpoint:** DELETE '/boards/(board_id)/cards/(card_id)'

**Request body:** N/A 

**Response body:** JSON object

`{ "message": string (success/error message) }`

---

## Delete All Cards of Board (?)

**Endpoint:** DELETE '/boards/(board_id)/cards'

**Request body:** N/A 

**Response body:** String with success message. 