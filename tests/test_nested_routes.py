# NESTED ROUTE TESTS

def test_get_cards_by_board_id(client, one_board_w_three_cards):
    response = client.get('/boards/1/cards')
    response_body = response.get_json()

    assert response.status_code == 200
    assert 'cards' in response_body
    assert len(response_body['cards']) == 3