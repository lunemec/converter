Converter
=========

A simple python script to iterate over movies in given directory and convert them
using ``ffmpeg`` to ``x265`` codec (mkv container).


Installation
------------
Download the ``converter.zip`` file from releases, then:

	python converter.zip PATH_TO_CONVERT


How it works
------------
It scans given directory for files with specified extensions ('.mp4', '.mkv', '.avi').
Then it checks if there is a stamp that conversion ended, in that case, file is already
converted and we skip it. If there is only stamp saying conversion started, it means
we haven't finished previous conversion of this file and we want to convert it again.

In this case, we refresh start stamp, and start the conversion. After the conversion is
finished, we create end stamp, delete the start stamp and delete the original file
(if specified in cmdline arguments).

File names
----------
Some files may have strange unicode charcters in their name. This causes errors on printing
which file is being converted. When you try to find your file and fail, look for '?' characters
inside the printed text and replace them with * for searching in your system. These are the
unprintable characters replaced to be visible. You may also fix this issue by renaming
that file.