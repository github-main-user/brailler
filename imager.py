import os
import subprocess

from braille_handler import BrailleHandler
from PIL import Image, ImageOps


class _ExistanceChecker:
    '''Check existance of the file true => return file, false => raise erroe'''
    @staticmethod
    def is_exist(file_path, error_msg) -> str:
        if os.path.exists(file_path):
            return file_path
        else:
            raise FileExistsError(error_msg)


class _ScreenshotTaker:
    def __init__(self, temp_file):
        self._temp_file = temp_file

    def _free_path(self):
        if os.path.exists(self._temp_file):
            os.remove(self._temp_file)

    def _take_screenshot(self):
        subprocess.call(['scrot', '-s', '-o', self._temp_file])

    def get_screenshot(self) -> str:
        self._free_path()
        self._take_screenshot()
        return _ExistanceChecker.is_exist(self._temp_file,
                                          error_msg='An error occurred while creating a screenshot')


class FileHandler:
    def __init__(self):
        self._screenshoter = _ScreenshotTaker('/tmp/brailler_temp_image.png')

    def get_file_path(self, file_path: str) -> str:
        if file_path:
            return _ExistanceChacker.is_exist(file_path,
                                              error_msg='The file does not exists')
        else:
            return self._screenshoter.get_screenshot()


class _SteppedInt:
    def __init__(self, value: int, step: int):
        self._step = step
        self._value = self.restrict_value(value, step)

    @staticmethod
    def restrict_value(value, step):
        value -= (value % step)
        return value

    @property
    def step(self):
        return (i for i in range(self._step))

    def __index__(self):
        return self._value

    def __iter__(self):
        return (i for i in range(0, self._value, self._step))


class _Monochromer:
    _WHITE = 255
    _BLACK = 0

    @classmethod
    def to_monochrome(cls, image, threshold):
        new_image = cls._convert_to_greyscale(image)
        new_image = cls._dithering(new_image, threshold)

        return new_image

    @staticmethod
    def _convert_to_greyscale(image):
        return image.convert('L')

    @classmethod
    def _dithering(cls, image, threshold):
        output_image = Image.new('L', image.size, cls._WHITE)

        color_depth = 8
        palette = [i * 255 // (color_depth - 1)
                   for i in range(color_depth - 1)]

        for y in range(1, image.height - 1):
            for x in range(1, image.width - 1):
                old_pixel = image.getpixel((x, y))

                if old_pixel / 255 < threshold:
                    new_pixel = cls._BLACK
                else:
                    new_pixel = cls._WHITE

                # new_pixel = min(palette, key=lambda x: abs(x - old_pixel))
                output_image.putpixel((x, y), new_pixel)
                quant_error = old_pixel - new_pixel

                image.putpixel(
                    (x + 1, y), image.getpixel((x + 1, y)) + quant_error * 7 // 16)
                image.putpixel(
                    (x - 1, y + 1), image.getpixel((x - 1, y + 1)) + quant_error * 3 // 16)
                image.putpixel(
                    (x, y + 1), image.getpixel((x, y + 1)) + quant_error * 5 // 16)
                image.putpixel(
                    (x + 1, y + 1), image.getpixel((x + 1, y + 1)) + quant_error * 1 // 16)

        return output_image


class _MonochromeImage:
    def __init__(self, image, threshold):
        self._image = image
        self._threshold = threshold

    def resize(self, width, height):
        self._image = self._image.resize((width, height))

    def autocontrast(self):
        self._image = ImageOps.autocontrast(self._image)

    def convert_to_monochrome(self):
        self._image = _Monochromer.to_monochrome(self._image, self._threshold)

    def get_pixel(self, x, y):
        return self._image.getpixel((x, y))


class BrailleImage():
    def __init__(self, image, symbols_x, symbols_y, threshold):
        self._monochrome_image = _MonochromeImage(image, threshold)
        self._monochrome_image.autocontrast()
        self._monochrome_image.resize(symbols_x * 2, symbols_y * 4)
        self._monochrome_image.convert_to_monochrome()

        self._width = _SteppedInt(symbols_x * 2, 2)
        self._height = _SteppedInt(symbols_y * 4, 4)

        self._braille_handler = BrailleHandler()

    def generate_image(self) -> str:
        '''Generates a list of "⣿" and returns it as a formatted string'''
        brailles_list = []
        for y in self._height:
            for x in self._width:
                colors = []

                for iny in self._height.step:
                    for inx in self._width.step:
                        colors.append(
                            self._monochrome_image.get_pixel(x + inx, y + iny))

                brailles_list.append(
                    self._braille_handler.get_symbol(colors))
            brailles_list.append('\n')

        return ''.join(brailles_list)
