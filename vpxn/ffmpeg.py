#!/bin/bash
import subprocess as sp
import datetime as dt
import threading
import platform
import sys
import os
import re

PY2 = (sys.version_info[0] == 2)
WINDOWS = platform.system() == 'Windows'

if PY2:
	from Queue import Queue
else:
	from queue import Queue


class FFmpeg(object):
	def __init__(self, cmd, stdout_sink=None):
		self.datasink = stdout_sink;
		self.outlines = Queue()
		self.errlines = Queue()
		self.outbuf = b''
		self.errbuf = b''
		
		self.env = os.environ.copy()
		self.env['AV_LOG_FORCE_COLOR'] = '1'

		self.ff = sp.Popen(cmd, env=self.env, stdout=sp.PIPE, stderr=sp.PIPE)
		self.busy = True

		threading.Thread(target=self.textreader, args=([[
			self.ff.stderr, self.errlines, self.errbuf]])).start()

		if stdout_sink is None:
			threading.Thread(target=self.textreader, args=([[
				self.ff.stdout, self.outlines, self.outbuf]])).start()
		else:
			threading.Thread(target=self.binreader).start()


	def binreader(self):
		while self.ff.poll() is None:
			chunk = src.read(4096)
			self.datasink.process(chunk)
			if chunk is None:
				break

		self.busy = False
		print('eof')


	def textreader(self, objs):
		src, lines, buf = objs
		while self.ff.poll() is None:
			chunk = src.read(1)
			if chunk is None:
				time.sleep(0.01)
				continue
			buf += chunk
			if chunk == b'\r' or chunk == b'\n':
				buf = buf.decode('utf-8')
				if buf.rstrip() == u'':
					buf = b''
					continue
				
				lines.put(buf)
				print('{0:05d} {1}'.format(len(buf), buf[:72]))
				buf = b''

		self.busy = False
		print('eof')
