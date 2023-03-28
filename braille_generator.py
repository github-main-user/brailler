class SymbolHandler:
    brailles = '⠁⠂⠃⠄⠅⠆⠇⡀⡁⡂⡃⡄⡅⡆⡇⠈⠉⠊⠋⠌⠍⠎⠏⡈⡉⡊⡋⡌⡍⡎⡏⠐⠑⠒⠓⠔⠕⠖⠗⡐⡑⡒⡓⡔⡕⡖⡗⠘⠙⠚⠛⠜⠝⠞⠟⡘⡙⡚⡛⡜⡝⡞⡟⠠⠡⠢⠣⠤⠥⠦⠧⡠⡡⡢⡣⡤⡥⡦⡧⠨⠩⠪⠫⠬⠭⠮⠯⡨⡩⡪⡫⡬⡭⡮⡯⠰⠱⠲⠳⠴⠵⠶⠷⡰⡱⡲⡳⡴⡵⡶⡷⠸⠹⠺⠻⠼⠽⠾⠿⡸⡹⡺⡻⡼⡽⡾⡿⢀⢁⢂⢃⢄⢅⢆⢇⣀⣁⣂⣃⣄⣅⣆⣇⢈⢉⢊⢋⢌⢍⢎⢏⣈⣉⣊⣋⣌⣍⣎⣏⢐⢑⢒⢓⢔⢕⢖⢗⣐⣑⣒⣓⣔⣕⣖⣗⢘⢙⢚⢛⢜⢝⢞⢟⣘⣙⣚⣛⣜⣝⣞⣟⢠⢡⢢⢣⢤⢥⢦⢧⣠⣡⣢⣣⣤⣥⣦⣧⢨⢩⢪⢫⢬⢭⢮⢯⣨⣩⣪⣫⣬⣭⣮⣯⢰⢱⢲⢳⢴⢵⢶⢷⣰⣱⣲⣳⣴⣵⣶⣷⢸⢹⢺⢻⢼⢽⢾⢿⣸⣹⣺⣻⣼⣽⣾⣿'

    @classmethod
    def set_empty_symbol(cls, string):
        if not string:
            print(
                '[!] Was given string with zero length, will be use default empty char')
            string = '⠀'
        cls.brailles = string[:1] + cls.brailles

    @classmethod
    def set_invert_state(cls, invert):
        cls.threshold = 0 if invert else 255

    @classmethod
    def get_symbol(cls, colors: list):
        '''Input 8 colors (just brightness 0...255) -> Output "⣿" '''
        byte = 0

        for grey_color in colors:
            byte <<= 1  # shift to left (0b0001 => 0b0010)

            if grey_color == cls.threshold:
                byte |= 1  # turn on last bit (0b0010 => 0b0011)

        return cls.brailles[byte]


class BrailleGenerator:
    @staticmethod
    def generate_braille_text(image, empty, invert) -> str:
        '''Generates a list of "⣿" and returns it as a formatted string'''
        SymbolHandler.set_empty_symbol(empty)
        SymbolHandler.set_invert_state(invert)

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
