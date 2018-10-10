import os

def replace_txt(src):
	c = 0
	dirs = os.listdir(src)
	for d in dirs:
		t = os.path.join(src, d, 'thrift', 'wrapper2')
		if os.path.exists(t) and os.path.isdir(t):
			jfs = os.listdir(t)

			for jf in jfs:
				file_path = os.path.join(t, jf)
				if jf.endswith('java') and os.path.isfile(file_path):
					content = None
					with open(file_path, 'r') as f:
						content = f.read()
						phrase = 'package com.vng.zing.' + d + '.thrift.wrapper;'
						target = 'package com.vng.zing.' + d + '.thrift.wrapper2;'
						content = content.replace(phrase, target)
						# print 'new content = ' + content
					with open(file_path, 'w') as f:
						f.write(content)

replace_txt('/home/tamvm/Projects/jzcommon-bewrapper/src/main/java/com/vng/zing')