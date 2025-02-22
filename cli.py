import argparse
import logging 
from http_client import HTTPClient

logging.basicConfig(filename='sms.log', level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description='CLI for sending SMS')
    parser.add_argument('sender', type=str, help='Sender number')
    parser.add_argument('recipient', type=str, help='REcipient number')
    parser.add_argument('message', type=str, help='Message text')
    args = parser.parse_args()

    client = HTTPClient()
    response = client.send_sms(args.sender, args.recipient, args.message)

    logging.info(f'Sent: {args.sender} -> {args.recipient}: {args.message}')
    logging.info(f"Server response: {response.status_code}, {response.body}")

    print(f"Server response: {response.status_code}, {response.body}")

if __name__ == "__main__":
    main()