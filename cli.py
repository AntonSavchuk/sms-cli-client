import argparse
import logging 
from http_client import HTTPClient

logger = logging.getLogger()

def send_sms(args):
    client = HTTPClient()
    response = client.send_sms(args.sender, args.recipient, args.message)

    logger.info('SMS sent: %s -> %s: %s', args.sender, args.recipient, args.message)
    logger.info("Server response: %s, %s", response.status_code, response.body)

    print("Server response: ", response.status_code, response.body)

def main():
    parser = argparse.ArgumentParser(description='CLI for sending SMS')
    subparsers = parser.add_subparsers(dest='command')

    send_parser = subparsers.add_parser("send", help="Send SMS")
    send_parser.add_argument("sender", type=str, help="Sender number")
    send_parser.add_argument("recipient", type=str, help="Recipient number")
    send_parser.add_argument("message", type=str, help="Message text")
    send_parser.set_defaults(func=send_sms)
    
    args = parser.parse_args()

    if args.command:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()