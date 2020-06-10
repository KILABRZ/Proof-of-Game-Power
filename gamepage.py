from cookies_and_tokens import *

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



if __name__ == '__main__':
	gen_gamepage_template(600, 30, 'abcdef', 'bbb')