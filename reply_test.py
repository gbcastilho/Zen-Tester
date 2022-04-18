import requests as req
import time

ATTEMPTS = 15

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


def create_message_to_be_answered(request_id):
    """
    Create the message where the replies will be tested
    """

    query = "mutation createMessageMutation($createMessageMutation: CreateMessageInput!) {createMessage(input: $createMessageMutation) {message {id}}}"
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


def replies_from_classapp_to_zendesk():
    f = open("replies_from_classapp_to_zendesk.txt", "w")
    for i in range(ATTEMPTS):
        answerable_message_id = create_message_to_be_answered(i + 1)
        time.sleep(1)
        reply_message_to_be_answered(f, i + 1, answerable_message_id)
        time.sleep(1)

    f.close()


def main():
    """
    Main function
    """

    # Test if the classapp message replies appear in zendesk
    replies_from_classapp_to_zendesk()


main()
