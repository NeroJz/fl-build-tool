import os
import platform

from shutil import copyfile
from datetime import datetime
from configparser import ConfigParser


class Build:
    def __init__(self, src="", out="", filename=""):
        super().__init__()
        self.src = src
        self.out = out
        self.filename = filename
        self.cfg = ConfigParser()
        self.cfg.read("config.ini")

    def move_file(self):
        dest = os.path.join(self.out, self.filename)
        self.destination = copyfile(self.src, dest)

    def is_source_file_exist(self):
        return os.path.exists(self.src)

    def is_out_file_exist(self):
        return os.path.isfile(self.out)

    def is_new_build(self):
        globalinfo = self.cfg['GLOBALINFO']
        if self.is_source_file_exist():
            dt_file = datetime.fromtimestamp(self.get_creation_date())
            dt_now = datetime.now()

            diff = dt_now - dt_file
            min = round(diff.seconds / 60)

            print("Min: {}".format(min))

            return min < int(globalinfo['temp_max_time'])

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
