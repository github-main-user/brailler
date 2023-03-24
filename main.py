#! /bin/python
import argparse

from PIL import Image
from imager import FileHandler, BrailleImage


class Starter:
    def __init__(self):
        self._file_handler = FileHandler()

    def start_with_args(self, args):
        file = self._file_handler.get_file_path(args.p)

        with Image.open(file) as img:
            braille_image = BrailleImage(image=img,
                                         width=args.x,
                                         height=args.y,
                                         threshold=args.t)

            print(braille_image.generate_image())


class Parser:
    def __init__(self):
        self._parser = argparse.ArgumentParser()
        self._starter = Starter()

    def start_parsing(self):
        self._parser.add_argument(
            '-x', type=int, help='Specify width (50 by default)', default=50)
        self._parser.add_argument(
            '-y', type=int, help='Specify height (50 by default)', default=50)
        self._parser.add_argument(
            '-p', type=str, help='Specify image path (if empty - do screenshot)', default='')
        self._parser.add_argument(
            '-t', type=float, help='Specify threshold 0.0 -> 1.0 (0.5 by default)', default=0.5)

        args = self._parser.parse_args()

        self._starter.start_with_args(args)


if __name__ == '__main__':
    parser = Parser()
    parser.start_parsing()
