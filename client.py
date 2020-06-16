import requests
from threading import Thread
import os
from base64 import b64encode, b64decode
from time import time, sleep
from bs4 import BeautifulSoup
from random import random
timeRecord = []

def dos(i, n):
	global timeRecord

	nowtime = time()
	sleep(random() * 3)
	for ep in range(n):
		print(i, 'launch', ep)

		fakesession = os.urandom(20)
		fakesession = str(b64encode(fakesession), 'ascii')
		cookies = {'SESSION_ID' : fakesession}
		r = requests.get('http://localhost:8000/service', cookies=cookies)
		dest = r.url.split('/')[-1]
		while dest == 'challenge':
			soup = BeautifulSoup(r.text, 'html.parser')
			t = soup.find(id='timecounter').get_text().strip(' ')
			t = int(t)
			sleep(t)
			r = requests.get('http://localhost:8000/service', cookies=cookies)
			dest = r.url.split('/')[-1]
		endtime = time()
		print(i, 'finish, result=', r.text)
	timeRecord.append(endtime - nowtime)

N = 100
n = 5
Ts = [Thread(target=dos, args=(t, n)) for t in range(N)]

for T in Ts:
	T.start()

for T in Ts:
	print('Max response time =', max(timeRecord))
	print('Average response time =', sum(timeRecord) / len(timeRecord))
	T.join()

print('End')

print('All time record = ', timeRecord)

