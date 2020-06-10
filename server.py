from flask import Flask, render_template, request, make_response, redirect, url_for
from cookies_and_tokens import *
from threading import Thread
from time import time, sleep
from Crypto.Util.number import getPrime
import copy

webService = Flask(__name__)

webState = dict()
webState['people_counter'] = 0
webState['ratio'] = 1
webState['timelock'] = 0
webState['counter_threhold'] = 50
webState['ratio_threhold'] = 2

def webMonitor():
	global webState

	dt = 2
	preState = copy.deepcopy(webState)
	while True:
		delta_people = webState['people_counter'] - preState['people_counter']
		webState['ratio'] = delta_people / dt

		print('Service Capacity:', webState['counter_threhold'])
		print('Service Popularity:', webState['people_counter'])
		print('Service InRatio:', webState['ratio'])
		print('Service Now Timelock:', webState['timelock'])
		print('==============================')

		if webState['people_counter'] < webState['counter_threhold'] and \
			webState['ratio'] < webState['ratio_threhold']:
			webState['timelock'] = 0
		if webState['people_counter'] >= webState['counter_threhold']:
			webState['timelock'] += (webState['people_counter'] - webState['counter_threhold']) * 3
		if webState['ratio'] >= webState['ratio_threhold']:
			webState['timelock'] += (webState['ratio'] - webState['ratio_threhold']) * 5
		sleep(dt)



Thread(target=webMonitor).start()

@webService.route('/')
def index():
	resp = make_response(render_template('index.html'))
	
	s = request.cookies.get('SESSION_ID')
	if s == None:
		s = generateSessionId()
		resp.set_cookie('SESSION_ID', s)


	return resp

@webService.route('/service')
def importantService():

	s = request.cookies.get('SESSION_ID')
	if s == None:
		return redirect(url_for('index'))



	webState['people_counter'] += 1


# Service

	s = getPrime(2000)

# Service

	webState['people_counter'] -= 1
	return str(s)




if __name__ == '__main__':
	webService.run(host='0.0.0.0', port=8000, threaded=3)