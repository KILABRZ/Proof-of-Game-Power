from cookies_and_tokens import *
from random import randint, shuffle, choice

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

def CHUNKKKKKKKKKKKKING(s, n):
	L = len(s)
	dl = L / n
	chp = [s[int(i*dl):int((i+1)*dl)] for i in range(n)]
	return chp

def randomPuzzleRotate(puzzlePack, n):
	rotate0 = [2, 0, 3, 1]
	rotate1_0 = [0, 1, 2, 3, 4, 9, 5, 7, 8, 10, 6, 11, 12, 13, 14, 15]
	rotate1_1 = [4, 0, 1, 2, 8, 5, 6, 3, 12, 9, 10, 7, 13, 14, 15, 11]
	rotate_2_0 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 20, 14, 16, 17, 18, 19, 21, 15, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
	rotate_2_1 = [0, 1, 2, 3, 4, 5, 6, 13, 7, 8, 9, 11, 12, 19, 14, 15, 10, 17, 18, 25, 20, 21, 16, 23, 24, 26, 27, 28, 22, 29, 30, 31, 32, 33, 34, 35]
	rotate_2_2 = [6, 0, 1, 2, 3, 4, 12, 7, 8, 9, 10, 5, 18, 13, 14, 15, 16, 11, 24, 19, 20, 21, 22, 17, 30, 25, 26, 27, 28, 23, 31, 32, 33, 34, 35, 29]

	rlen = (4, 12, 20)
	rotating = [[rotate0], [rotate1_0, rotate1_1], [rotate_2_0, rotate_2_1, rotate_2_2]][n]

	for i, rotate in enumerate(rotating):
		s = randint(rlen[i]//2, rlen[i]-1)
		
		npp = [0 for j in range(len(puzzlePack))]
		for _ in range(s):
			for i, r in enumerate(rotate):
				npp[i] = puzzlePack[r]
			puzzlePack = list(tuple(npp))
	return puzzlePack


def gen_rotating_puzzle_page(validDuration, validTime, userId, gameKey):
	totalDifficulties = 3
	difficulty = min(totalDifficulties-1, validTime // 30)
	puzzleCount = (4, 16, 36)[difficulty]

	problemList = open('./static/rotating_puzzle/problemlist.txt', 'r').read().split('\n')[:-1]
	problemList = [c.split(',') for c in problemList]
	problemsGroup = [[] for _ in range(totalDifficulties)]
	for p in problemList:
		problemsGroup[int(p[1])].append(p[0])

	problemPath = './static/rotating_puzzle/{}'.format(choice(problemsGroup[difficulty]))
	imgPathes = open('{}/problem_description.txt'.format(problemPath), 'r').read().split(';')[:-1]
	imgPathes = ['{}/{}'.format(problemPath, c) for c in imgPathes]
	tokenLength = max(6 * puzzleCount, 60)
	timeToken, passToken = generateToken(validDuration, validTime, userId, gameKey, tokenLength)
	print('passtoken =', str(b64encode(passToken), 'ascii'))
	print('timetoken =', str(b64encode(timeToken), 'ascii'))
	presToken = CHUNKKKKKKKKKKKKING(str(b64encode(passToken), 'ascii'), puzzleCount)
	puzzlePack = [c for c in zip(imgPathes, presToken)]
	puzzlePack = randomPuzzleRotate(puzzlePack, difficulty)

	return difficulty, puzzlePack, timeToken



if __name__ == '__main__':
	userId = arbID('user')
	serverSuperKey = arbKey('KEY{YEHA_Server_SUPER_Key!!!!!!!!!!!!!!!!!!!!!}')
	gen_rotating_puzzle_page(10, 100, userId, serverSuperKey)

# vyGPvrWY6v0f6pTbnRb5V//WJeq794/1K0FyXF4NOKdR5o5hCXnyv3NTnnG9trHOcmylkXDMGS6T652kkqJF6LMy4ow3NHhWf/gWZrtob+WimisoalQ70TbKg0GH4SqlT6EYLFc23E94Cfjhn4277rEAAeWjgbTkDG3xvmmKf3F5DH8pSTqpbpgPuMm1iYnMLs4SJgF1h4jG9OxqQ1Uf3D+Ot+lwktTNViGKmWHbJU+IOaWhFxnGVInSavIRNIS+4o1JLaOks8Rbr96qbHhicIYfnrf5QAGU
# vyGPvrWY6v0f6pTbnRb5V//WJeq794/1K0FyXF4NOKdR5o5hCXnyv3NTnnG9trHOcmylkXDMGS6T652kkqJF6LMy4ow3NHhWf/gWZrtob+WimisoalQ70TbKg0GH4SqlT6EYLFc23E94Cfjhn4277rEAAeWjgbTkDG3xvmmKf3F5DH8pSTqpbpgPuMm1iYnMLs4SJgF1h4jG9OxqQ1Uf3D+Ot+lwktTNViGKmWHbJU+IOaWhFxnGVInSavIRNIS+4o1JLaOks8Rbr96qbHhicIYfnrf5QAGU