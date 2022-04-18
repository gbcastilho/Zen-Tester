import requests as req
from zenpy import Zenpy

from zen_tester import comment_message_from_zendesk_ticket

ATTEMPTS = 3

# ClassApp connection credentials
URL = "http://localhost:2000/graphql"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer d5e151629738fa0aa0cafdbbe14ced2c1b7b24d7a7429036082db7e0d579",
}
QUERYSTRING = {
    "client_id": "ZmYyYWM3M2JmYjkxY2IwZWJhNzlhZjcw",
    "tz_offset": "-180",
    "locale": "en",
}

# Zendesk API credentials
ZENPY_CREDS = {
    "email": "gabriel.mazzeu+zen01@classapp.com.br",
    "token": "5cQ9NY7g9xBa5NzPJifwxuGFzqL0lt2aIT80YNHa",
    "subdomain": "d3v-ca00001",
}


def create_message_to_zendesk_integrated(file, request_id):
    """
    Make CreateMassage request and store the result in a file
    """

    query = "mutation createMessage($createMessageMutation: CreateMessageInput!) {\n  createMessage(input: $createMessageMutation) {\n    clientMutationId\n    __typename\n  }\n}\n"
    variables = {
        "createMessageMutation": {
            "entityId": "72",
            "isHtml": True,
            "subject": "",
            "content": '<p style="margin-bottom: 5pt; line-height: 1.38;">Ticket Message #'
            + str(request_id)
            + "</p>",
            "pin": False,
            "public": False,
            "forum": False,
            "noReply": False,
            "surveys": [],
            "commitments": [],
            "reports": [],
            "medias": [],
            "tags": [],
            "labelId": None,
            "recipients": {"entityIds": [73], "groupIds": []},
            "charges": [],
            "forms": [],
        }
    }

    res = req.post(
        URL,
        headers=HEADERS,
        params=QUERYSTRING,
        json={"query": query, "variables": variables},
    )

    file.write(
        "Message request " + str(request_id) + ": " + str(res.status_code) + "\n"
    )
    if res.status_code != 200:
        file.write(res.text + "\n")


def comment_message_from_zendesk_ticket(zenpy_client: Zenpy):
    tickets = zenpy_client.search("Ticket Message #", type="ticket")
    for ticket in tickets:
        print(str(ticket.to_dict()))


def create_comments_from_zendesk_to_classapp(zenpy_client):
    f = open("create_message_to_zendesk_integrated.txt", "w")
    for i in range(ATTEMPTS):
        create_message_to_zendesk_integrated(f, i + 1)
    comment_message_from_zendesk_ticket(zenpy_client)

    f.close()


def main():
    """
    Main function
    """

    zenpy_client = Zenpy(**ZENPY_CREDS)

    # Test if zendesk tickets appear in classapp
    create_comments_from_zendesk_to_classapp(zenpy_client)


main()
