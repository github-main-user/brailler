import strings


class SymbolHandler:
    @staticmethod
    def get_symbol(colors: list):
        '''Input 8 colors (just brightness 0...255) -> Output "⣿" '''
        brailles = strings.BRAILLES
        byte = 0

        for grey_color in colors:
            byte <<= 1  # shift to left (0b0001 => 0b0010)

            if grey_color == 255:
                byte |= 1  # turn on last bit (0b0010 => 0b0011)

        return brailles[byte]
