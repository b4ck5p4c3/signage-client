#!/usr/bin/python3
from argparse import ArgumentParser
import paho.mqtt.publish as mqttpublish


def format_message(msg, persistant, scrollspeed):
    return ', '.join((f'{{"msg": "{msg}"', f'"persistant": {persistant}',
                      f'"scrollspeed": {scrollspeed}}}'))


if __name__ == "__main__":
    parser = ArgumentParser(
        description="send generic message to B4CKSP4CE's signage",
        add_help=False)
    parser.add_argument("--help", action="help", help="show this help message")
    parser.add_argument("-t",
                        type=str,
                        dest="topic",
                        help="mqtt topic",
                        required=True)
    parser.add_argument("-h",
                        type=str,
                        dest="host",
                        help="mqtt broker host address",
                        required=True)
    parser.add_argument("-u", type=str, dest="username", help="mqtt username")
    parser.add_argument("-p", type=str, dest="password", help="mqtt password")
    parser.add_argument("-s",
                        type=int,
                        dest="scrollspeed",
                        default=14,
                        help="scroll speed to ask firmware for")
    parser.add_argument("message", type=str)
    parser.add_argument(
        "-P",
        type=int,
        dest="persistant",
        default=1,
        help="ask firmware to keep message looping until next one arrives")
    args = parser.parse_args()

    mqttpublish.single(args.topic,
                       hostname=args.host,
                       auth={
                           "username": args.username,
                           "password": args.password
                       },
                       payload=format_message(args.message, args.persistant,
                                              args.scrollspeed))
