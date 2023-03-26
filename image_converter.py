from PIL import Image, ImageOps


class ImageConverter:
    @staticmethod
    def to_monochrome(image, threshold) -> Image:
        new_image = ImageOps.autocontrast(image.convert('L'))
        output_image = Image.new('L', new_image.size, 255)

        W = image.width
        H = image.height

        color_depth = 8
        palette = [i * 255 // (color_depth - 1)
                   for i in range(color_depth - 1)]

        for y in range(H):
            for x in range(W):
                old_pixel = new_image.getpixel((x, y))

                if old_pixel / 255 < threshold:
                    new_pixel = 0
                else:
                    new_pixel = 255

                output_image.putpixel((x, y), new_pixel)
                quant_error = old_pixel - new_pixel

                new_image.putpixel((x % (W - 1) + 1, y),
                                   new_image.getpixel((x % (W - 1) + 1, y)) + quant_error * 7 // 16)
                new_image.putpixel((x - 1, y % (H - 1) + 1),
                                   new_image.getpixel((x - 1, y % (H - 1) + 1)) + quant_error * 3 // 16)
                new_image.putpixel((x, y % (H - 1) + 1),
                                   new_image.getpixel((x, y % (H - 1) + 1)) + quant_error * 5 // 16)
                new_image.putpixel((x % (W - 1) + 1, y % (H - 1) + 1),
                                   new_image.getpixel((x % (W - 1) + 1, y % (H - 1) + 1)) + quant_error * 1 // 16)

        return output_image
