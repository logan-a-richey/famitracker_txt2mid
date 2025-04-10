# reader.py

class HandlerRegistry:
    def __init__(self):
        self._handlers = {}

    def register(self, key, handler_cls):
        self._handlers[key.upper()] = handler_cls()

    def get_handler(self, key):
        return self._handlers.get(key.upper())

class Reader:
    def __init__(self, project):
        self.project = project
        self.registry = HandlerRegistry()
        self._register_handlers()

    def _register_handlers(self):
        from .handlers import MacroHandler  # assuming you move handlers to a module
        self.registry.register("MACRO", MacroHandler)

    def process_line(self, line):
        if not line.strip() or line.startswith("#"):
            return

        command = line.split()[0].upper()
        handler = self.registry.get_handler(command)

        if handler:
            match = handler.match(line)
            if match:
                handler.handle(match, self)
            else:
                print("[Warning] Pattern did not match for line: {}".format(line))
        else:
            print("[Warning] Unknown command type: {}".format(command))

