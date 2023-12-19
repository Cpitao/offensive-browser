from base_browser.browser import BaseBrowser


class Controller:

    def __init__(self, browser: BaseBrowser):
        self.browser = browser

    def get_cookies(self):
        return self.browser.get_cookies()
