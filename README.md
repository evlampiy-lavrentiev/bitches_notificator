# Telegram Channel Member(Leaving Bitches) Tracker

This script is designed to send notifications about users who have joined or left a Telegram channel. Notifications are sent once daily, providing up-to-date information about the member dynamics of your channel.

Example of messages:

[User1](link1) **Join** at 2025-01-16 11:57:19+00:00

[User2](link2) **Leave** at 2025-01-16 11:51:01+00:00

## Installation

1. Clone the repository to your device:

    ```
    git clone https://github.com/evlampiy-lavrentiev/bitches_notificator.git
    cd bitches_notificator
    ```

2. Install the necessary dependencies listed in requirements.txt:

    ```
    pip install -r requirements.txt
    ```

3. Configure the settings:

    You need to set a few variables so the script can connect to the Telegram API. These variables can be specified in a config.json file or as environment variables (e.g., using a .env file):

    - api_id (or API_ID)
    - api_hash (or API_HASH)
    - bot_token (or BOT_TOKEN)

    Example content for config.json:

    ```
    {
        "api_id": "your_api_id",
        "api_hash": "your_api_hash",
        "bot_token": "your_bot_token"
    }
    ```

    Example content for .env:


    ```
    API_ID="your_api_id"
    API_HASH="your_api_hash"
    BOT_TOKEN="your_bot_token"
    ```


4. Running the script:

    It is recommended to run this script in a screen or tmux session to keep it running even after the terminal is closed. Here's how you can do it using screen:

    ```
    screen -S telegram_tracker
    python your_script.py
    ```

    Or using tmux:

    ```
    tmux new -s telegram_tracker
    python your_script.py
    ```

    To detach from screen or tmux, press Ctrl+A, then D. To reattach to the session, use screen -r telegram_tracker or tmux attach -t telegram_tracker.


## How It Works

The script performs the following actions:

1. Connects to Telegram using provided API keys.
2. Monitors changes in the member list of the specified channel.
3. Sends a daily notification listing users who have joined or left the channel.

## Support

If you have any questions or suggestions, please create a discussion or an issue in the repository. We are happy to help!
