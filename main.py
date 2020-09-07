import subprocess
import os
import io

from build_android import BuildAndroid
from build_ios import BuildIOS
from file_utils import *
from configparser import ConfigParser

from datetime import datetime


def build(project_path="", output="", apk_platform=""):
    """Build the ios/apk based on the given path.

    Parameters:
        path: destination of the Flutter project
    """

    # 1. Create the build folder and clear existing build
    build_ios_path, build_android_path = create_build_folder()

    # 2. Clear flutter previous build
    process = subprocess.Popen(['flutter', 'clean'],
                               cwd=project_path)

    rc = process.wait()

    # 3. Invoke flutter build apk
    if(output == 'apk' or output == 'all'):
        build_android(
            path=project_path, build_android_path=build_android_path, platform=apk_platform)

    # 4. Invoke flutter build ios
    if(output == 'ipa' or output == 'all'):
        build_ios(path=project_path, build_ios_path=build_ios_path)


def build_android(path="", build_android_path="", platform=""):
    """ Build Android APK
    """
    apk_platform = '--target-platform={}'.format(platform)
    process = subprocess.Popen(['flutter', 'build', 'apk', '--release', apk_platform],
                               cwd=path)
    rc = process.wait()

    # Android Build
    flutter_android_file_path = os.path.join(
        path, 'build', 'app', 'outputs', 'apk', 'release', 'app-release.apk')

    build_android_filepath = os.path.join(
        build_android_path, "app-release.apk")

    # Create Android Build Instance
    # provide source and build location
    android = BuildAndroid(flutter_android_file_path,
                           build_android_path, filename='app-release.apk')

    # Generate Android build
    android.generate()

    if android.is_apk_existed():
        print("Success: Android Build copy to {}".format(android.out))
    else:
        print("Failed to generate Build for Android")


def build_ios(path="", build_ios_path=""):
    """ Build iOS IPA
    """
    process = subprocess.Popen(['flutter', 'build', 'ios'],
                               cwd=path)

    rc = process.wait()

    # iOS Build
    flutter_ios_file_path = os.path.join(
        path, 'build', 'ios', 'iphoneos', 'Runner.app')

    build_ios_filename = os.path.join(build_ios_path, "Runner.ipa")

    ios = BuildIOS(flutter_ios_file_path, build_ios_path,
                   build_ios_filename, cwd=path)
    ios.generate()

    if ios.is_ipa_existed():
        dest = os.path.join(ios.out, ios.filename)
        print("Success: IPA Build copy to {}".format(dest))
    else:
        print("Failed to generate IPA for iOS")


def main():
    # Get Build Info
    configParser = ConfigParser()
    configParser.read('config.ini')

    buildInfo = configParser['BUILDINFO']

    if not buildInfo == None:
        project_path = buildInfo['flutter_path'] if not buildInfo['flutter_path'] is None else ''
        output = buildInfo['output'] if not buildInfo['output'] is None else 'both'
        apk_platform = buildInfo['apk_platform'] if not buildInfo['apk_platform'] is None else 'android-arm64'

        if project_path != '' and os.path.exists(project_path):
            build(project_path, output, apk_platform)
        else:
            print("Build Terminate. Could not find Flutter Project")

    else:
        print("Build Terminate: Could not find BuildInfo")


if __name__ == "__main__":
    main()
