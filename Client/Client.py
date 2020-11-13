#include:utf-8
"""
Author : Horairy Hakim
Email : hakim.horairy@telecom-sudparis.eu
Tel : 07 69 22 52 55
"""
import socket
import hashlib
import os


def SHA256(filePath):
	if filePath == "fin":
		return "fin"
	else :
		with open("./protectedFilesTest/" + filePath,"rb") as file:
			binaryFile = file.read()# read entire file as byte
			readable_hash = hashlib.sha256(binaryFile).hexdigest();

	return readable_hash

######################################################################################################
######################################################################################################


def ServiceTestClient():
	hote = "localhost"
	port = 12800

	connexionWithServer = socket.socket(family=socket.AF_INET,
	                                    type=socket.SOCK_STREAM)

	connexionWithServer.connect((hote, port))
	print("Connexion établie avec le serveur sur le port {}".format(port))

	stopWord = connexionWithServer.recv(1024)

	print(f"Pour fermer la connexion envoyer : '{stopWord.decode()}'")

	messageToBeSent = b""
	while messageToBeSent != stopWord:
	    filePath = input("Donnez le chemin du fichier à tester : ")
	    messageToBeSent = SHA256(filePath)
	    # Peut planter si vous tapez des caractères spéciaux
	    messageToBeSent = messageToBeSent.encode()
	    # On envoie le message
	    connexionWithServer.send(messageToBeSent)
	    receivedMessage = connexionWithServer.recv(1024)
	    print(receivedMessage.decode())  # Là encore, peut planter s'il y a des accents

	print("Fermeture de la connexion")

	connexionWithServer.close()
	os.system("clear")

	return None


#########################################################################################################
#########################################################################################################

ServiceTestClient()