import os
import subprocess

from braille_handler import BrailleHandler


class ExistanceChacker:
    @staticmethod
    def is_exist(file_path, error_msg):
        if os.path.exists(file_path):
            return file_path
        else:
            raise FileExistsError(error_msg)


class ScreenshotTaker:
    def __init__(self, temp_file):
        self._temp_file = temp_file

    def _free_path(self):
        if os.path.exists(self._temp_file):
            os.remove(self._temp_file)

    def _take_screenshot(self):
        subprocess.call(['scrot', '-s', '-o', self._temp_file])

    def get_screenshot(self):
        self._free_path()
        self._take_screenshot()
        return ExistanceChacker.is_exist(self._temp_file,
                                         error_msg='An error occurred while creating a screenshot')


class FileHandler:
    def __init__(self):
        self._screenshot_taker = ScreenshotTaker('/tmp/brailler_temp_image.png')

    def get_file_path(self, file_path):
        if file_path:
            return ExistanceChacker.is_exist(file_path,
                                             error_msg='The file does not exists')
        else:
            return self._screenshot_taker.get_screenshot()


class SteppedInt:
    def __init__(self, value, step):
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


class BrailleImage:
    def __init__(self, image, width, height, bright_bound):
        self._width = SteppedInt(width, 2)
        self._height = SteppedInt(height, 4)
        self._image = image.resize((self._width, self._height))
        self._bright_bound = bright_bound

        self._braille_handler = BrailleHandler()

    def generate_image(self):
        brailles_list = []
        for y in self._height:
            for x in self._width:
                colors = []

                for iny in self._height.step:
                    for inx in self._width.step:
                        colors.append(self._image.getpixel((x + inx, y + iny)))

                brailles_list.append(
                    self._braille_handler.get_symbol(colors, self._bright_bound))
            brailles_list.append('\n')

        return ''.join(brailles_list)
