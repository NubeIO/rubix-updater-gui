class MainWindowController:
    def __init__(self, parent_window, app):
        self.parent = parent_window
        self.initial_load = True
        self.app = app
        self.init_app()

    def init_app(self):
        self.app.init()
        self.app.init_logger()
        if self.app.geometry():
            self.parent.restoreGeometry(self.app.geometry())
        if self.app.window_state():
            self.parent.restoreState(self.app.window_state())

