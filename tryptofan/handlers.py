from conf import settings

from tornado.web import StaticFileHandler
from tornado.websocket import WebSocketHandler


class IndexStaticFileHandler(StaticFileHandler):
    def parse_url_path(self, url_path):
        if not url_path or url_path.endswith('/'):
            url_path += 'index.html'

        return super(IndexStaticFileHandler, self).parse_url_path(url_path)


class ControllerHandler(WebSocketHandler):
    tryptofan = None

    def open(self):
        self.tryptofan.add_controller_client(self)

    def check_origin(self, origin):
        if settings.DEBUG:
            return True
        else:
            return super().check_origin(origin)

    def on_message(self, message):
        pass

    def on_close(self):
        self.tryptofan.remove_controller_client(self)
