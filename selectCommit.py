import requests
import sys
import time
import os

'''
cannot deal with branch labels
'''

def getCommit(url, text, commitList, f):
	lines = text.split('\n')
	for line in lines:
		if 'data-pjax="true"' in line:
			commitTitle = line.split('class="message"')[1].split('title=')[1]
			commitLink = line.split('class="message"')[-2].split('<a href="')[-1].split('" ')[0]
			commitList = [commitTitle, commitLink]

			# add keywords here
			if 'inject' in line or 'leak' in line or 'overflow' in line:
				try:
					f.write(commitTitle+'\n')
				except:
					f.write('some illegal characters...\n')
					
				f.write('https://github.com/'+commitLink+'\n\n')
	return commitList


def getLast(url):
	last = url.split('commit/')[1]
	return last

def getNum(url):
	url = url.split('/commits')[0]
	res = requests.get(url)
	paras = res.text.split('<li')
	for para in paras:
		if 'class="commits"' in para:
			num = para.split('<span class="num text-emphasized">')[1].split('</span>')[0].strip(' ').strip('\n').strip(' ')
			return num

def selectCommit(url, filename):
	f = open(filename, 'w')
	if '?' not in url:
		num = getNum(url)
		print num+' commits...'
	oldurl = ''
	commitList = ['pen', 'apple']
	while oldurl != url:
		res = requests.get(url)
		commitList = getCommit(url, res.text, commitList, f)
		last = getLast(commitList[1])
		oldurl = url
		url = oldurl.split('?')[0]
		url = url+'?after='+last+'+0'
		print url
		time.sleep(5)
	f.close()


if __name__ == '__main__':

	# input1: url of the commit page. e.g.:https://github.com/iluwatar/java-design-patterns/commits/master
	# input2: the path of file to write. e.g.: /home/lulu/commits.txt
	selectCommit(sys.argv[1], sys.argv[2])
	os.system('supertux2')