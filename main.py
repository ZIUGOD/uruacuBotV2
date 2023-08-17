import tweepy
from os import system, name
from dotenv import dotenv_values
from utils.data import *
from time import sleep

env_vars = dotenv_values(".env")


# method to clear the terminal. Works on every system
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
        f"{color['green']}Tweet sent successfully!!{color['end']}\n"
        f"Waiting 10 minutes"
    )

    sleep(600)  # waiting 10 minutes
    clear()
    print("Restarting search...")
    sleep(2)
    clear()


# function to validate a tweet. If it's a new one, it will be favourited and retweeted.
def process_tweet(api, name, tweet_id):
    if name not in black_list:
        try:
            api.retweet(tweet_id)
            api.create_favorite(tweet_id)

        except:
            pass

        return True


# this method makes a new search when its called.
def search_tweets(api):
    print("Search started")
    search = tweepy.Cursor(
        api.search_tweets,
        q=query,
        result_type="recent",
    ).items(5)
    for tweet in search:
        found = process_tweet(api, tweet.user.screen_name, tweet.id)

        if found:
            print(
                f"{color['cyan']}@UruacuBOT{color['end']} found a tweet by {color['cyan'], tweet.user.screen_name, color['end']}:\n"
                f"{tweet.text}\n"
                f"Tweet retweeted and favorited! Waiting 10 minutes . . ."
            )

            sleep(600)  # waiting 10 minutes
        else:
            pass


# method to start the bot
def start():
    clear()
    print(color["yellow"] + "The bot is about to start . . ." + color["end"])
    sleep(2)
    clear()

    api = auth_api()

    try:
        api.verify_credentials()
        print(color["green"] + "Credentials OK!" + color["end"])
    except Exception as error:
        print(color["red"] + f"Error during authentication: {error}" + color["end"])

    sleep(1)
    clear()

    try:
        while True:
            print("Search...")
            search_tweets(api)

            print("Waiting 20 seconds . . .")
            sleep(20)  # pause 20 seconds to avoid too many requests

            clear()

    except Exception as error:
        clear()

        print(
            f"{color['red']}An error occurred and the bot stopped:{color['yellow']}\n",
            error,
            color["end"],
        )


if __name__ == "__main__":
    start()
