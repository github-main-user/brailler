#! /bin/python
import argparse

from os import get_terminal_size
from PIL import Image
from imager import FileHandler, BrailleImage

COLS = get_terminal_size().columns
LINES = get_terminal_size().lines


class Starter:
    def __init__(self):
        self._file_handler = FileHandler()

    def start_with_args(self, args):
        file = self._file_handler.get_file_path(args.p)

        with Image.open(file) as img:
            braille_image = BrailleImage(image=img,
                                         symbols_x=args.s[0],
                                         symbols_y=args.s[1],
                                         threshold=args.t)

            print(braille_image.generate_image())


class Parser:
    def __init__(self):
        self._parser = argparse.ArgumentParser()
        self._starter = Starter()

    def start_parsing(self):
        self._parser.add_argument(
            '-s', '--size', type=int, nargs='+', help='Specify braille image size x y (in symbols) - default COLS LINES',
            default=[COLS, LINES])
        self._parser.add_argument(
            '-p', '--path', type=str, help='Specify image path (if empty - do screenshot)', action='store_true', default='')
        self._parser.add_argument(
            '-t', '--threshold', type=float, help='Specify dithering threshold 0.0 -> 1.0 (0.5 by default)', default=0.5)

        args = self._parser.parse_args()

        self._starter.start_with_args(args)


if __name__ == '__main__':
    parser = Parser()
    parser.start_parsing()
