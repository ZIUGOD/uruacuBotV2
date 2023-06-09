import tweepy
from os import system, name
from dotenv import dotenv_values
from utils.data import *
from time import sleep

env_vars = dotenv_values(".env")


def clear():
    if name == "nt":
        system("cls")
    else:
        system("clear")


def auth_api():
    auth = tweepy.OAuthHandler(env_vars["api_key"], env_vars["api_secret_key"])
    auth.set_access_token(env_vars["access_token"], env_vars["access_token_secret"])

    return tweepy.API(auth)


def tweet(api, message: str, image_path=None):
    api = auth_api()
    clear()
    if image_path:
        api.update_status_with_media("AUTOMATED - " + message, image_path)
    else:
        api.update_status("AUTOMATED - " + message)

    print(color["green"] + "Tweet sent sucessfully!" + color["end"])
    sleep(60)
    clear()


def search_tweets():
    api = auth_api()
    
    found = False

    for tweet in tweepy.Cursor(
        api.search_tweets,
        q=query,
        result_type="recent",
        ).items(10):
        print(tweet)
        break