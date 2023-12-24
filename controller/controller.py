from base_browser.browser import BaseBrowser


class Controller:

    def __init__(self, browser: BaseBrowser):
        self.browser = browser

    def get_cookies(self):
        return self.browser.get_cookies()
    
    def set_cookie(self, name, attr, value):
        cookie = next((c.copy() for c in self.browser.get_cookies() if c["name"] == name), None)
        self.browser.delete_cookie(name)
        cookie[attr] = value
        self.browser.add_cookie(cookie)
        return cookie

    def change_context(self, idx):
        self.browser.cookie_contexts.change_context(idx, self.get_cookies())
