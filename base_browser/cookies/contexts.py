class Contexts:

    def __init__(self):
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
    
    def change_context(self, idx, cookies=None):
        if cookies is None:
            self.active_context = idx
            return
        self.__ctxts[self.active_context] = cookies
        self.active_context = idx
        return self.get_active_context()