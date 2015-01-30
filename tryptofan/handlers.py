import json
import logging

from tornado.web import StaticFileHandler
from tornado.websocket import WebSocketHandler

logger = logging.getLogger('tryptofan')


class IndexStaticFileHandler(StaticFileHandler):
    def parse_url_path(self, url_path):
        if not url_path or url_path.endswith('/'):
            url_path += 'index.html'

        return super(IndexStaticFileHandler, self).parse_url_path(url_path)


class ControllerHandler(WebSocketHandler):
    def initialize(self, tryptofan):
        self.tryptofan = tryptofan

    def check_origin(self, origin):
        return True

    def open(self):
        self.tryptofan.add_controller_client(self)
        self.write_message(json.dumps(self.tryptofan.state))

    def on_message(self, message):
        try:
            self.tryptofan.set_state(self, json.loads(message))
        except:
            logger.exception("Could not load state from controller")

    def on_close(self):
        self.tryptofan.remove_controller_client(self)
