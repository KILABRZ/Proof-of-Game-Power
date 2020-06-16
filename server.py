from flask import Flask, render_template, request, make_response, redirect, url_for
from cookies_and_tokens import *
from threading import Thread
from time import time, sleep
from Crypto.Util.number import getPrime, inverse, GCD
from random import choice, randint
from gamepage import *
from cookies_and_tokens import *
import copy
from base64 import b64encode, b64decode

webService = Flask(__name__)

webState = dict()
webState['people_counter'] = 0
webState['ratio'] = 1
webState['timelock'] = 0
webState['counter_threhold'] = 10
webState['ratio_threhold'] = 2
webState['allow_time'] = 1800
webState['basic_time_lock'] = 500
webState['start_defense'] = True

serverSuperKey = arbKey('KEY{YEHA_Server_SUPER_Key!!!!!!!!!!!!!!!!!!!!!}')

def webMonitor():
	global webState

	dt = 1
	lastinTime = time()
	preState = copy.deepcopy(webState)
	while True:
		delta_people = webState['people_counter'] - preState['people_counter']
		webState['ratio'] = delta_people / dt
		preState = copy.deepcopy(webState)
		print('Service Capacity:', webState['counter_threhold'])
		print('Service Popularity:', webState['people_counter'])
		print('Service InRatio:', webState['ratio'])
		print('Service Now Timelock:', webState['timelock'])
		print('==============================')
		if not webState['start_defense']:
			webState['timelock'] = 0
			continue

		if webState['people_counter'] < webState['counter_threhold'] and \
			webState['ratio'] < webState['ratio_threhold']:
			webState['timelock'] = webState['basic_time_lock']
		if webState['people_counter'] >= webState['counter_threhold']:
			webState['timelock'] += ((webState['people_counter'] - webState['counter_threhold'])**1.5) 
		if webState['ratio'] >= webState['ratio_threhold']:
			webState['timelock'] += (webState['ratio'] - webState['ratio_threhold']) * 0.5

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

@webService.route('/service', methods=['GET'])
def importantService():

	s = request.cookies.get('SESSION_ID')
	if s == None:
		return redirect(url_for('index'))

	if request.args.get('PASS_TOKEN', None) is not None:
		resp = make_response(redirect(request.path))
		r = request.args.get('PASS_TOKEN').replace('*', '+')
		resp.set_cookie('PASS_TOKEN', r)
		print('pass get route')
		return resp

	userId = arbID(s)
	isGood = False
	if webState['timelock'] != 0:
		r = request.cookies.get('PASS_TOKEN')
		if r == 'None':
			return redirect(url_for('challenge'))
		if not verifyToken(userId, r, serverSuperKey):
			print('Not pass verify')
			print(r)
			return redirect(url_for('challenge'))
		else:
			print('Pass Verification !!!')

	webState['people_counter'] += 1

# Service
	p = getPrime(2048)
	q = getPrime(2048)
	N = hex(p*q)[2:]
	r = (p-1)*(q-1)
	e = 65537
	while GCD(e, r) != 1:
		e += 2
	d = inverse(e, r)
	p = hex(p)[2:]
	q = hex(q)[2:]
	d = hex(d)[2:]
# Service

	webState['people_counter'] -= 1
	return render_template('service_page.html', p=p, q=q, N=N, e=e, d=d)

@webService.route('/challenge')
def challenge():
	s = request.cookies.get('SESSION_ID')
	if s == None:
		return redirect(url_for('index'))

	validDuration = int(webState['allow_time'])
	validTime = int(webState['timelock'])
	userId = arbID(request.cookies.get('SESSION_ID'))
	gameKey = serverSuperKey

	x = randint(0, 1)
	if x == 0:
		game, timetoken = gen_quiz_page(validDuration, validTime, userId, gameKey)
		print('Quiz')
		timetoken = b64encode(timetoken)
		resp = make_response(game)
		resp.set_cookie('PASS_TOKEN', timetoken)
		return resp
	elif x == 1:
		difficulty, puzzlePack, timetoken = gen_rotating_puzzle_page(validDuration, validTime, userId, gameKey)
		timetoken = b64encode(timetoken)
		resp = make_response(render_template('rotating_puzzle.html', puzzlePack=puzzlePack, difficulty=difficulty, theTime=validTime+10))
		resp.set_cookie('PASS_TOKEN', timetoken)
		return resp

if __name__ == '__main__':
	webService.run(host='0.0.0.0', port=8000, threaded=3)