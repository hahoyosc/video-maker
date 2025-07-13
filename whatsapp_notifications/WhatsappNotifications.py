import requests

def send_whatsapp_notification(whatsapp_params, match_name, drive_folder_id):
    url = "https://graph.facebook.com/" + whatsapp_params['apiVersion'] + "/" + whatsapp_params['phoneNumberId'] + "/messages"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + whatsapp_params['userAccessToken']
    }
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": "57" + whatsapp_params['recipientPhoneNumber'],
        "type": "template",
        "template": {
            "name": whatsapp_params['templateName'],
            "language": {
                "code": whatsapp_params['templateLanguageCode'],
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "parameter_name": "match_name",
                            "text": match_name
                        }
                    ]
                },
                {
                    "type": "button",
                    "sub_type": "url",
                    "index": "0",
                    "parameters": [
                        {
                            "type": "text",
                            "text": drive_folder_id
                        }
                    ]
                }
            ]
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    return response.status_code, response.json()
