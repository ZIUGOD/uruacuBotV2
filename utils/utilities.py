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


def clear():
    if name == "nt":
        system("cls")
    else:
        system("clear")


def auth_api():
    auth = tweepy.OAuthHandler(env_vars["api_key"], env_vars["api_secret_key"])
    auth.set_access_token(env_vars["access_token"], env_vars["access_token_secret"])

    return tweepy.API(auth)


def create_tweet(api, message: str, image_path=None):
    clear()
    if image_path:
        api.update_status_with_media("AUTOMATED - " + message, image_path)
    else:
        api.update_status("AUTOMATED - " + message)

    print(color["green"] + "Tweet sent successfully!" + color["end"])
    sleep(60)
    clear()
    print("Restarting search...")
    sleep(2)
    clear()


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
                + f":\n{text}"
            )
            return True
        except:
            return False


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
                # Aguarda uma thread terminar antes de continuar
                continue

            # Inicia uma nova thread para processar o tweet
            print("Iniciando nova thread.")
            thread = threading.Thread(
                target=process_tweet,
                args=(api, tweet.user.screen_name, tweet.id, tweet.text),
            )
            thread.start()
            running_threads += 1


def start():
    clear()
    print("The bot is about to start...")
    sleep(2)
    clear()

    api = auth_api()

    while True:
        search_tweets(api)

        # Pausa para evitar excesso de requisições
        print("Esperando 15 segundos")
        sleep(15)

        # Reinicia as threads
        with lock:
            running_threads = 0
