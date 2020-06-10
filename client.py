import requests
from threading import Thread
import os
from base64 import b64encode, b64decode
from time import time
timeRecord = []

def dos(i):
	global timeRecord

	nowtime = time()
	print(i, 'launch')

	fakesession = os.urandom(20)
	fakesession = str(b64encode(fakesession), 'ascii')
	cookies = {'SESSION_ID' : fakesession}
	r = requests.get('http://localhost:8000/service', cookies=cookies)

	endtime = time()
	print(i, 'finish')
	timeRecord.append(endtime - nowtime)

N = 100
Ts = [Thread(target=dos, args=(t,)) for t in range(N)]

for T in Ts:
	T.start()

for T in Ts:
	T.join()

print('End')
print('Max response time =', max(timeRecord))
print('All time record = ', timeRecord)

