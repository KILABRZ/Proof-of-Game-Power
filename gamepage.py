from cookies_and_tokens import *
from random import randint, shuffle

def gen_gamepage_template(useT, expET, userId, gameKey):
	gameKey = arbKey(gameKey)
	userId = arbID(userId)

	def decide_tokenLength(expET):
		vaule = expET + 48
		return max(vaule, 60)

	tokenLength = decide_tokenLength(expET)

	timeToken, passToken = generateToken(useT, expET, userId, gameKey, tokenLength)
	probToken = urandom(tokenLength)

	print(passToken)

	xxxxToken = OTP(passToken, probToken)
	recoToken = OTP(xxxxToken, probToken)

	print(recoToken)

	presToken = b64encode(passToken)

	print(verifyToken(userId, presToken, gameKey))



def gen_quiz_page(validDuration, validTime, userId, gameKey):
	problemCount = min(validTime // 10 + 1, 10)
	problems = open('./resource/quiz/problems.txt', 'r').read().split('\n')[:-1]
	shuffle(problems)
	problems = problems[:problemCount]

	probToken = b''

	for problem in problems:
		p, a = problem.split(';')
		probToken = probToken + bytes(a, 'ascii')

	tokenLength = max(len(probToken), 60)
	timeToken, passToken = generateToken(validDuration, validTime, userId, gameKey, tokenLength)
	if len(probToken) < 60:
		probToken = probToken + b'\x00' * len(passToken[len(probToken):])
	

	xxxxToken = OTP(passToken, probToken)

	htmlheader = '<html><title> Speed Quiz {} !!!</title><body>'.format(problemCount)

	script = '<h1 style="text-align: center; font-size: 80px; margin-bottom: 30px;"> Finish Quiz !!!</h1>'
	for i, problem in enumerate(problems):
		p, a = problem.split(';')
		script += '<div style="display: flex; justify-content: center; align-items: center; height: 8vh; width: 100%; margin-bottom: 15px;">'
		script += '<div style="display: inline-block; font-size: 40px; margin-right: 30px;"> {} </div>'.format(p)
		script += '<div style="display: inline-block; width: 10%; "><input id="{}" style="font-size: 40px;border :2px black solid; width: 100%;" type="text"> </input> </div>'.format(i)
		script += '</div>'

	script += '<div style="display: flex; justify-content: center; align-items: center; height: 8vh; width: 100%; margin-bottom: 15px;">'
	script += '<div style="display: inline-block; width: 10%; "> <button id="submit_button" style="font-size: 40px;"> Submit </button> </div>'
	script += '</div>'
	script += '<h1 style="text-align: center; font-size: 20px; margin-bottom: 12px;"> or pass after <b id = "supernumber"> X </b> seconds. </h1>'
	

	script += '<script>'
	script += 'var initialWT = {};'.format(validTime+3)
	script += 'var s = function(){ if(initialWT <= 0) { initialWT = 0; return 0;} initialWT--; document.getElementById("supernumber").innerHTML = initialWT; if(initialWT <= 0) { window.location = window.location.origin + "/service"; } };'
	script += 'window.setInterval(s, 1000);'
	script += 'var xxxxToken = "{}";'.format(str(b64encode(xxxxToken), 'ascii'))
	script += 'var recoToken = "";'
	script += 'var ssssToken = "";'
	script += 'var totalProblems = {};'.format(problemCount)
	script += 'var e = function(){for(var i=0;i<totalProblems;i++){var s = document.getElementById(i).value.toString(); recoToken += s;}'
	script += 'xxxxToken = atob(xxxxToken);'
	script += 'for(var i=0;i<recoToken.length;i++){ssssToken += String.fromCharCode(xxxxToken[i].charCodeAt(0) ^ recoToken[i].charCodeAt(0));}'
	script += 'xxxxToken = ssssToken + xxxxToken.substr(recoToken.length);'
	script += 'document.cookie = document.cookie.split(";")[0] + "; PASS_TOKEN=" + btoa(xxxxToken);'
	script += 'window.location = window.location.origin + "/service"; };'
	script += 'document.getElementById("submit_button").addEventListener("click", e);'

	script += '</script>'
	htmltailer = '</body></html>'

	js = htmlheader + script + htmltailer
	print(js)

	return js, timeToken



if __name__ == '__main__':
	gen_gamepage_template(600, 30, 'abcdef', 'bbb')