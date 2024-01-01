class Contexts:

    def __init__(self, browser):
        self.browser = browser
        self.__ctxts = {1: []}
        self.active_context = 1

    def new_context(self, ctx):
        for idx in range(0, max(self.__ctxts.keys()) + 1):
            if idx not in self.__ctxts:
                self.__ctxts[idx] = ctx
                self.active_context = idx
                return idx
    
    def get_contexts(self):
        return self.__ctxts
    
    def remove_context(self, idx):
        del self.__ctxts[idx]

    def get_active_context(self):
        return self.__ctxts.get(self.active_context, [])
    
    def change_context(self, idx: int):
        if idx not in self.__ctxts:
            self.__ctxts[idx] = []
        self.active_context = idx
        self.browser.roll_cookies(self.get_active_context())
        return self.get_active_context()
    
    def update_cookies(self, cookies):
        ctx = self.__ctxts[self.active_context]
        for c in cookies:
            for i, current_cookie in enumerate(ctx):
                    if c['name'] == current_cookie['name'] and c['domain'] == current_cookie['domain']:
                        ctx[i] = c
                        break
            else:
                ctx.append(c)
    
    def get_cookies(self):
        return self.__ctxts[self.active_context]

