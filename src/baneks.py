#!/usr/bin/python3
from requests import get
from bs4 import BeautifulSoup
from time import sleep
from unidecode import unidecode_expect_nonascii
from os import getenv
import paho.mqtt.client as mqtt
from argparse import ArgumentParser
from message import format_message
from random import randint
import logging


def get_anek():
    try:
        html = get("https://baneks.ru/random")
        logging.info("successfully downloaded anecdote fron baneks")
    except Exception as e:
        logging.error("failed to get anecdote from baneks", exc_info=e)
    soup = BeautifulSoup(html.text, features="html.parser")
    return soup.body.section.p.text


def get_quote():
    try:
        html = get("http://bashorg.org/casual")
        logging.info("successfully downloaded quote from bashorg")
    except Exception as e:
        logging.error("failed to get quote from bashorg", exc_info=e)
    soup = BeautifulSoup(html.text, features="html.parser")
    return soup.body.find("div",
                          id="page").find("div",
                                          class_="q").findAll("div")[1].text


def get_message(max_length):
    # loop until we find one with correct length
    while True:
        match (randint(0, 1)):
            case 0:
                message = get_anek()
            case 1:
                message = get_quote()
            case _:
                logging.fatal("invalid random value")
                exit(1)

        message = unidecode_expect_nonascii(message).replace("\n",
                                                             " ").replace(
                                                                 '"', "")

        if len(message) <= max_length:
            return message

        logging.info("text too long, retrying")


if __name__ == "__main__":
    logging.root.setLevel(logging.INFO)

    # parse arguments using uppercase environment variables as a fallback
    parser = ArgumentParser(
        description="send anecdotes from baneks.ru to B4CKSP4CE's signage",
        add_help=False)
    parser.add_argument("--help", action="help", help="show this help message")
    parser.add_argument("-t",
                        type=str,
                        dest="topic",
                        default=getenv("TOPIC"),
                        help="mqtt topic")
    parser.add_argument("-h",
                        type=str,
                        dest="host",
                        default=getenv("HOST"),
                        help="mqtt broker host address")
    parser.add_argument("-u",
                        type=str,
                        dest="username",
                        default=getenv("USERNAME"),
                        help="mqtt username")
    parser.add_argument("-p",
                        type=str,
                        dest="password",
                        default=getenv("PASSWORD"),
                        help="mqtt password")
    parser.add_argument("-m",
                        type=int,
                        dest="max_length",
                        default=getenv("MAX_LENGTH", 160),
                        help="maximum allowed anecdote length")
    parser.add_argument("-s",
                        type=int,
                        dest="scrollspeed",
                        default=getenv("SCROLLSPEED", 14),
                        help="scroll speed to ask firmware for")
    args = parser.parse_args()

    # this ones are strictly required for script to work at all
    for var in args.topic, args.host:
        if var is None:
            logging.fatal("error: topic and host are required")
            exit(1)

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logging.info("successfully connected to the broker")
        else:
            logging.error(f"broker connection failure, result code: {rc}")

    def on_publish(client, userdata, mid):
        logging.info("successfully sent message")

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.username_pw_set(args.username, args.password)
    client.connect(args.host)
    client.loop_start()

    while True:
        client.publish(args.topic,
                       payload=format_message(get_message(args.max_length), 1,
                                              args.scrollspeed))
        sleep(120)
