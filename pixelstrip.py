from neopixel import Adafruit_NeoPixel
from colorsys import hsv_to_rgb

class Color:
    def __init__(self, _r = 0, _g = 0, _b = 0):
        self.r = _r
        self.g = _g
        self.b = _b
    def __str__(self):
        return "( %d, %d, %d)" % (self.r, self.g, self.b)
    def getBits(self):
        return (self.g << 16) | (self.r << 8) | self.b

class PixelStrip:
    def __init__(self, stripLength, edgeCount, brightness = 255, gpio = 18, hz = 800000, dma = 10, invert = False, channel = 0):
        self.pixelCount = stripLength * edgeCount
        self.strip = Adafruit_NeoPixel(self.pixelCount, gpio, hz, dma, invert, brightness, channel)
        self.strip.begin()
        self.stripLength = stripLength
        self.edgeCount = edgeCount
        self.edgeLength = self.stripLength / self.edgeCount
        self.blankColor = Color()
        self.edgeHalfBuffer = []
        for i in range(self.edgeLength / 2):
            self.edgeHalfBuffer.append(self.blankColor)
        self.edge = []
        for i in range(self.edgeLength):
            self.edge.append(self.blankColor)
    
    def show(self):
        self.strip.show()
    
    def setPixel(self, n, color):
        self.strip.setPixelColor(n, color.getBits())

    def fill(self, color = Color()):
        for i in range(self.edgeLength / 2):
            self.edgeHalfBuffer[i] = color
        self.writeEdges(self.edgeHalfBuffer)
        self.show()
    """
    def setEdge(self, edgeHalf):
        del self.edge[:]
        self.edge = []
        for i in range(self.edgeLength / 2):
            self.edge.append(edgeHalf[i])
        for i in range(self.edgeLength / 2):
            self.edge.append(edgeHalf[(self.edgeLength / 2) - i - 1])
        self.writeEdges()
    """
    def writeEdges(self, colors):
        for i in range(self.edgeCount):
            for p in range(self.edgeLength / 2):
                self.setPixel(i * self.edgeLength + p, colors[p])
                # might need to -1 after "- p" 
                self.setPixel(i * self.edgeLength + self.edgeLength - p - 1, colors[p])

