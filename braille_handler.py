import strings


class ColorHelper:
    def get_brightness(self, r, g, b) -> float:
        return (r / 255 + g / 255 + b / 255) / 3


class SequenceHelper:
    def even_out_sequence(self, colors, num):
        if len(colors) < num:
            colors.extend([(0, 0, 0) for i in range(num - len(colors))])
        else:
            colors[:] = colors[:num]


class BrailleHandler:
    def __init__(self):
        self._color_helper = ColorHelper()
        self._sequence_helper = SequenceHelper()
        self._brailles = strings.BRAILLES

    def _byte_to_symbol(self, byte):
        '''Input 11000011 -> Output "⢣" ''' 
        return self._brailles[byte]

    def get_symbol(self, colors: list, bright_bound: float):
        '''Input [(r, g, b), (r, g, b), ...] -> Output "⣿" '''
        byte = 0
        self._sequence_helper.even_out_sequence(colors, 8)

        for r, g, b in colors:
            bright = self._color_helper.get_brightness(r, g, b)

            byte <<= 1  # shift to left (0b0001 => 0b0010)
            if bright >= bright_bound:
                byte |= 1  # turn on last bit (0b0010 => 0b0011)

        return self._byte_to_symbol(byte)
