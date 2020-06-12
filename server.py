from flask import Flask, render_template, request, make_response, redirect, url_for
from cookies_and_tokens import *
from threading import Thread
from time import time, sleep
from Crypto.Util.number import getPrime
from random import choice, randint
from gamepage import *
from cookies_and_tokens import *
import copy
from base64 import b64encode, b64decode

webService = Flask(__name__)

webState = dict()
webState['people_counter'] = 0
webState['ratio'] = 1
webState['timelock'] = 30
webState['counter_threhold'] = 50
webState['ratio_threhold'] = 2
webState['allow_time'] = 1800
webState['basic_time_lock'] = 30

serverSuperKey = arbKey('KEY{YEHA_Server_SUPER_Key!!!!!!!!!!!!!!!!!!!!!}')

def webMonitor():
	global webState

	dt = 2
	lastinTime = time()
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
			webState['timelock'] = webState['basic_time_lock']
		if webState['people_counter'] >= webState['counter_threhold']:
			webState['timelock'] += (webState['people_counter'] - webState['counter_threhold']) * 3
		if webState['ratio'] >= webState['ratio_threhold']:
			webState['timelock'] += (webState['ratio'] - webState['ratio_threhold']) * 5

		nowtime = time()
		if nowtime + webState['timelock'] <= lastinTime:
			webState['timelock'] = lastinTime - nowtime
		else:
			lastinTime = nowtime + webState['timelock']
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

	userId = arbID(s)

	if webState['timelock'] != 0:
		r = request.cookies.get('PASS_TOKEN')
		if r == 'None':
			return redirect(url_for('challenge'))
		if not verifyToken(userId, r, serverSuperKey):
			return redirect(url_for('challenge'))

	webState['people_counter'] += 1

# Service

	s = getPrime(2000)

# Service

	webState['people_counter'] -= 1
	return str(s)

@webService.route('/challenge')
def challenge():

	validDuration = webState['allow_time']
	validTime = webState['timelock']
	userId = arbID(request.cookies.get('SESSION_ID'))
	gameKey = serverSuperKey

	x = randint(0, 0)
	if x == 0:
		game, timetoken = gen_quiz_page(validDuration, validTime, userId, gameKey)
		timetoken = b64encode(timetoken)
		resp = make_response(game)
		resp.set_cookie('PASS_TOKEN', timetoken)
		return resp


if __name__ == '__main__':
	webService.run(host='0.0.0.0', port=8000, threaded=3)