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


class BrailleGenerator:
    @staticmethod
    def generate_braille_text(image) -> str:
        '''Generates a list of "⣿" and returns it as a formatted string'''
        brailles_list = []
        for y in range(0, image.height, 4):
            for x in range(0, image.width, 2):
                colors = []

                for iny in range(4):
                    for inx in range(2):
                        colors.append(image.getpixel((x + inx, y + iny)))

                brailles_list.append(SymbolHandler.get_symbol(colors))
            brailles_list.append('\n')

        return ''.join(brailles_list)
