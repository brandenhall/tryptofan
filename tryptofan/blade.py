import logging
import random

from conf import settings

from tornado.ioloop import PeriodicCallback

colors = [(255, 0, 0), (255, 6, 0), (255, 12, 0), (255, 18, 0), (255, 24, 0), (255, 30, 0), (255, 36, 0), (255, 42, 0), (255, 48, 0), (255, 54, 0), (255, 60, 0), (255, 66, 0), (255, 72, 0), (255, 78, 0), (255, 84, 0), (255, 90, 0), (255, 96, 0), (255, 102, 0), (255, 108, 0), (255, 114, 0), (255, 120, 0), (255, 126, 0), (255, 132, 0), (255, 138, 0), (255, 144, 0), (255, 150, 0), (255, 156, 0), (255, 162, 0), (255, 168, 0), (255, 174, 0), (255, 180, 0), (255, 186, 0), (255, 192, 0), (255, 198, 0), (255, 204, 0), (255, 210, 0), (255, 216, 0), (255, 222, 0), (255, 228, 0), (255, 234, 0), (255, 240, 0), (255, 246, 0), (255, 252, 0), (252, 255, 0), (246, 255, 0), (240, 255, 0), (234, 255, 0), (228, 255, 0), (222, 255, 0), (216, 255, 0), (210, 255, 0), (204, 255, 0), (198, 255, 0), (192, 255, 0), (186, 255, 0), (180, 255, 0), (174, 255, 0), (168, 255, 0), (162, 255, 0), (156, 255, 0), (150, 255, 0), (144, 255, 0), (138, 255, 0), (132, 255, 0), (126, 255, 0), (120, 255, 0), (114, 255, 0), (108, 255, 0), (102, 255, 0), (96, 255, 0), (90, 255, 0), (84, 255, 0), (78, 255, 0), (72, 255, 0), (66, 255, 0), (60, 255, 0), (54, 255, 0), (48, 255, 0), (42, 255, 0), (36, 255, 0), (30, 255, 0), (24, 255, 0), (18, 255, 0), (12, 255, 0), (6, 255, 0), (0, 255, 0), (0, 255, 6), (0, 255, 12), (0, 255, 18), (0, 255, 24), (0, 255, 30), (0, 255, 36), (0, 255, 42), (0, 255, 48), (0, 255, 54), (0, 255, 60), (0, 255, 66), (0, 255, 72), (0, 255, 78), (0, 255, 84), (0, 255, 90), (0, 255, 96), (0, 255, 102), (0, 255, 108), (0, 255, 114), (0, 255, 120), (0, 255, 126), (0, 255, 132), (0, 255, 138), (0, 255, 144), (0, 255, 150), (0, 255, 156), (0, 255, 162), (0, 255, 168), (0, 255, 174), (0, 255, 180), (0, 255, 186), (0, 255, 192), (0, 255, 198), (0, 255, 204), (0, 255, 210), (0, 255, 216), (0, 255, 222), (0, 255, 228), (0, 255, 234), (0, 255, 240), (0, 255, 246), (0, 255, 252), (0, 252, 255), (0, 246, 255), (0, 240, 255), (0, 234, 255), (0, 228, 255), (0, 222, 255), (0, 216, 255), (0, 210, 255), (0, 204, 255), (0, 198, 255), (0, 192, 255), (0, 186, 255), (0, 180, 255), (0, 174, 255), (0, 168, 255), (0, 162, 255), (0, 156, 255), (0, 150, 255), (0, 144, 255), (0, 138, 255), (0, 132, 255), (0, 126, 255), (0, 120, 255), (0, 114, 255), (0, 108, 255), (0, 102, 255), (0, 96, 255), (0, 90, 255), (0, 84, 255), (0, 78, 255), (0, 72, 255), (0, 66, 255), (0, 60, 255), (0, 54, 255), (0, 48, 255), (0, 42, 255), (0, 36, 255), (0, 30, 255), (0, 24, 255), (0, 18, 255), (0, 12, 255), (0, 6, 255), (0, 0, 255), (6, 0, 255), (12, 0, 255), (18, 0, 255), (24, 0, 255), (30, 0, 255), (36, 0, 255), (42, 0, 255), (48, 0, 255), (54, 0, 255), (60, 0, 255), (66, 0, 255), (72, 0, 255), (78, 0, 255), (84, 0, 255), (90, 0, 255), (96, 0, 255), (102, 0, 255), (108, 0, 255), (114, 0, 255), (120, 0, 255), (126, 0, 255), (132, 0, 255), (138, 0, 255), (144, 0, 255), (150, 0, 255), (156, 0, 255), (162, 0, 255), (168, 0, 255), (174, 0, 255), (180, 0, 255), (186, 0, 255), (192, 0, 255), (198, 0, 255), (204, 0, 255), (210, 0, 255), (216, 0, 255), (222, 0, 255), (228, 0, 255), (234, 0, 255), (240, 0, 255), (246, 0, 255), (252, 0, 255), (255, 0, 252), (255, 0, 246), (255, 0, 240), (255, 0, 234), (255, 0, 228), (255, 0, 222), (255, 0, 216), (255, 0, 210), (255, 0, 204), (255, 0, 198), (255, 0, 192), (255, 0, 186), (255, 0, 180), (255, 0, 174), (255, 0, 168), (255, 0, 162), (255, 0, 156), (255, 0, 150), (255, 0, 144), (255, 0, 138), (255, 0, 132), (255, 0, 126), (255, 0, 120), (255, 0, 114), (255, 0, 108), (255, 0, 102), (255, 0, 96), (255, 0, 90), (255, 0, 84), (255, 0, 78), (255, 0, 72), (255, 0, 66), (255, 0, 60), (255, 0, 54), (255, 0, 48), (255, 0, 42), (255, 0, 36), (255, 0, 30), (255, 0, 24), (255, 0, 18), (255, 0, 12), (255, 0, 6), (255, 0, 0)]

