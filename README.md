# Zen-Tester
Zendesk integration tester

## Install

There are necessary dependencies to install. Run the commands:

- `pip install requests`
- `pip install zenpy`


## Preparations

Before run make these steps
- Run Joy project in background
- In the database, set the User `id = 2` to be master
- In Zendesk, create an account
- Create a link/channel between Zendesk and this user

## Run

To test the stress methods run the following commands:
1. Message to the Zendesk connected user: `python3 message_test.p`
2. Reply a message from the Zendesk connected user: `python3 reply_test.py`
3. Comment on a message to Zendesk connected user via Zendesk: `python3 comment_test.py`

        Set the ATTEMPTS variable to configure the amount of requests to be tried