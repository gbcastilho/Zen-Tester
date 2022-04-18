import requests as req
import time

ATTEMPTS = 10

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
            "content": '<p style="margin-bottom: 5pt; line-height: 1.38;">Test Message #'
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


def create_messages_from_classapp_to_zendesk():
    f = open("create_message_to_zendesk_integrated.txt", "w")
    for i in range(ATTEMPTS):
        create_message_to_zendesk_integrated(f, i + 1)
        time.sleep(1)

    f.close()


def main():
    """
    Main function
    """
    # Test if classapp messages appear in zendesk
    create_messages_from_classapp_to_zendesk()


main()
