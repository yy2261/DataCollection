import requests
import time


def parseUrl(url, after, num):
	f = open('name_'+str(num), 'w')
	payload = {'after':after}
	res = requests.get(url, params=payload)
	lines = res.text.split('<article class=')

	for i in range(len(lines)):
		if i == len(lines)-1:
			statements = lines[i].split('\n')
			for statement in statements:
				if 'name="after"' in statement:
					oneAfter = statement.split('value="')[1].split('">')[0]
					after.append(oneAfter)

		if 'border-bottom border-gray-light py-4' in lines[i]:
			para = lines[i].split('border-bottom border-gray-light py-4')[1].split('</h3>')[0]
			addr = para.split('<a href="')[1].split('">')[0]
			f.write(addr+'\n')
			print addr

	time.sleep(5)
	f.close()
	num += 1
	parseUrl(url, after, num)

if __name__ == '__main__':
	num = 0
	url = 'https://github.com/topics/java?l=java&o=desc&s=stars'
	after = []
	parseUrl(url, after, num)