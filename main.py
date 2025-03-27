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


def generate_comment(config):
    opening = random.choice(config.get('openings', []))
    adjective = random.choice(config.get('adjectives', []))
    noun = random.choice(config.get('nouns', []))
    verb = random.choice(config.get('verbs', []))
    middle = random.choice(config.get('middles', []))
    closing = random.choice(config.get('closings', []))
    emoji = random.choice(config.get('emojis', []))
    return f"{opening} {adjective} {noun} {verb} {middle} something truly special{closing} {emoji}"


def main():
    config = read_config()
    if not config:
        print("Failed to read config. Exiting...")
        return

    username = config.get('username')
    password = config.get('password')
    # Set min and max delay in seconds from config
    min_delay = config.get('min_delay', 300)
    max_delay = config.get('max_delay', 600)

    if not username or not password:
        print("Username and password are required in the config file. Exiting...")
        return

    cl = Client()
    print(f"Attempting to log in as {username}...")
    try:
        cl.login(username, password)
        print("Logged in successfully.")
        print("Searching for recent pet posts...")
        medias = cl.hashtag_medias_recent('pets', amount=10)
        print(f"Found {len(medias)} pet posts.")
        for index, media in enumerate(medias):
            print(f"Processing post {index + 1} of {len(medias)}...")
            try:
                # 先点赞帖子
                #try:
                #    cl.media_like(media.id)
                #    print(f"Successfully liked post {media.id}")
                #except Exception as like_error:
                #    print(f"Error liking post {media.id}: {like_error}")

                # 有 1% 的概率保存帖子
                if random.randint(1, 100) == 1:
                    cl.media_save(media.id)
                    print(f"Successfully saved post {media.id}")

                # 等待 10 - 20 秒的随机时间
                extra_delay = random.randint(10, 20)
                print(f"Waiting for {extra_delay} seconds before commenting...")
                time.sleep(extra_delay)

                comment = generate_comment(config)
                print(f"Prepared comment: {comment} for post {media.id}")
                cl.media_comment(media.id, comment)
                print(f"Successfully commented on post {media.id} with: {comment}")
                # 仅当不是最后一篇帖子时才设置延迟
                if index < len(medias) - 1:
                    # Set a random delay within the range
                    delay = random.randint(min_delay, max_delay)
                    print(f"Waiting for {delay} seconds before the next comment...")
                    time.sleep(delay)
            except Exception as e:
                print(f"Error processing post {media.id}: {e}")
    except Exception as e:
        print(f"Error logging in: {e}")
    finally:
        print("Logging out...")
        cl.logout()
        print("Logged out successfully.")


if __name__ == "__main__":
    main()
