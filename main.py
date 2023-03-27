#! /bin/python
import argparse

from os import get_terminal_size
from PIL import Image
from screenshot_handler import ScreenshotHandler
from braille_generator import BrailleGenerator
from image_converter import ImageConverter

COLS = get_terminal_size().columns
LINES = get_terminal_size().lines


def start_with_args(args):
    file = args.path if args.path != '' else ScreenshotHandler.take_screenshot()

    with Image.open(file) as img:
        img = img.resize((args.size[0] * 2, args.size[1] * 4))
        img = ImageConverter.to_monochrome(img)

        braille_image = BrailleGenerator.generate_braille_text(img)
        print(braille_image, end='')

class Parser:
    def __init__(self):
        self._parser = argparse.ArgumentParser()

    def start_parsing(self):
        self._parser.add_argument(
            '-s', '--size', type=int, nargs='+', help='Specify braille image size in symbols -s x y (default is max COLS LINES)',
            default=[COLS, LINES])
        self._parser.add_argument(
            '-p', '--path', type=str, help='Specify image path (if empty - do screenshot)', default='')
        # space symbol
        # invert

        args = self._parser.parse_args()

        start_with_args(args)


if __name__ == '__main__':
    parser = Parser()
    parser.start_parsing()
