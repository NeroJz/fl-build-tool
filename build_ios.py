from build import Build


class BuildIOS(Build):
    def __init__(self, src='', out='', filename=''):
        super().__init__(src=src, out=out, filename=filename)

    def generate(self):
        pass
