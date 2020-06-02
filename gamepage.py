try:
	from Cryptodome.Cipher import AES
	from Cryptodome.Hash import SHA256
except:
	from Crypto.Cipher import AES
	from Crypto.Hash import SHA256

from os import urandom
from time import time
from base64 import b64encode, b64decode

def arbKey(keystring):
	h = SHA256.new()
	h.update(bytes(keystring, 'ascii'))
	return h.digest()

def arbID(idstring):
	h = SHA256.new()
	h.update(bytes(idstring, 'ascii'))
	return h.digest()[:16]

def OTP(aToken, bToken):
	return b''.join([int.to_bytes(a^b, 1, byteorder='big') for a,b in zip(aToken, bToken)])

def generateTimeToken(useT, expET, userId, gameKey, tokenLength):
	serverTime = int(time())
	validTime = bytes(str(serverTime + expET).rjust(12, '0'), 'ascii')
	expiredTime = bytes(str(serverTime + expET + useT).rjust(12, '0'), 'ascii')
	nonce = urandom(tokenLength - 56)
	rawToken = userId + validTime + expiredTime + nonce

	aes = AES.new(gameKey, AES.MODE_GCM)
	encryptedToken = aes.encrypt(rawToken)
	theTimeToken = aes.nonce + encryptedToken
	return theTimeToken

def generatePassToken(useT, userId, gameKey, tokenLength):
	serverTime = int(time())
	validTime = bytes(str(serverTime).rjust(12, '0'), 'ascii')
	expiredTime = bytes(str(serverTime + expET + useT).rjust(12, '0'), 'ascii')
	nonce = urandom(tokenLength - 56)
	rawToken = userId + validTime + expiredTime + nonce

	aes = AES.new(gameKey, AES.MODE_GCM)
	encryptedToken = aes.encrypt(rawToken)
	thePassToken = aes.nonce + encryptedToken
	return thePassToken

def verifyToken(userId, token, gameKey):
	try:
		token = b64decode(token)
	except:
		return False

	nonce = token[:16]
	encryptedToken = token[16:]
	aes = AES.new(gameKey, nonce=nonce AES.MODE_GCM)
	try:
		recoveryToken = aes.decrypt(encryptedToken)
	except:
		return False

	t_userId = recoveryToken[:16]
	t_validTime = int(str(recoveryToken[16:28], 'ascii'))
	t_expiredTime = int(str(recoveryToken[28:40], 'ascii'))

	if userId != t_userId:
		return False

	serverTime = int(time())

	if serverTime < t_validTime:
		return False

	if serverTime > t_expiredTime:
		return False

	return True


def gen_gamepage_template(useT, expET, userId, gameKey):
	gameKey = arbKey(gameKey)
	userId = arbID(userId)

	def decide_tokenLength(expET):
		vaule = expET + 48
		return max(vaule, 60)

	tokenLength = decide_tokenLength(expET)

	timeToken = generateTimeToken(useT, expET, userId, gameKey, tokenLength)
	passToken = generatePassToken(useT, expET, userId, gameKey, tokenLength)
	probToken = urandom(tokenLength)

	print(passToken)
	print(probToken)

	xxxxToken = OTP(passToken, probToken)
	recoToken = OTP(xxxxToken, probToken)

	print(recoToken)



if __name__ == '__main__':
	gen_gamepage_template(600, 30, 'abcdef', 'bbb')