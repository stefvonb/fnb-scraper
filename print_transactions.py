"""
Print transactions
"""
import sys
import os

import logging
from argparse import ArgumentParser
from fnb_scraper import FNBScraper

log = logging.getLogger("Transaction printer")
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

parser = ArgumentParser()
parser.add_argument('-u', '--username', help="Your FNB username.")
parser.add_argument('-p', '--password', help="Your FNB password.")
args = parser.parse_args()


def main():
    """
    Runs the program and prints out a list of transactions that have been
    scraped.
    """
    log.info("Starting FNB scraper.")
    username = os.environ["FNB_USERNAME"] if args.username is None \
        else args.username
    password = os.environ["FNB_PASSWORD"] if args.password is None \
        else args.password
    fnb_scraper = FNBScraper(username, password)
    fnb_scraper.scrape()
    print(fnb_scraper.get_transactions())


if __name__ == "__main__":
    main()
