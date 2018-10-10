import os

def compare_dir(ref, src):
	c = 0
	dirs = os.listdir(ref)
	for d in dirs:
		wd = os.path.join(ref, d, 'thrift', 'wrapper')
		# print ('check dir ' + wd)
		if os.path.exists(wd) and os.path.isdir(wd):
			for f in os.listdir(wd):
				if f.endswith('Client.java') or f.endswith('ClientWithCache.java') or f.endswith('ClientWithQueue.java') or f.endswith('.java'):
					# print(os.path.join(wd, f))
					c += 1
					check = os.path.join(src, d, 'thrift', 'wrapper', f)

					if not (os.path.exists(check) and os.path.isfile(check)):
						print (check + ' is not found ')

	print ('found ' + str(c) + ' wrappers ')



if __name__ == '__main__':
	compare_dir('/home/tamvm/Projects/corelib-java/src/jzcommon-corelib/src/com/vng/zing', '/home/tamvm/Projects/jzcommon-bewrapper/src/main/java/com/vng/zing')
