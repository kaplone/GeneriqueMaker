# -*- coding: utf-8 -*-
import socket, sys, os

conn_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try :
	conn_avec_serveur.connect(('192.168.0.201', 12800))
except socket.error :
	print("la connection a echoue")
	sys.exit()
	
msgsrv = "_ok_"

fichier = sys.argv[1]
numero = fichier.split(os.sep)[-1].split(".")[0]
conn_avec_serveur.send(numero)
e = open(fichier, "rb")
er = e.read()
print('1')
while conn_avec_serveur.recv(1024) != "OK":
    print('2')
    time.sleep(1)
print('3')
e.close()
print('4')
conn_avec_serveur.send(er)
print('5')
while conn_avec_serveur.recv(1024) == "OK":
    print('6')
    time.sleep(1)
print('7')
a = raw_input("l'export est terminé")
conn_avec_serveur.close() 
