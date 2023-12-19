#!/bin/python3
from chrome.browser import ChromeBrowser
from console.console import Console

if __name__ == "__main__":
    browser = ChromeBrowser()
    console = Console(browser=browser)
    console.run()

    browser.stop()