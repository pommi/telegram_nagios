#!/usr/bin/env python

import argparse
from twx.botapi import TelegramBot


def parse_args():
    parser = argparse.ArgumentParser(description='Nagios notification via Telegram')
    parser.add_argument('-t', '--token', nargs='?', required=True)
    parser.add_argument('-o', '--object_type', nargs='?', required=True)
    parser.add_argument('--contact', nargs='?', required=True)
    parser.add_argument('--notificationtype', nargs='?')
    parser.add_argument('--hoststate', nargs='?')
    parser.add_argument('--hostname', nargs='?')
    parser.add_argument('--hostaddress', nargs='?')
    parser.add_argument('--servicestate', nargs='?')
    parser.add_argument('--hostalias', nargs='?')
    parser.add_argument('--servicedesc', nargs='?')
    parser.add_argument('--output', nargs='?')
    args = parser.parse_args()
    return args


def send_notification(token, user_id, message):
    bot = TelegramBot(token)
    bot.send_message(user_id, message).wait()


def host_notification(args):
    return "%s Host is %s. %s (%s). %s" % (
        args.notificationtype,
        args.hoststate,
        args.hostname,
        args.hostaddress,
        args.output,
    )


def service_notification(args):
    return "%s Service is %s. %s/%s. %s" % (
        args.notificationtype,
        args.servicestate,
        args.hostalias,
        args.servicedesc,
        args.output,
    )


def main():
    args = parse_args()
    user_id = int(args.contact)
    if args.object_type == 'host':
        message = host_notification(args)
    elif args.object_type == 'service':
        message = service_notification(args)
    send_notification(args.token, user_id, message)

if __name__ == '__main__':
    main()
