import strings


class _ColorHelper:
    def get_brightness(self, grey_color) -> float:
        return grey_color / 255


class BrailleHandler:
    def __init__(self):
        self._color_helper = _ColorHelper()
        self._brailles = strings.BRAILLES

    def _byte_to_symbol(self, byte):
        '''Input 11000011 -> Output "⢣" '''
        return self._brailles[byte]

    def get_symbol(self, colors: list):
        '''Input [(r, g, b), (r, g, b), ...] -> Output "⣿" '''
        byte = 0

        for grey_color in colors:
            byte <<= 1  # shift to left (0b0001 => 0b0010)

            if grey_color == 255:
                byte |= 1  # turn on last bit (0b0010 => 0b0011)

        return self._byte_to_symbol(byte)
