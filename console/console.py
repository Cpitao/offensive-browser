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
            case "[(cs)|(cookieset) .*]":
                self._set_cookie(Console._parse_set_cookie(inp))
            case "quit" | "exit":
                print("Bye")
                self.running = False
            case _:
                print("Invalid action")

    def _parse_cookie_names(inp: str):
        names = inp.split()[1:]
        return names
    
    def _parse_set_cookie(inp: str):
        attr, value = inp.split()[1:]
        return attr, value
    
    def _set_cookie(self, attr, value):
        pass
        
    
    def _print_cookies(self, cookie_names: List[str]) -> None:
        cookies = self.controller.get_cookies()

        
        table = PrettyTable()
        table.field_names = ["Name", "Value", "Domain", "Path", "HttpOnly", "SameSite", "Secure", "Expires"]
        if cookie_names:
            for cookie in cookies:
                if cookie['name'] in cookie_names:
                    value_display = cookie['value']
                    http_only_display = (Fore.GREEN if cookie['httpOnly'] else Fore.RED) + str(cookie['httpOnly']) + Style.RESET_ALL
                    same_site_display = (Fore.GREEN if cookie['sameSite'] == "Strict" else Fore.YELLOW if cookie['sameSite'] == "Lax" else Fore.RED) \
                        + cookie['sameSite'] + Style.RESET_ALL
                    print()
                    print("Name:", cookie['name'])
                    print("Value:", value_display)
                    print("Domain:", cookie['domain'])
                    print("Path:", cookie['path'])
                    print("HttpOnly:", http_only_display)
                    print("SameSite:", same_site_display)
                    print("Secure:", cookie['secure'])
                    print("Expiry:", cookie.get('expiry', '-'))
            return

                
        
        for cookie in cookies:
            value_display = cookie['value'] if len(cookie['value']) <= 25 else cookie['value'][:22] + '...'
            http_only_display = (Fore.GREEN if cookie['httpOnly'] else Fore.RED) + str(cookie['httpOnly']) + Style.RESET_ALL
            same_site_display = (Fore.GREEN if cookie['sameSite'] == "Strict" else Fore.YELLOW if cookie['sameSite'] == "Lax" else Fore.RED) \
                + cookie['sameSite'] + Style.RESET_ALL
            table.add_row([
                            cookie['name'],
                            value_display,
                            cookie['domain'],
                            cookie['path'],
                            http_only_display,
                            same_site_display,
                            cookie['secure'],
                            cookie.get('expiry', '-')
                        ])
        print(table)


class RegexEqual(str):
    def __eq__(self, pattern):
        return bool(re.match(pattern, self))