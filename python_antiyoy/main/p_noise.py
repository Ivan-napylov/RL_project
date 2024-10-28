from perlin_noise import PerlinNoise

class PerlinNoiseGenerator:
    def __init__(self, scale=0.1):
        self.scale = scale
        self.noise = PerlinNoise(octaves=1) 

    def get_noise(self, x, y):
        return self.noise([x * self.scale, y * self.scale])
