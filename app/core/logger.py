import logging


class ConsoleLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = parent.feedback_logs_console

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class LoggerSetup:
    def __init__(self, parent):
        self.parent = parent
        log = ConsoleLogger(self.parent)
        log.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(log)
        logging.getLogger().setLevel(logging.DEBUG)
