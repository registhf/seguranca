from Crypto import Random
from Crypto.Cipher import AES
import sys


key = sys.argv[1].encode('utf-8')
word = sys.argv[2].encode('utf-8')

init = Random.new().read(AES.block_size) # 16 bytes aleatorios
try:
	cipher = AES.new(key, mode=AES.MODE_CFB, IV=init)
except ValueError as e:
	print(e)
	exit(0)
msg = init + cipher.encrypt(word)
back = cipher.decrypt(msg)

print('Encrypt: ' + str(msg)[1:])
print('Decrypt: ' + str(back[AES.block_size:])[1:]) # remove o tamanho do bloco concatenado

