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