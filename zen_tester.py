import requests as req
from zenpy import Zenpy

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
    # if (res.status_code != 200):
    file.write(res.text + "\n")


def create_comment_from_zendesk(file, request_id, zenpy_client: Zenpy):
    ticket = zenpy_client.search(
        "Test Message #" + str(request_id),
        type="ticket",
        sort_by="created_at",
        sort_order="desc",
    )


def create_messages_from_classapp_to_zendesk():
    f = open("create_message_to_zendesk_integrated.txt", "w")
    for i in range(ATTEMPTS):
        create_message_to_zendesk_integrated(f, i + 1)
        # create_comment_from_zendesk(f, i + 1, zenpy_client)

    f.close()


def create_message_to_be_answered(request_id):
    """
    Create the message where the replys will be tested
    """

    query = "mutation createMessageMuta($createMessageMutation: CreateMessageInput!) {createMessage(input: $createMessageMutation) {message {id}}}"
    variables = {
        "createMessageMutation": {
            "entityId": "73",
            "isHtml": True,
            "subject": "Message to be answered #" + str(request_id) + "",
            "content": '<p style="margin-bottom: 5pt; line-height: 1.38;">Can you answer?</p>',
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
            "recipients": {"entityIds": [72], "groupIds": []},
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

    if res.status_code != 200:
        raise Exception("Message to be created not created: " + res.text)

    return res.json()["data"]["createMessage"]["message"]["id"]


def reply_message_to_be_answered(file, request_id, message_id):
    """
    Make ReplyMessage request and store the result in a file
    """

    query = "mutation createReply($createReplyMutation: CreateReplyInput!) {\n  createReply(input: $createReplyMutation) {\n    clientMutationId\n    __typename\n  }\n}\n"
    variables = {
        "createReplyMutation": {
            "content": "Answering Message #" + str(request_id),
            "medias": [],
            "messageId": str(message_id),
            "entityId": 72,
            "parentId": "72",
        }
    }

    res = req.post(
        URL,
        headers=HEADERS,
        params=QUERYSTRING,
        json={"query": query, "variables": variables},
    )

    file.write("Reply request " + str(request_id) + ": " + str(res.status_code) + "\n")
    if res.status_code != 200:
        file.write(res.text + "\n")


# def reply_the_reply_classapp(file, request_id, message_id):
#     """
#     Make ReplyMessage to the message reply and store the result in a file
#     """

#     query = "mutation createReply($createReplyMutation: CreateReplyInput!) {\n  createReply(input: $createReplyMutation) {\n    clientMutationId\n    __typename\n  }\n}\n"
#     variables = {
#         "createReplyMutation": {
#             "content": "Adding reply comment #" + str(request_id),
#             "medias": [],
#             "messageId": str(message_id),
#             "entityId": 73,
#             "parentId": 72,
#         }
#     }

#     res = req.post(
#         URL,
#         headers=HEADERS,
#         params=QUERYSTRING,
#         json={"query": query, "variables": variables},
#     )

#     file.write(
#         "  ⌙Reply comment " + str(request_id) + ": " + str(res.status_code) + "\n"
#     )
#     if res.status_code != 200:
#         file.write(res.text + "\n")


def replies_from_classapp_to_zendesk():
    f = open("replies_from_classapp_to_zendesk.txt", "w")
    for i in range(ATTEMPTS):
        answerable_message_id = create_message_to_be_answered(i + 1)
        reply_message_to_be_answered(f, i + 1, answerable_message_id)

    f.close()


def clear_tickets(zenpy_client: Zenpy):
    tickets = zenpy_client.search("", type="ticket")
    for ticket in tickets:
        zenpy_client.tickets.delete(ticket)


def comment_message_from_zendesk_ticket():
    f = open("comment_message_from_zendesk_ticket.txt", "w")
    for i in range(ATTEMPTS):
        create_message_to_zendesk_integrated(f, i + 1, "")

    f.close()


def main():
    """
    Main function
    """
    zenpy_client = Zenpy(**ZENPY_CREDS)
    clear_tickets(zenpy_client)

    # Test if classapp messages appear in zendesk
    create_messages_from_classapp_to_zendesk()

    # Test if the classapp message replies appear in zendesk
    replies_from_classapp_to_zendesk()

    # Test if zendesk ticket comment appear in classapp


main()
