#!/bin/python3
import cli_parser
import config
from chrome.browser import ChromeBrowser
from console.console import Console


if __name__ == "__main__":
    cli_parser.set_options(cli_parser.parser.parse_args())

    browser = ChromeBrowser(proxy=config.PROXY)
    console = Console(browser=browser)
    console.run()

    browser.stop()
