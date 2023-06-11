import tweepy
from os import system, name
from dotenv import dotenv_values
from utils.data import *
from time import sleep
import threading

env_vars = dotenv_values(".env")


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
def process_tweet(api, name, tweet_id):
    if name not in black_list:
        try:
            api.retweet(tweet_id)
            api.create_favorite(tweet_id)

            return True
        except:
            return False


# this method makes a new search when its called.
def search_tweets(api):
    found = False
    global running_threads
    search = tweepy.Cursor(
        api.search_tweets,
        q=query,
        result_type="recent",
    ).items(5)
    for tweet in search:
        found = process_tweet(api, tweet.user.screen_name, tweet.id)

        if found:
            print(
                color["cyan"]
                + f"@UruacuBOT"
                + color["end"]
                + " found a tweet by "
                + color["cyan"]
                + f"@{tweet.user.screen_name}"
                + color["end"]
                + f":\n{tweet.text}\n\n"
                + "Tweet retweeted and favorited! Let's wait 10 minutes..."
            )
            sleep(600)  # waiting 10 minutes
            break  # breaking the point to restart after a new RT
        else:
            print("Próximo...")
            pass


# method to start the bot
def start():
    clear()
    print("The bot is about to start...")
    sleep(2)
    clear()

    api = auth_api()
    try:
        api.verify_credentials()
        print(color["green"] + "Credentials OK!" + color["end"])
    except Exception as error:
        print(color["red"] + f"Error: {error}")

    sleep(1)
    clear()

    while True:
        search_tweets(api)

        # pause to avoid too many requests
        print("Waiting 15 seconds")
        sleep(15)
        clear()
