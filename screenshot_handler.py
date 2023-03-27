import os
import subprocess


class ScreenshotHandler:
    @staticmethod
    def take_screenshot() -> str:
        temp_file = '/tmp/brailler_temp_image.png'
        
        subprocess.call(['scrot', '-s', '-o', temp_file])
        if os.path.exists(temp_file):
            return temp_file
        else:
            raise FileExistsError(
                'An error occurred while creating a screenshot')
