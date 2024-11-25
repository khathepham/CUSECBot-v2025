import json

import requests
from requests.models import PreparedRequest
from requests.auth import HTTPBasicAuth
from infisical_sdk import InfisicalSDKClient
from dotenv import load_dotenv
import os
from typing import Optional


load_dotenv()

i_client = InfisicalSDKClient(host="https://app.infisical.com")
i_client.auth.universal_auth.login(client_id=os.environ.get("I_CLIENT_ID"),
                                   client_secret=os.environ.get("I_CLIENT_SECRET"))
i_tt_apikey = i_client.secrets.get_secret_by_name(secret_name="TICKET_TAILOR_API_KEY",
                                                  project_id="fcdb0041-ad1d-4fa6-854d-0745640829d0",
                                                  environment_slug="prod", secret_path="/")

i_event_id = i_client.secrets.get_secret_by_name(secret_name="EVENT_ID",
                                                 project_id="fcdb0041-ad1d-4fa6-854d-0745640829d0",
                                                 environment_slug="prod", secret_path="/")

tt_apikey = i_tt_apikey.secret.secret_value
event_id = i_event_id.secret.secret_value

auth = HTTPBasicAuth(tt_apikey, '')
headers = {"Accept": "application/json"}
baseurl = "https://api.tickettailor.com/v1"


class Ticket:
    def __init__(self, ticket_code: str, emails: set, first_name: str, last_name: str, custom_questions: list):
        self.ticket_code = ticket_code
        self.emails = emails
        self.first_name = first_name
        self.last_name = last_name
        self.custom_question = custom_questions

    def __str__(self):
        return f"{self.first_name} {self.last_name}: {self.ticket_code}; {self.emails}"

    @classmethod
    def create_ticket_from_json(cls, js_object: dict):
        ticket_code = js_object.get("barcode")
        emails = {str(js_object.get("email")).lower().strip()}
        first_name = js_object.get("first_name")
        last_name = js_object.get("last_name")
        custom_questions = js_object.get("custom_questions")

        for q in custom_questions:
            if q["question"] in ("What's a good personal email for you?", "What is your student email address?"):
                emails.add(str(q["answer"]).strip().lower())

        return Ticket(ticket_code, emails, first_name, last_name, custom_questions)


def get_ticket_by_ticket_code(ticket_code: str) -> Optional[Ticket]:
    if ticket_code is None or len(ticket_code) == 0:
        return None

    params = {
        "event_id": event_id,
        "barcode": ticket_code
    }
    url = f"{baseurl}/issued_tickets"
    prepared_request = PreparedRequest()
    prepared_request.prepare_url(url, params)
    prepared_url = prepared_request.url

    response = requests.get(f"{prepared_url}", headers=headers, data=params, auth=auth)
    print(json.dumps(response.json(), indent=4))

    if dict(response.json()).get("data") is not None and len(dict(response.json()).get("data")) > 0:
        ticket_json = dict(response.json()).get("data")[0]
        return Ticket.create_ticket_from_json(ticket_json)
    return None


if __name__ == '__main__':
    ticket = get_ticket_by_ticket_code("AE7anAV")
    print(ticket)