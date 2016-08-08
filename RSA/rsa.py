from Crypto.PublicKey import RSA
from Crypto import Random
import base64

texto = 'Regis'

random = Random.new().read
key = RSA.generate(2048, random)
public_key = key.publickey()


print('Texto original: ' + texto)
enc = public_key.encrypt(texto.encode('utf-8'), 32)
print('-----\nEncriptado com a chave pública: ' + str(enc))


dec = key.decrypt(enc)
print('-----\nDescriptografado com a chave privada: ' + str(dec))