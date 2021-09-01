import sys

from fnb_scraper import FNBScraper
import logging
from argparse import ArgumentParser

log = logging.getLogger("Transaction printer")
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

parser = ArgumentParser()
parser.add_argument('username', help="Your FNB username.")
parser.add_argument('password', help="Your FNB password.")
args = parser.parse_args()


def main():
    log.info("Starting FNB scraper.")
    fnb_scraper = FNBScraper(args.username, args.password)
    fnb_scraper.scrape()
    print(fnb_scraper.get_transactions())


if __name__ == "__main__":
    main()
