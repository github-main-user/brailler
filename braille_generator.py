class SymbolHandler:
    def __init__(self):
        self._BRAILLES = '⠁⠂⠃⠄⠅⠆⠇⡀⡁⡂⡃⡄⡅⡆⡇⠈⠉⠊⠋⠌⠍⠎⠏⡈⡉⡊⡋⡌⡍⡎⡏⠐⠑⠒⠓⠔⠕⠖⠗⡐⡑⡒⡓⡔⡕⡖⡗⠘⠙⠚⠛⠜⠝⠞⠟⡘⡙⡚⡛⡜⡝⡞⡟⠠⠡⠢⠣⠤⠥⠦⠧⡠⡡⡢⡣⡤⡥⡦⡧⠨⠩⠪⠫⠬⠭⠮⠯⡨⡩⡪⡫⡬⡭⡮⡯⠰⠱⠲⠳⠴⠵⠶⠷⡰⡱⡲⡳⡴⡵⡶⡷⠸⠹⠺⠻⠼⠽⠾⠿⡸⡹⡺⡻⡼⡽⡾⡿⢀⢁⢂⢃⢄⢅⢆⢇⣀⣁⣂⣃⣄⣅⣆⣇⢈⢉⢊⢋⢌⢍⢎⢏⣈⣉⣊⣋⣌⣍⣎⣏⢐⢑⢒⢓⢔⢕⢖⢗⣐⣑⣒⣓⣔⣕⣖⣗⢘⢙⢚⢛⢜⢝⢞⢟⣘⣙⣚⣛⣜⣝⣞⣟⢠⢡⢢⢣⢤⢥⢦⢧⣠⣡⣢⣣⣤⣥⣦⣧⢨⢩⢪⢫⢬⢭⢮⢯⣨⣩⣪⣫⣬⣭⣮⣯⢰⢱⢲⢳⢴⢵⢶⢷⣰⣱⣲⣳⣴⣵⣶⣷⢸⢹⢺⢻⢼⢽⢾⢿⣸⣹⣺⣻⣼⣽⣾⣿'

    def set_empty_char(self, string: str):
        if not string:
            print(
                '[!] Was given string with zero length, will be use default empty char')
            string = '⠀'
        self._BRAILLES = string[:1] + self._BRAILLES

    def set_invert_state(self, invert_state: bool):
        '''invert_state = True
         - (not True * 255) = False * 255 = 0
           --------------------
           invert_state = False
         - (not False) * 255 = True * 255 = 255
         '''
        self._THRESHOLD = (not invert_state) * 255

    def get_symbol(self, colors: list):
        '''Input 8 colors (just brightness 0...255) -> Output "⣿" '''
        byte = 0

        for grey_color in colors:
            byte <<= 1  # shift to left (0b0001 => 0b0010)

            if grey_color == self._THRESHOLD:
                byte |= 1  # turn on last bit (0b0010 => 0b0011)

        return self._BRAILLES[byte]


class BrailleGenerator:
    def __init__(self, image, symbol_handler):
        self.image = image
        self.symbol_handler = symbol_handler

    def generate_text(self) -> str:
        '''Generates a list of "⣿" and returns it as a formatted string'''
        brailles_list = []

        for y in range(0, self.image.height, 4):
            for x in range(0, self.image.width, 2):
                colors = []

                for iny in range(4):
                    for inx in range(2):
                        colors.append(self.image.getpixel((x + inx, y + iny)))

                brailles_list.append(self.symbol_handler.get_symbol(colors))
            brailles_list.append('\n')

        return ''.join(brailles_list)
