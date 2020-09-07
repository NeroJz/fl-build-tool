from build import Build
import os


class BuildAndroid(Build):
    def __init__(self, src="", out="", filename=""):
        super().__init__(src, out, filename)

    def generate(self):
        if self.is_new_build():
            self.move_file()

    def is_apk_existed(self):
        dest = os.path.join(self.out, self.filename)
        return os.path.exists(dest)
