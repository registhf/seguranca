from bottle import run, get, post, request
import requests
import threading
from time import sleep
from sys import argv


alice = 0
ai = 0
bob = 0
bi = 0
primo = 2147483647
base = 17 


if len(argv) < 3:
	print('Inicie com {alice|bob} {chave}')
	exit(0)


print('-------------------------------------')
if argv[1] == 'alice':
	alice = int(argv[2])
	ai = ((base ** alice) % primo)
	print('Alice, chave privada: ' + str(alice) + ', chave intermediária: ' + str(ai))
elif argv[1] == 'bob':
	bob = int(argv[2])
	bi = ((base ** bob) % primo)
	print('Bob, chave privada: ' + str(bob) + ', chave intermediária: ' + str(bi))
else:
	print('Parâmetros inválidos')
	exit(0)


def trocachave():
	global alice, bob, base, primo
	while True:
		try:
			if argv[1] == 'alice':
				requests.post('http://localhost:8001/chave', {'chave': ai})
			elif argv[1] == 'bob':
				requests.post('http://localhost:8000/chave', {'chave': bi})
			return True
		except Exception as e:
			sleep(1/5)


@post('/chave')
def recebechave():
	global alice, bob
	chave = int(request.forms.get('chave'))
	print('Chave recebida: ' + str(chave))
	if argv[1] == 'alice':
		bob = chave
		print('Resultado: ' + str((bob ** alice) % primo))
	elif argv[1] == 'bob':
		alice = chave
		print('Resultado: ' + str((alice ** bob) % primo))


tr = threading.Thread(None, trocachave, (), {}, None)
tr.start()

run(host='localhost', port=8000 if argv[1] == 'alice' else 8001, quiet=True)