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

        braille_image = BrailleGenerator.generate_braille_text(
            image=img, empty=args.empty, invert=args.invert)
        
        print(braille_image, end='')


class Parser:
    def __init__(self):
        self._parser = argparse.ArgumentParser()

    def start_parsing(self):
        self._parser.add_argument(
            '-s', '--size', type=int, nargs=2, help='Specify braille image size in symbols -s x y (default is max COLS LINES)',
            default=[COLS, LINES])
        self._parser.add_argument(
            '-p', '--path', type=str, help='Specify image path (if empty - do screenshot)', default='')
        self._parser.add_argument(
            '-e', '--empty', type=str, help='Specify empty symbol (empty braille is default)', default='⠀')
        self._parser.add_argument(
            '-i', '--invert', help='Using inverting', action='store_true')

        args = self._parser.parse_args()

        start_with_args(args)


if __name__ == '__main__':
    parser = Parser()
    parser.start_parsing()
