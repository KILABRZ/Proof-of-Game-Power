from flask import Flask, render_template, request, make_response
from cookies_and_tokens import *

webService = Flask(__name__)

@webService.route('/')
def index():
	resp = make_response(render_template('index.html'))
	
	s = request.cookies.get('SESSION_ID')
	if s == None:
		resp.set_cookie('user', expire=0)
		resp.set_cookie('SESSION_ID', expire=0)
		resp.set_cookie('PASSING_TOKEN', expire=0)
		s = generateSessionId()
		resp.set_cookie('SESSION_ID', s)


	return resp

@webService.route('/service')
def importantService():
	

if __name__ == '__main__':
	webService.run(host='0.0.0.0', port=8000, threaded=3)