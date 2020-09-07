import os
import platform
from shutil import copyfile, rmtree

import subprocess


def create_build_folder():
    """ Create a build folder /build/ios and /build/android
    """

    current_dir = os.getcwd()
    build_dir = os.path.join(current_dir, 'build')

    # Remove existing build folder
    if os.path.exists(build_dir):
        rmtree(build_dir)

    ios_path = os.path.join(build_dir, 'ios')
    android_path = os.path.join(build_dir, 'android')

    # Recreate the build folders (build/ios and build/android)
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
        os.makedirs(ios_path)
        os.makedirs(android_path)

    return ios_path, android_path


def clear_file_content(path):
    """ Delete all files in a given path
    """
    for f in os.listdir(path):
        os.remove(os.path.join(path, f))


def is_file_exist(file_path=""):
    return os.path.isfile(file_path)


def move_file(src="", dest=""):
    destination = copyfile(src, dest)
    print(destination)


def get_creation_date(path_to_file=""):
    if platform.system() == "Windows":
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime
