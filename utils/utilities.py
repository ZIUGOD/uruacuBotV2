import tweepy
from os import system, name
from dotenv import dotenv_values
from utils.data import *
from time import sleep
import threading

env_vars = dotenv_values(".env")

# variables for threads control
running_threads = 0
max_threads = 3
lock = threading.Lock()


# function to clear the terminal. Works on Linux, Windows or MacOS
def clear():
    if name == "nt":
        system("cls")
    else:
        system("clear")


# function to authorize the bot
def auth_api():
    auth = tweepy.OAuthHandler(env_vars["api_key"], env_vars["api_secret_key"])
    auth.set_access_token(env_vars["access_token"], env_vars["access_token_secret"])

    return tweepy.API(auth)


# this method creates a new tweet using (or not) an image
def create_tweet(api, message: str, image_path=None):
    clear()
    if image_path:
        api.update_status_with_media("AUTOMATED - " + message, image_path)
    else:
        api.update_status("AUTOMATED - " + message)

    print(
        color["green"]
        + "Tweet sent successfully!"
        + color["end"]
        + "\n\nWaiting 5 minutes"
    )
    sleep(300)  # waiting 5 minutes
    clear()
    print("Restarting search...")
    sleep(2)
    clear()


# function to validate a tweet and retweet it if
def process_tweet(api, name, tweet_id, text):
    if name not in black_list:
        try:
            api.retweet(tweet_id)
            api.create_favorite(tweet_id)

            print(
                color["cyan"]
                + f"@UruacuBOT"
                + color["end"]
                + " found a tweet by "
                + color["cyan"]
                + f"@{name}"
                + color["end"]
                + f":\n{text}\n\n"
                + "Waiting 10 minutes..."
            )
            sleep(600)  # waiting 10 minutes after a new RT
            return True
        except:
            return False


# this method makes a new search when its called.
def search_tweets(api):
    global running_threads
    for tweet in tweepy.Cursor(
        api.search_tweets,
        q=query,
        result_type="recent",
    ).items(5):
        print("Tweet: " + tweet.text)
        with lock:
            if running_threads >= max_threads:
                # wait for a thread to finish before continuing
                continue

            # starts a new thread to process the tweet
            print("Iniciando nova thread.")
            thread = threading.Thread(
                target=process_tweet,
                args=(api, tweet.user.screen_name, tweet.id, tweet.text),
            )  # configuring a new thread
            thread.start()
            running_threads += 1


# method to start the bot
def start():
    clear()
    print("The bot is about to start...")
    sleep(2)
    clear()

    api = auth_api()

    while True:
        search_tweets(api)

        # pause to avoid too many requests
        print("Waiting 15 seconds")
        sleep(15)

        # restart threads
        with lock:
            running_threads = 0
