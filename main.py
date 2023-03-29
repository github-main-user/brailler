#! /bin/python
import argparse

from os import get_terminal_size
from PIL import Image

from screenshot_handler import take_screenshot
from braille_generator import SymbolHandler, BrailleGenerator
from image_converter import convert_to_monochrome

COLS = get_terminal_size().columns
LINES = get_terminal_size().lines


def parse():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-s', '--size', type=int, nargs=2,
        help='Specify size in symbols <x> <y> (default is <COLS> <LINES>)',
        default=[COLS, LINES])
    parser.add_argument(
        '-p', '--path', type=str,
        help='Specify path (if not use - do screenshot)', default='')
    parser.add_argument(
        '-e', '--empty', type=str,
        help='Specify empty symbol (empty braille is default)', default='⠀')
    parser.add_argument(
        '-i', '--invert',
        help='Using inverting', action='store_true')

    return parser.parse_args()


def start_with_args(args):
    file = args.path if args.path != '' else take_screenshot()

    width = args.size[0] * 2
    height = args.size[1] * 4

    with Image.open(file) as img:
        img = img.resize((width, height))
        img = convert_to_monochrome(img)

        symbol_handler = SymbolHandler()
        symbol_handler.set_empty_char(args.empty)
        symbol_handler.set_invert_state(args.invert)

        braille_generator = BrailleGenerator(img, symbol_handler)
        braille_image = braille_generator.generate_text()

        print(braille_image, end='')


if __name__ == '__main__':
    args = parse()
    start_with_args(args)
