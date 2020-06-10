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
	problemCount = min(validTime // 4 + 1, 10)
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
		probToken = probToken + passToken[len(probToken):]
	

	xxxxToken = OTP(passToken, probToken)

	htmlheader = '<html><title> Speed Quiz {} !!!</title><body>\
	<canvas id=\"canvas\" height=\"924\" width=\"1920\"><script>'.format(problemCount)
	
	script  = 'var canvas = document.getElementById(\"canvas\").getContext(\"2d\");'
	script += 'var height = window.innerHeight, width = window.innerWidth;'
	script += 'canvas.fillStyle = \'#000\';'
	textSize = 40
	linespace = 10
	script += 'canvas.font = \'{}px Arial\';'.format(textSize)
	for i, problem in enumerate(problems):
		p, a = problem.split(';')
		script += 'canvas.fillText(\"{}\", 0, {})'.format(p, (i+1) * textSize + i * linespace)

	htmltailer = '</script></body></html>'

	js = htmlheader + script + htmltailer
	print(js)

	return js, timeToken



if __name__ == '__main__':
	gen_gamepage_template(600, 30, 'abcdef', 'bbb')