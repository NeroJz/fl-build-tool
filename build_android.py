from build import Build


class BuildAndroid(Build):
    def __init__(self, src="", out=""):
        super().__init__(src, out)

    def generate(self):
        if self.is_new_build():
            self.move_file()
