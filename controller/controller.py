from base_browser.browser import BaseBrowser


class Controller:

    def __init__(self, browser: BaseBrowser):
        self.browser = browser

    def get_cookies(self):
        return self.browser.get_cookies()
    
    def get_all_cookies(self):
        return self.browser.get_all_cookies()
    
    def set_cookie(self, name, attr, value):
        cookie = next((c.copy() for c in self.browser.get_cookies() if c["name"] == name), None)
        self.browser.delete_cookie(name)
        cookie[attr] = value
        self.browser.add_cookie(cookie)
        return cookie

    def change_context(self, idx: int):
        self.browser.cookie_contexts.change_context(idx)
    
    def get_contexts(self):
        return self.browser.cookie_contexts.get_contexts()
    
    def get_active_context_index(self):
        return self.browser.cookie_contexts.active_context
