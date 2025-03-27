import json
import random
import time
from instagrapi import Client


def read_config():
    try:
        # Specify the encoding as utf-8
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Config file not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding config file.")
        return None


def main():
    config = read_config()
    if not config:
        print("Failed to read config. Exiting...")
        return

    username = config.get('username')
    password = config.get('password')
    comments = config.get('comments', ['So cute!'])
    # Set min and max delay in seconds from config
    min_delay = config.get('min_delay', 90)
    max_delay = config.get('max_delay', 180)
    emojis = config.get('emojis', ['😻', '🐶', '🥰', '😘'])

    if not username or not password:
        print("Username and password are required in the config file. Exiting...")
        return

    cl = Client()
    print(f"Attempting to log in as {username}...")
    try:
        cl.login(username, password)
        print("Logged in successfully.")
        print("Searching for recent pet posts...")
        medias = cl.hashtag_medias_recent('pets', amount=3)
        print(f"Found {len(medias)} pet posts.")
        for index, media in enumerate(medias):
            print(f"Processing post {index + 1} of {len(medias)}...")
            try:
                comment = random.choice(comments)
                emoji = random.choice(emojis)
                comment = f"{comment} {emoji}"
                print(f"Prepared comment: {comment} for post {media.id}")
                cl.media_comment(media.id, comment)
                print(f"Successfully commented on post {media.id} with: {comment}")
                # Set a random delay within the range
                delay = random.randint(min_delay, max_delay)
                print(f"Waiting for {delay} seconds before the next comment...")
                time.sleep(delay)
            except Exception as e:
                print(f"Error commenting on post {media.id}: {e}")
    except Exception as e:
        print(f"Error logging in: {e}")
    finally:
        print("Logging out...")
        cl.logout()
        print("Logged out successfully.")


if __name__ == "__main__":
    main()
