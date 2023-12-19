from base_browser.browser import BaseBrowser
from controller.controller import Controller
from prettytable import PrettyTable
from colorama import Fore, Style
import re
from typing import List, Optional


class Console:

    def __init__(self, browser: BaseBrowser):
        self.browser = browser
        self.controller = Controller(browser)
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.handle_input(input('> '))
    
    def handle_input(self, inp: str) -> None:
        match RegexEqual(inp):
            case "[c|(cookies)]( .*)?":
                self._print_cookies(Console._parse_cookie_names(inp))
            case "quit" | "exit":
                print("Bye")
                self.running = False
            case _:
                print("Invalid action")

    def _parse_cookie_names(inp: str):
        names = inp.split()[1:]
        return names
    
    def _print_cookies(self, cookie_names: List[str]) -> None:
        cookies = self.controller.get_cookies()
        table = PrettyTable()
        table.field_names = ["Name", "Value", "Domain", "Path", "HttpOnly", "SameSite", "Secure", "Expires"]
        for cookie in cookies:
            if cookie_names and cookie['name'] not in cookie_names:
                continue
            value_display = cookie['value'] if len(cookie['value']) <= 25 else cookie['value'][:22] + '...'
            table.add_row([
                            cookie['name'],
                            value_display,
                            cookie['domain'],
                            cookie['path'],
                            cookie['httpOnly'],
                            cookie['sameSite'],
                            cookie['secure'],
                            cookie.get('expiry', '-')
                        ])
        print(table)


class RegexEqual(str):
    def __eq__(self, pattern):
        return bool(re.match(pattern, self))