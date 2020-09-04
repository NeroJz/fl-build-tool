import os
import platform

from shutil import copyfile
from datetime import datetime

TEMP_MAX_TIME = 3600


class Build:
    def __init__(self, src="", out="", filename=""):
        super().__init__()
        self.src = src
        self.out = out

    def move_file(self):
        self.destination = copyfile(self.src, self.out)

    def is_source_file_exist(self):
        return os.path.isfile(self.src)

    def is_out_file_exist(self):
        return os.path.isfile(self.out)

    def is_new_build(self):
        if self.is_source_file_exist():
            dt_file = datetime.fromtimestamp(self.get_creation_date())
            dt_now = datetime.now()

            diff = dt_now - dt_file
            min = round(diff.seconds / 60)

            print("Min: {}".format(min))

            return min < TEMP_MAX_TIME

        return False

    def get_creation_date(self):
        if platform.system() == "Windows":
            return os.path.getctime(self.src)
        else:
            stat = os.stat(self.src)
            try:
                return stat.st_birthtime
            except AttributeError:
                return stat.st_mtime
