from dataclasses import dataclass
from typing import List
import requests
import logging
from bs4 import BeautifulSoup

log = logging.getLogger("FNB Scraper")

call_request = {"GET": requests.get, "POST": requests.post}


def get_base_headers():
    return {
        'Host': None,
        'Connection': 'keep-alive',
        'Accept': 'text/html, */*; q=0.01',
        'Origin': None,
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36',
        'Referer': 'https://www.online.fnb.co.za/banking/main.jsp',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'en-US,en;q=0.8'
    }


@dataclass
class Transaction:
    amount: float


@dataclass
class Account:
    id: str


class FNBScraper:
    __transactions: List[Transaction]
    cookies: dict
    username: str
    password: str

    def __init__(self, username, password):
        log.info("Initialising FNB scraper...")
        self.cookies = {}
        self.username = username
        self.password = password
        self.__transactions = []
        log.info("Successfully initialised!")

    def get_transactions(self) -> List[Transaction]:
        return self.__transactions

    def scrape(self):
        self.__hit_home_page()
        self.__login()

        bank_account_links = self.__get_bank_account_links()

    def __save_cookie(self, response):
        for cookie_key, cookie_value in response.cookies.items():
            self.cookies[cookie_key] = cookie_value

    def __hit_page(self, host="www.online.fnb.co.za", path="/", method="POST", post_data=None, params=None,
                   content_type=None):
        # Set the URL
        url = f"https://{host}{path}"
        log.debug(f"Hitting page with URL: {url}")

        # Set the headers
        headers = get_base_headers()
        headers["Host"] = host
        headers["Origin"] = host
        if content_type:
            headers['Content-Type'] = content_type
        log.debug(f"Headers: {headers}")

        log.debug(f"Sending request with cookies: {self.cookies}")

        response = call_request[method](url, cookies=self.cookies, headers=headers, data=post_data, params=params)

        self.__save_cookie(response)

        return response

    def __hit_home_page(self):
        return self.__hit_page("www.fnb.co.za", method="GET")

    def __login(self):
        post_data = {
            'multipleSubmit': 1,
            'url': 0,
            'country': 15,
            'countryCode': 'ZA',
            'language': 'en',
            'BrowserType': None,
            'BrowserVersion': None,
            'OperatingSystem': None,
            'action': 'login',
            'formname': 'LOGIN_FORM',
            'form': 'LOGIN_FORM',
            'LoginButton': 'Login',
            'homePageLogin': 'true',
            'division': '',
            'products': '',
            'bankingUrl': 'https://www.online.fnb.co.za',
            'nav': 'navigator.UserLogon',
            'Username': self.username,
            'Password': self.password,
        }

        response = self.__hit_page('www.online.fnb.co.za', '/login/Controller', "POST", post_data=post_data,
                                   content_type='application/x-www-form-urlencoded')

        parsed_response = BeautifulSoup(response.text, 'html.parser')

        form_input_tags = parsed_response.find("form").findAll("input")
        payload = {tag["id"]: tag["value"] for tag in form_input_tags}

        payload.update({
            'genericApplet': '0',
            'form': 'LOGIN_FORM',
            'multipleSubmit': '1',
            'simple': 'true',
            'countryCode': 'ZA',
            'homePageLogin': 'true',
            'url': '0',
            'skin': '0',
            'country': '15',
            'division': '',
            'fromLogin': 'true',
            'LoginButton': 'Login',
            'action': 'login',
            'nav': 'navigator.UserLogon',
            'bankingUrl': 'https://www.online.fnb.co.za',
            'language': 'en',
            'formname': 'LOGIN_FORM',
            'products': '',
            'datasource': '101',
            'OperatingSystem': 'MacIntel',
            'BrowserType': 'Chrome',
            'BrowserVersion': '34.0.1847.137 Safari/537.36',
            'BrowserHeight': '0',
            'BrowserWidth': "0",
            'isMobile': "false"}
        )

        redirect_response = self.__hit_page(path="/banking/Controller", method="GET", params=payload)

        return redirect_response

    def __get_bank_account_links(self):
        payload = {
            'nav': "accounts.summaryofaccountbalances.navigator.SummaryOfAccountBalances",
            'FARFN': "4",
            'actionchild': "1",
            'isTopMenu': "true",
            'targetDiv': "workspace"
        }

        response = self.__hit_page(path="/banking/Controller", params=payload)

        bank_account_links = []

        return bank_account_links
