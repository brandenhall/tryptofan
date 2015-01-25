from conf import settings


#   byte hue;
#   byte special;
#   byte rate;
#   float step;
#   byte mode;
#   int direction;
#   int position;
#   int stage;

# void spiralEffect(struct Blade*, CRGB*);
# void driveEffect(struct Blade*, CRGB*);
# void waveEffect(struct Blade*, CRGB*);
# void rocketEffect(struct Blade*, CRGB*);
# void kittenEffect(struct Blade*, CRGB*);
# void helixEffect(struct Blade*, CRGB*);
# void sparkleEffect(struct Blade*, CRGB*);

class Blade():
    def __init__(self, pixels, offset):
        self.pixels = pixels
        self.offset = offset
        self.position = 0
        self.direction = 1
        self.rate = 1
        self.step = 0
        self.special = False
        self.color = (255, 0, 0)
        self.draw = self.spiral

    def spiral(self):
        pass

    def rocket(self):
        pass

    def wander(self):
        pass

    def helix(self):
        pass

    def sparkle(self):
        pass
