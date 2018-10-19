import os
from subprocess import call

def diff_all():
	base = '/home/tamvm/Downloads/20181019scriptsHistory'
	versions = [os.path.join(base, d) for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))]
	versions.sort()
	# print(versions)

	for i in range(0, len(versions) - 1):
		c = os.path.join(versions[i], 'TplService')
		n = os.path.join(versions[i+1], 'TplService')
		# print ('comparing ' + os.path.basename(versions[i]) + ' and ' + os.path.basename(versions[i + 1]) + ' ================== ')
		dirs = ['runservice', 'cmd']
		for d in dirs:
			cd = os.path.join(c, d)
			nd = os.path.join(n, d)
			if os.path.exists(cd) and not os.path.exists(nd):
				print(d + ' is removed')
			elif not os.path.exists(cd) and os.path.exists(nd):
				print(d + ' is added ')
			elif os.path.exists(cd) and os.path.exists(nd):
				print(call(['diff', cd, nd]))


if __name__ == '__main__':
	diff_all()