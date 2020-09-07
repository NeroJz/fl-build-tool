import os
import subprocess
import platform

from datetime import datetime

from build import Build


class BuildIOS(Build):
    def __init__(self, src='', out='', filename='', cwd=''):
        super().__init__(src=src, out=out, filename=filename)
        self.archive_path = os.path.join(self.out, 'Runner.xcarchive')
        self.cwd = cwd

    def generate(self):
        """ Generate the archive and iPA"""
        if self.is_new_build():
            # Archive the Build
            self.archive()

            # Export the IPA
            self.export()

    def archive(self):
        """Archive the file
            Steps:
            1. Get the archive info from the config.ini
            2. Paired the commands with the archive info
            3. Execute the xcode archive command
        """

        # Step 1
        archiveinfo = self.cfg['ARCHIVEINFO']

        # Step 2
        cmd_arr = ['xcodebuild',
                   '-workspace', archiveinfo['workspace'],
                   '-scheme', archiveinfo['scheme'],
                   '-sdk', archiveinfo['sdk'],
                   '-configuration', archiveinfo['configuration'],
                   'archive', archiveinfo['archive'],
                   '-archivePath', self.archive_path]

        # Step 3
        process = subprocess.Popen(cmd_arr, cwd=self.cwd)
        rc = process.wait()

        # For delete purpose in future
        if self.is_archive_existed():
            os.chmod(self.archive_path, 0o777)

    def is_archive_existed(self):
        """ Check archive is existed
        """
        return os.path.exists(self.archive_path)

    def get_created_metadata(self, path=""):
        if platform.system() == "Windows":
            return os.path.getctime(path)
        else:
            stat = os.stat(path)
            try:
                return stat.st_birthtime
            except AttributeError:
                return stat.st_mtime

    def is_new_archive(self):
        """ Check the archive is newly created
        """
        globalinfo = self.cfg['GLOBALINFO']
        if self.is_archive_existed():
            dt_file = datetime.fromtimestamp(
                self.get_created_metadata(self.archive_path))
            dt_now = datetime.now()

            diff = dt_now - dt_file
            min = round(diff.seconds / 60)

            return min < int(globalinfo['temp_max_time'])

        return False

    def export(self):
        if self.is_new_archive():
            self.build_ipa()
        else:
            print("New archive not found! Generating IPA has exited!")

    def build_ipa(self):
        """ Generate the IPA build
            Steps:
            1. Get the export option plist
            2. Paired the export option with Xcode build command
            3. Execute the build command
        """
        archiveinfo = self.cfg['ARCHIVEINFO']

        # Step 1
        # Get Export Options .plist
        exportOptions = archiveinfo['exportOptions']

        # Exported filename
        dest = os.path.join(self.out, self.filename)

        # Step 2
        cmd_arr = ['xcodebuild',
                   '-exportArchive',
                   '-archivePath', self.archive_path,
                   '-exportOptionsPlist', exportOptions,
                   '-exportPath', dest]
        # Step 3
        process = subprocess.Popen(cmd_arr)
        rc = process.wait()

        if self.is_new_ipa_created():
            print("New IPA generated! You can find the IPA at: {}".format(dest))
        else:
            print("Failed to generate new IPA!")

    def is_new_ipa_created(self):
        globalinfo = self.cfg['GLOBALINFO']

        dest = os.path.join(self.out, self.filename)
        if os.path.exists(dest):
            dt_file = datetime.fromtimestamp(self.get_created_metadata(dest))
            dt_now = datetime.now()

            diff = dt_now - dt_file
            min = round(diff.seconds / 60)

            return min < int(globalinfo['temp_max_time'])

        return False
