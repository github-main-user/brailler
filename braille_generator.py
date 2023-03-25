from symbol_handler import SymbolHandler


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