logger = logging.getLogger('tryptofan')


class Blade():
    def __init__(self, pixels, offset, mode, speed, hue):
        self.pixels = pixelss
        self.offset = offset
        self.position = 0
        self.direction = 1
        self.rate = 1
        self.step = 0
        self.blank = [(0, 0, 0), ] * settings.BLADE_PIXELS
        self.modes = [self.flower, self.rocket, self.spiral, self.helix, self.sparkle]
        self.mode = self.modes[0]

        self.updater = PeriodicCallback(self.draw, 1000/1)
        self.update(mode, speed, hue)
        self.updater.start()

    def draw(self):
        self.mode()

    def update(self, mode, speed, hue):
        self.mode = self.modes[mode % len(self.modes)]
        self.updater.callback_time = 1000 / (speed/255.0 * (settings.FRAMERATE - settings.FRAMERATE/10) + settings.FRAMERATE/10)
        self.color = colors[hue]

    def flower(self):
        self.pixels[self.offset:self.offset + settings.BLADE_PIXELS] = self.blank
        self.pixels[self.offset + self.position] = self.color
        self.position -= 1
        self.position %= settings.BLADE_PIXELS

    def rocket(self):
        self.pixels[self.offset:self.offset + settings.BLADE_PIXELS] = self.blank
        self.pixels[self.offset + self.position] = self.color
        self.position += 1
        self.position %= settings.BLADE_PIXELS

    def spiral(self):
        self.pixels[self.offset:self.offset + settings.BLADE_PIXELS] = self.blank
        self.pixels[self.offset + self.position] = self.color
        self.position += self.direction
        if self.position < 0:
            self.position = 1
            self.direction = 1
        elif self.position == settings.BLADE_PIXELS:
            self.position = settings.BLADE_PIXELS - 2
            self.direction = -1

    def helix(self):
        self.pixels[self.offset:self.offset + settings.BLADE_PIXELS] = self.blank
        self.pixels[self.offset + self.position] = self.color
        self.pixels[self.offset + settings.BLADE_PIXELS - 1 - self.position] = self.color
        self.position += self.direction
        if self.position < 0:
            self.position = 1
            self.direction = 1
        elif self.position == settings.BLADE_PIXELS:
            self.position = settings.BLADE_PIXELS - 2
            self.direction = -1

    def sparkle(self):
        self.pixels[self.offset:self.offset + settings.BLADE_PIXELS] = self.blank
        self.pixels[self.offset + random.randint(0, settings.BLADE_PIXELS - 1)] = self.color
