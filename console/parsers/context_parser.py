from controller.controller import Controller


class ContextParser:
    
    def __init__(self, controller: Controller):
        self.controller = controller

    def parse_command(self, inp: str) -> None:
        inp = inp.split()
        if len(inp) == 1:
            self.list_contexts()
        else:
            try:
                self.controller.change_context(int(inp[1]))
            except:
                raise Exception("Context index is not a number")
            
    def list_contexts(self):
        ctxs = self.controller.get_contexts()
        active = self.controller.get_active_context_index()
        s = ""
        for c in ctxs.keys():
            if c != active:
                s += str(c) + "\n"
            else:
                s += "-> " + str(c) + "\n"
        print(s)
