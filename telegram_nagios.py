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
    parser.add_argument('--servicedesc', nargs='?')
    parser.add_argument('--output', nargs='?')
    parser.add_argument('--author', nargs='?')
    parser.add_argument('--comment', nargs='?')
    args = parser.parse_args()
    return args


def send_notification(token, user_id, message):
    bot = TelegramBot(token)
    bot.send_message(user_id, message).wait()


def host_notification(args):
    state = ''
    notification = ''
    if args.hoststate == 'UP':
        state = u'\U00002705 '
    elif args.hoststate == 'DOWN':
        state = u'\U0001F525 '
    elif args.hoststate == 'UNREACHABLE':
        state = u'\U00002753 '

    if args.notificationtype in ['DOWNTIMESTART',
                                 'DOWNTIMEEND',
                                 'ACKNOWLEDGEMENT',
                                 'CUSTOM']:
        state = u'\U0001F4AC '
        notification = "%s%s %s by %s - %s (%s): %s" % (
            state,
            args.notificationtype,
            args.comment,
            args.author,
            args.hostname,
            args.hostaddress,
            args.output,
        )
    else:
        notification = "%s%s %s (%s): %s" % (
            state,
            args.notificationtype,
            args.hostname,
            args.hostaddress,
            args.output,
        )
    return notification

def service_notification(args):
    state = ''
    notification = ''
    if args.servicestate == 'OK':
        state = u'\U00002705 '
    elif args.servicestate == 'WARNING':
        state = u'\U000026A0 '
    elif args.servicestate == 'CRITICAL':
        state = u'\U0001F525 '
    elif args.servicestate == 'UNKNOWN':
        state = u'\U00002753 '

    if args.notificationtype in ['DOWNTIMESTART',
                                 'DOWNTIMEEND',
                                 'ACKNOWLEDGEMENT',
                                 'CUSTOM']:
        state = u'\U0001F4AC '
        notification = "%s%s %s by %s - %s/%s: %s" % (
            state,
            args.notificationtype,
            args.comment,
            args.author,
            args.hostname,
            args.servicedesc,
            args.output,
        )
    else:
        notification = "%s%s %s/%s: %s" % (
            state,
            args.notificationtype,
            args.hostname,
            args.servicedesc,
            args.output,
        )
    return notification

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
