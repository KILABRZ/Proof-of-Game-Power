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
	problemCount = min(int(validTime // 10 + 1), 10)
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
	
	print('passtoken =', b64encode(passToken))
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
	script += '<h1 style="text-align: center; font-size: 20px; margin-bottom: 12px;"> or auto pass after <b id = "timecounter"> {} </b> seconds. </h1>'.format(validTime)
	

	script += '<script>'
	script += 'var initialWT = {};'.format(validTime+10)
	script += 'var s = function(){ if(initialWT <= 0) { initialWT = 0; return 0;} initialWT--; document.getElementById("timecounter").innerHTML = initialWT; if(initialWT <= 0) { window.location = window.location.origin + "/service"; } };'
	script += 'window.setInterval(s, 1000);'
	script += 'var xxxxToken = "{}";'.format(str(b64encode(xxxxToken), 'ascii'))
	script += 'var recoToken = "";'
	script += 'var ssssToken = "";'
	script += 'var totalProblems = {};'.format(problemCount)
	script += 'var e = function(){for(var i=0;i<totalProblems;i++){var s = document.getElementById(i).value.toString(); recoToken += s;}'
	script += 'xxxxToken = atob(xxxxToken);'
	script += 'for(var i=0;i<recoToken.length;i++){ssssToken += String.fromCharCode(xxxxToken[i].charCodeAt(0) ^ recoToken[i].charCodeAt(0));}'
	script += 'xxxxToken = ssssToken + xxxxToken.substr(recoToken.length);'
	script += 'window.location = window.location.origin + "/service?PASS_TOKEN="+ btoa(xxxxToken).split("+").join("*"); };'
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

def randomPuzzleRotate(puzzlePack, difficulty):

	w = (2, 4, 6, 8, 10, 12, 14, 16, 18, 20)[difficulty]
	r = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)[difficulty]
	piv = (w-1) / 2

	N = r ** 2 + 20 + randint(5, 21)

	order = [i for i in range(w*w)]
	neworder = [i for i in range(w*w)]

	ring_position = [[] for i in range(r)]
	next_position = [None for i in range(w*w)]
	prev_position = [None for i in range(w*w)]

	for i in range(w):
		for j in range(w):
			tr = int(max(abs(i - piv), abs(j - piv)))
			if j >= i and i+j < piv * 2:
				d = 0
			elif i+j >= piv*2 and j > i:
				d = 1
			elif i+j > piv*2 and i >= j:
				d = 2
			elif i+j <= piv * 2 and i >= j:
				d = 3
			di = [0, 1, 0, -1][d]
			dj = [1, 0, -1, 0][d]
			ni, nj = i+di, j+dj
			idx, nidx = i*w+j, ni*w+nj

			ring_position[tr].append(idx)
			next_position[idx] = nidx
			prev_position[nidx] = idx


	for t in range(N):
		rr = randint(0, r-1)
		for idx in ring_position[rr]:
			nidx = prev_position[idx]
			neworder[nidx] = order[idx]
		order = list(tuple(neworder))
	puzzlePack= [puzzlePack[c] for c in order]

	return puzzlePack



def gen_rotating_puzzle_page(validDuration, validTime, userId, gameKey):
	totalDifficulties = 10
	difficulty = min(int(totalDifficulties-1), int(validTime // 5))
	puzzleCount = (4, 16, 36, 64, 100, 144, 192, 256, 324, 400)[difficulty]

	problemList = open('./static/rotating_puzzle/problemlist.txt', 'r').read().split('\n')[:-1]
	problemList = [c.split(',') for c in problemList]
	problemsGroup = [[] for _ in range(totalDifficulties)]
	for p in problemList:
		problemsGroup[int(p[1])].append(p[0])

	problemPath = './static/rotating_puzzle/{}'.format(choice(problemsGroup[difficulty]))
	imgPathes = open('{}/problem_description.txt'.format(problemPath), 'r').read().split(';')[:-1]
	imgPathes = ['{}/{}'.format(problemPath, c) for c in imgPathes]
	tokenLength = max(3 * puzzleCount, 60)
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
