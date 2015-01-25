import logging
import logging.config
import signal
import handlers
import opc

from conf import settings

from multiprocessing.pool import ThreadPool

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.web import Application

logger = logging.getLogger(__name__)


class Tryptofan():
    def __init__(self):
        logger.info("Initializing Tryptofan...")
        logging.config.dictConfig(settings.LOGGING)
        self.pixels = []

        handlers.ControllerHandler.tryptofan = self

        signal.signal(signal.SIGTERM, self.sig_handler)
        signal.signal(signal.SIGINT, self.sig_handler)

        self.workers = ThreadPool(10)
        self.controller_clients = []

    def start(self):
        logger.info("Starting Tryptofan...")
        self.opc_client = opc.Client('localhost:7890')

        apps = [
            (r'/ws', handlers.ControllerHandler),
            (r'/(.*)', handlers.IndexStaticFileHandler, {'path': settings.WEBROOT}),
        ]
        application = Application(apps)
        self.http_server = HTTPServer(application)

        self.updater = PeriodicCallback(self.update, 1000/settings.FRAMERATE)

        self.updater.start()
        IOLoop.instance().start()

    def update(self):
        # TODO: update fan blades here
        self.blit()

    def blit(self):
        self.opc_client.put_pixels(self.pixels)

    def add_controller_client(self, client):
        logger.info('Controller client connected')
        self.controller_clients.append(client)

    def remove_controller_client(self, client):
        logger.info('Controller client disconnected')
        self.controller_clients.remove(client)

    def clear(self):
        self.pixels = [(0, 0, 0)] * settings.PIXEL_COUNT
        self.blit()
        self.blit()

    def sig_handler(self, sig, frame):
        logger.warning('Caught signal: %s', sig)
        IOLoop.instance().add_callback(self.shutdown)

    def shutdown(self):
        logger.info('Stopping Tryptofan...')
        try:
            self.updater.stop()
            self.clear()

        except Exception as err:
            logger.error("Could not close servers gracfully. {}".format(err))

        finally:
            IOLoop.instance().stop()
            logger.info('Shutdown')

if __name__ == "__main__":
    tryptofan = Tryptofan()
    tryptofan.start()
