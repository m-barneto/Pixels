from pixelstrip import PixelStrip
from pixelstrip import Color
from time import sleep
from time import time
from colorsys import hsv_to_rgb
from colorsys import rgb_to_hsv
from random import random

def bubbleSort(strip, msDelay):
    startTime = time() * 1000.0
    n = strip.edgeLength / 2
    data = []
    for i in range(n):
        data.append(Color())
    for i in range(n):
        data[i] = randomColor()
        strip.writeEdges(data)
        strip.show()
        sleep(msDelay / 1000.0)

    i = 0
    while True:
        if (i == n):
            break

        j = 0
        while True:
            if (j == n - i - 1):
                break

            if (rgb_to_hsv(data[j].r / 255.0, data[j].g / 255.0, data[j].b / 255.0)[0] > rgb_to_hsv(data[j + 1].r / 255.0, data[j + 1].g / 255.0, data[j + 1].b / 255.0)[0]):
                val = data[j + 1]
                data[j + 1] = data[j]
                data[j] = val
                strip.writeEdges(data)
                strip.show()
                sleep(msDelay / 1000.0)

            if ((time() * 1000.0) - startTime >= msDelay * j):
                j += 1
        i += 1

# To decrease period, change the denominator of shift, the bigger it is the closer together the spectrum
# To change the speed, change numerator maybe???
def rainbowEdge(strip, duration):
    startTime = time() * 1000.0
    interval = duration / (strip.edgeLength / 2)
    index = 0
    while True:
        cTime = time() * 1000.0
        if (cTime - startTime >= duration):
            break
        for i in range(strip.edgeLength / 2):
            strip.edgeHalfBuffer[i] = rainbow(cTime / 1000.0, i / float(strip.edgeLength / 2.0))
        strip.writeEdges(strip.edgeHalfBuffer)
        strip.show()

def rainbow(cTime, shift):
    rgb = hsv_to_rgb(((cTime + shift) % 1.0), 1.0, 1.0)
    return Color(int(rgb[0] * 255.0), int(rgb[1] * 255.0), int(rgb[2] * 255.0))

# Use the time() for the rainbow color that way it matches with the rainbowEdge func
def growEdge(strip, duration):
    startTime = time() * 1000.0
    interval = duration / (strip.edgeLength / 2)
    index = 0
    while True:
        cTime = time() * 1000.0
        if (index >= (strip.edgeLength / 2)):
            break
        if (cTime - startTime >= (interval * index)):
            index += 1
        for v in range(index):
            strip.edgeHalfBuffer[v] = rainbow(cTime / 1000.0, v / float(strip.edgeLength / 2.0))
        strip.writeEdges(strip.edgeHalfBuffer)
        strip.show()

def shrinkEdge(strip, duration):
    startTime = time() * 1000.0
    interval = duration / (strip.edgeLength / 2)
    index = 0
    while True:
        cTime = time() * 1000.0
        if (startTime - cTime >= duration or index >= (strip.edgeLength / 2)):
            break
        if (cTime - startTime >= (interval * index)):
            strip.edgeHalfBuffer[(strip.edgeLength / 2) - index - 1] = strip.blankColor
            strip.writeEdges(strip.edgeHalfBuffer)
            strip.show()
            index += 1

def randomColor():
    rgb = hsv_to_rgb(random(), 1.0, 1.0)
    return Color(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

def randomEdge(strip):
    for i in range(strip.edgeLength / 2):
        strip.edgeHalfBuffer[i] = randomColor()
    strip.writeEdges(strip.edgeHalfBuffer)
    strip.show()

def main(args):
    #      ledCount, edgeCount, brightness (0-255)
    strip = PixelStrip(144, 1, 5)
    # clear strip data by filling with blank data
    strip.fill()
    try:
        while True:
            print("Random")
            for i in range(10):
                randomEdge(strip)
            shrinkEdge(strip, 1000)
            print("Rainbow Road")
            growEdge(strip, 1000)
            rainbowEdge(strip, 2000)
            shrinkEdge(strip, 1000)
            print("Bubble Sort Algorithm")
            bubbleSort(strip, 10)
            shrinkEdge(strip, 1000)
            print("---------------")
    except KeyboardInterrupt:
        print("\nExiting")
        shrinkEdge(strip, 1000)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
