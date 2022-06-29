from flask import abort, make_response
import requests
import os 

def validate_model_instance(cls, model_id, class_name_string):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{class_name_string} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)    
    if not model: 
        return abort(make_response({"message":f"{class_name_string} {model_id} not found"}, 404))
        
    return model

def send_slack_new_card_message(new_card):

    PATH = "https://slack.com/api/chat.postMessage"

    BEARER_TOKEN = os.environ.get(
            "AUTH_TOKEN_SLACK")

    query_params = {"channel" : "inspir-adies", "text": f"Someone just created the card with the message '{new_card.message}'" }
    headers = {"authorization" : BEARER_TOKEN}
    
    response_body = requests.get(PATH, params=query_params, headers=headers)