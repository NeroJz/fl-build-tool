import subprocess
import argparse
import os
import io

from build_android import BuildAndroid
from file_utils import *


from datetime import datetime


def build(path=""):
    """Build the ios/apk based on the given path.

    Parameters:
        path: destination of the Flutter project
    """

    # 1. Create the build folder and clear existing build
    build_ios_path, build_android_path = create_build_folder()

    # 2. Clear flutter previous build
    # process = subprocess.Popen(['flutter', 'clean'],
    #                            cwd=path)

    # rc = process.wait()

    # 3. Invoke flutter build apk
    # process = subprocess.Popen(['flutter', 'build', 'apk'],
    #                            cwd=path)

    # rc = process.wait()

    # Android Build
    flutter_android_file_path = os.path.join(
        path, 'build', 'app', 'outputs', 'apk', 'release', 'app-release.apk')

    build_android_filepath = os.path.join(
        build_android_path, "app-release.apk")

    # Create Android Build Instance
    # provide source and build location
    # android = BuildAndroid(flutter_android_file_path, build_android_filepath)

    # Generate Android build
    # android.generate()

    # if android.is_out_file_exist():
    #     print("Success: Android Build copy to {}".format(android.out))
    # else:
    #     print("Failed to generate Build for Android")

    # 3. Invoke flutter build apk
    # process = subprocess.Popen(['flutter', 'build', 'ios'],
    #                            cwd=path)

    # rc = process.wait()

    # iOS Build
    flutter_ios_file_path = os.path.join(
        path, 'build', 'ios', 'iphoneos', 'Runner.app')

    build_ios_filepath = os.path.join(build_ios_path, "Runner.ipa")


def main():
    project_path = ""

    if(os.path.exists(project_path)):
        build(path=project_path)
    else:
        print("Path not existed! Program has exited!")


if __name__ == "__main__":
    main()
