# -*- coding: utf-8 -*-

import socket, sys, time
import gene_export_003_png_melt as export

def init():

    connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connexion_principale.bind(('192.168.0.201', 12800))
    except socket.error:
        print("La liaison du socket a l'adresse choisie a Echoue.")
        sys.exit()
        
    while 1:
        print("Serveur pret, en attente de requetes ...")
        connexion_principale.listen(5)
        connexion, adresse = connexion_principale.accept()
        print("Client connecte, adresse IP %s, port %s" % (adresse[0], adresse[1]))
    
        msgClient = connexion.recv(1024)
        
        msgClientB = ""
        print(msgClient + "\n")
        export.nouveauGenerique(msgClient)
        connexion.send("OK")
        msgClient = connexion.recv(1024)
        connexion.send("OK")
        while msgClient != "":
            msgClientB += msgClient
            msgClient = connexion.recv(1024)
        
        export.creerGenerique(msgClientB)
        print("******** export terminé ************")
        connexion.send("termine")
            
init()
    
