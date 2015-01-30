import json
import logging
import logging.config
import signal
import opc

import handlers

from conf import settings
from blade import Blade

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.web import Application

logger = logging.getLogger('tryptofan')

# state [mode, speed, hue]


class Tryptofan():
    def __init__(self):
        logging.config.dictConfig(settings.LOGGING)

        self.pixels = [(0, 0, 0)] * settings.PIXELS
        self.state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.frame = 0
        self.blades = []

        handlers.ControllerHandler.tryptofan = self

        signal.signal(signal.SIGTERM, self.sig_handler)
        signal.signal(signal.SIGINT, self.sig_handler)

        self.controller_clients = []

    def start(self):
        logger.info("Starting Tryptofan...")
        self.opc_client = opc.Client('localhost:7890')

        apps = [
            (r'/ws', handlers.ControllerHandler, {'tryptofan': self}),
            (r'/(.*)', handlers.IndexStaticFileHandler, {'path': settings.WEBROOT}),
        ]
        application = Application(apps)
        self.http_server = HTTPServer(application)

        self.updater = PeriodicCallback(self.update, 1000/settings.FRAMERATE)

        for i in range(settings.BLADES):
            blade = Blade(self.pixels, i * settings.BLADE_PIXELS, self.state[i][0], self.state[i][1], self.state[i][2])
            self.blades.append(blade)

        self.http_server.listen(settings.HTTP_PORT)
        self.updater.start()
        IOLoop.instance().start()

    def update(self):
        self.blit()

    def blit(self):
        self.opc_client.put_pixels(self.pixels)

    def add_controller_client(self, client):
        logger.debug('Controller client connected')
        self.controller_clients.append(client)

    def remove_controller_client(self, client):
        logger.debug('Controller client disconnected')
        self.controller_clients.remove(client)

    def set_state(self, sender, state):
        for info, blade in zip(state, self.blades):
            blade.update(info[0], info[1], info[2])

        self.state = state
        message = json.dumps(state)
        for client in self.controller_clients:
            if client != sender:
                client.write_message(message)

    def clear(self):
        self.pixels = [(0, 0, 0)] * settings.PIXELS
        self.blit()
        self.blit()

    def sig_handler(self, sig, frame):
        logger.warning('Caught signal: %s', sig)
        IOLoop.instance().add_callback(self.shutdown)

    def shutdown(self):
        logger.info('Stopping Tryptofan...')
        try:
            self.http_server.stop()
            self.updater.stop()
            self.clear()

        except:
            logger.exception('Could not close servers gracfully.')

        finally:
            IOLoop.instance().stop()
            logger.info('Shutdown')

if __name__ == "__main__":
    tryptofan = Tryptofan()
    tryptofan.start()
