from colorama import Fore, Style
from prettytable import PrettyTable


class CookieParser:

    _commands = {
        "show": "_print_cookies",
        "all": "_print_all_cookies",
        "set": "_set_cookie",
        "help": "_print_help"
    }

    def __init__(self, controller):
        self.controller = controller

    def parse_command(self, inp: str) -> None:
        inp = inp.split()
        if len(inp) == 1:
            self._print_cookies(self.controller.get_cookies())
            return
        
        if inp[1] not in CookieParser._commands:
            self._print_cookies(self.controller.get_cookies(), *inp[1:])
            return

        getattr(self, CookieParser._commands[inp[1]])(*inp[2:])
    
    def _set_cookie(self, name, attrProps):
        """Set cookie property"""
        attr, value = attrProps.split(sep='=')
        CookieParser._print_cookie(self.controller.set_cookie(name, attr, value))
    
    def _print_all_cookies(self) -> None:
        """Print all cookies for all domains"""
        self._print_cookies(self.controller.get_all_cookies())
        
    def _print_cookies(self, cookies, *cookie_names: str) -> None:
        """Print all or selected cookies for current domain"""

        table = PrettyTable()
        table.field_names = ["Name", "Value", "Domain", "Path", "HttpOnly", "SameSite", "Secure", "Expires"]
        if cookie_names:
            for cookie in cookies:
                if cookie['name'] in cookie_names:
                    CookieParser._print_cookie(cookie)
            return

        cookie_max_len = 15
        for cookie in cookies:
            value_display = cookie['value'] if len(cookie['value']) <= cookie_max_len else cookie['value'][:cookie_max_len-3] + '...'
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
    
    def _print_cookie(cookie: dict):
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
    
    def _print_help(self):
        """Print this help"""
        for cmd, fn in CookieParser._commands.items():
            print(f"cookie {cmd}: {getattr(CookieParser, fn).__doc__}")
