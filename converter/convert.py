# -*- encoding: utf-8 -*-

import os
import subprocess
import traceback

from stamp import (
    create_end_stamp,
    create_start_stamp,
    has_end_stamp,
    has_start_stamp,
)
from utils import text


class ConvertedFile():

    def __init__(self, binary, video_formats, filepath, delete, convert=True):
        """
        @param filepath: absolute filepath to the file being converted
        @param delete: True/False if we want the original to be deleted
        @param convert: for testing purposes, if False we don't call ffmpeg.
        """
        self.binary = binary
        self.video_formats = video_formats
        self.filepath_in = filepath
        self.delete = delete

        self.path, self.ext = os.path.splitext(filepath)

        # Temporary path used during the convert.
        self.filepath_out = '{}.output.mkv'.format(self.path)
        # Filepath of the resulting file. The temporary file will be renamed to
        # this.
        self.filepath = '{}.mkv'.format(self.path)

        self.convert = convert

    def remove_original(self):
        """
        Removes original file that has been successfully converted and moves the
        newly converted file to its name.
        """
        try:
            os.remove(self.filepath_in)
            os.rename(self.filepath_out, self.filepath)
        except OSError:
            # This means the file is directory.
            pass

    def should_convert(self):
        """
        Checks if the file already has end_stamp, which means it is already
        converted and no action is required.
        If the stamp is missing, we want to convert, in which case, we check for
        the file's extension and decide accordingly.
        """
        if not has_end_stamp(self.filepath_in) and '.output.' not in self.filepath_in:
            if self.ext in self.video_formats:
                return True

        return False

    def convert_file(self):
        """
        Handles converting of single file. It creates stamps signaling the file
        is being converted and that it was finished.

        Returns filepath of the input file if there is an error.
        """
        if self.should_convert():
            if has_start_stamp(self.filepath_in):
                if os.path.exists(self.filepath_out):
                    os.remove(self.filepath_out)

            try:
                create_start_stamp(self.filepath_in)
                text('Converting: {}'.format(self.filepath_in))
                with open('{}.convert'.format(self.path), 'w') as convert_out:
                    cmd = [self.binary, '-y', '-i', self.filepath_in, '-sn',
                           '-x265-params', 'crf=28', '-c:v', 'libx265',
                           self.filepath_out]

                    if self.convert:
                        subprocess.check_call(
                            cmd,
                            stdout=convert_out,
                            stderr=convert_out
                        )
                create_end_stamp(self.filepath_in)

                if self.delete:
                    self.remove_original()
            except subprocess.CalledProcessError:
                traceback.print_exc()
                return self.filepath_in
