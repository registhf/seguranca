from Crypto.PublicKey import RSA
from Crypto import Random
import binascii
import base64
from hashlib import sha256
import sys

argc = len(sys.argv)
if argc != 4 or (sys.argv[1] != 'generate' and sys.argv[1] != 'check'):
	print('Use: python3 certificado.py generate|check file cert')
	exit(0)

file = open(sys.argv[2]).read()
hsh = sha256(file.encode('utf-8')).hexdigest()

if sys.argv[1] == 'generate':
	random = Random.new().read
	key = RSA.generate(2048, random)
	public_key = key.publickey()

	c = open(sys.argv[3], 'w+')

	c.write('-----BEGIN SHA-256-----\n' + hsh + '\n-----END SHA-256-----\n')

	enc = binascii.hexlify(public_key.encrypt(hsh.encode('utf-8'), 32)[0]).decode('utf-8')
	c.write('-----BEGIN RSA SHA-256-----\n' + enc + '\n-----END RSA SHA-256-----\n')

	c.write(public_key.exportKey().decode('utf-8'))

	c.close()
	print('Chave gerada no arquivo: ' + sys.argv[3])
elif sys.argv[1] == 'check':
	c = open(sys.argv[3]).read()
	c_hsh = c.split('-----BEGIN SHA-256-----\n')[1].split('\n-----END SHA-256-----\n')[0]
	c_rsahsh = c.split('-----BEGIN RSA SHA-256-----\n')[1].split('\n-----END RSA SHA-256-----\n')[0]
	pkey = '-----BEGIN PUBLIC KEY-----\n' + c.split('-----BEGIN PUBLIC KEY-----\n')[1]
	pkey = RSA.importKey(pkey)
	c_enc = binascii.hexlify(pkey.encrypt(hsh.encode('utf-8'), 32)[0]).decode('utf-8')

	if c_hsh != hsh:
		print('Falha na verificação do hash.')
		print(c_hsh)
		print(hsh)
		exit(0)
	elif c_enc != c_rsahsh:
		print('Falha na verificação do hash encriptado.')
		print(c_enc)
		print(c_rsahsh)
		exit(0)
	else:
		print('Ok')

