
*API Reference*

- [*Board routes*](#board-routes)
  - [Create New Board](#create-new-board)
  - [Get All Boards](#get-all-boards)
  - [Get One Board](#get-one-board)
  - [Update Board Details](#update-board-details)
  - [Delete Board](#delete-board)
- [*Nested Routes*](#nested-routes)
  - [Create New Card (1)](#create-new-card-1)
  - [Get All Cards of Board by Board ID](#get-all-cards-of-board-by-board-id)
  - [Delete All Cards of Board by Board ID](#delete-all-cards-of-board-by-board-id)
- [*Card Routes*](#card-routes)
  - [Create New Card (2)](#create-new-card-2)
  - [Update Card Details](#update-card-details)
  - [Delete Card](#delete-card)

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
        "board_id": integer,
        "title": string,
        "owner": string,
        "cards": array []
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
            "board_id": integer,
            "title": string,
            "owner": string,
            "cards": array [
                {
                    "card_id": integer,
                    "message": string,
                    "likes_count": integer,
                    "board_id": integer
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
        "board_id": integer,
        "title": string,
        "owner": string,
        "cards": array [
            {
                "card_id": integer,
                "message": string,
                "likes_count": integer,
                "board_id": integer
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
        "board_id": integer,
        "owner": string,
        "title": string
        "cards": array [
            {
                "card_id": integer,
                "likes_count": integer,
                "message": string,
                "board_id": integer
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

# *Nested Routes*

## Create New Card (1)

**Endpoint:** POST '/boards/(board_id)/cards'

**Request body:** JSON object 

`{ "message": string }`

**Response body:** JSON object

```
{
    "message": string (success/error message),
    "card": {
        "card_id": integer,
        "message": string,
        "likes_count": integer,
        "board_id": integer
    }
}
```

---

## Get All Cards of Board by Board ID

**Endpoint:** GET '/boards/(id)/cards

**Request body:** N/A

**Response body:** JSON object
```
{
    "cards": [
        {
            "board_id": integer,
            "card_id": integer,
            "likes_count": integer,
            "message": string
        },
        ...
    ]
}
```

---

## Delete All Cards of Board by Board ID

**Endpoint:** DELETE '/boards/(id)/cards'

**Request body:** N/A 

**Response body:**  JSON object

`{ "message": string (success/error message) }`

# *Card Routes*

## Create New Card (2)

**Endpoint:** POST '/cards'

**Request body:** JSON object 

`{ "message": string, "board_id": integer }`

| *Request JSON must contain 'board_id' value when creating by this route*

**Response body:** JSON object

```
{
    "message": string (success/error message),
    "card": {
        "card_id": integer,
        "message": string,
        "likes_count": integer,
        "board_id": integer
    }
}
```

---

## Update Card Details

**Endpoint:** PATCH '/cards/(id)'

**Request body:** JSON object 

`{ "message": string, "likes_count": integer }`

| *JSON can contain one of 'message' or 'likes_count' keys, or both*

**Response body:** JSON object
```
{
    "message": string (success/error message),
    "card": {
        "card_id": integer,
        "likes_count": integer,
        "message": string,
        "board_id": integer
    }
}
```

---

## Delete Card

**Endpoint:** DELETE '/cards/(id)'

**Request body:** N/A 

**Response body:** JSON object

`{ "message": string (success/error message) }`

