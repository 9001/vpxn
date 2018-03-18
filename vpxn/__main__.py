#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import print_function


"""vpxn: vpxnitro, time-sliced vpx encoder """
__version__   = "0.1"
__author__    = "ed <a@ocv.me>"
__credits__   = ["stackoverflow.com"]
__license__   = "MIT"
__copyright__ = 2018


import time
import sys

if not 'vpxn' in sys.modules:
	print('\r\n  vpxnitro must be launched as a module.\r\n  in the project root, run this:\r\n\r\n    python -m vpxn\r\n')
	sys.exit(1)

from .ffmpeg import *


def run():
	ff = FFmpeg([
		'ffmpeg',
		'-y',
		'-i', 'C:/Users/ed/Downloads/croissant.mp4',
		'-acodec', 'copy',
		'-vcodec', 'libx264',
		'fgsfds.mkv'])
	
	while ff.busy:
		time.sleep(1)


if __name__ == '__main__':
	run()
