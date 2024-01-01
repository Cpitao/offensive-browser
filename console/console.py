from base_browser.browser import BaseBrowser
from console.parsers.context_parser import ContextParser
from controller.controller import Controller
from console.parsers.cookie_parser import CookieParser

import re


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
        try:
            match RegexEqual(inp):
                case "[c|(cookie)]( .*)?":
                    CookieParser(controller=self.controller).parse_command(inp)
                case "ctx( .*)?":
                    ContextParser(controller=self.controller).parse_command(inp)
                case "quit" | "exit":
                    print("Bye")
                    self.running = False
                case _:
                    print("Invalid action")
        except Exception as e:
            print("Error running command. Check syntax and try again")
            print(e)


class RegexEqual(str):
    def __eq__(self, pattern):
        return bool(re.fullmatch(pattern, self))