#include:utf-8
"""
Author : Horairy Hakim
Email : hakim.horairy@telecom-sudparis.eu
Tel : 07 69 22 52 55
"""
import socket
import hashlib
import pickle
import os


def CesarCiffer(word, key):
	alphabets = {alphabet : index for index, alphabet in enumerate("0123456789abcdef")}

	cipheredWord = ""

	for carac in word:
		if alphabets[carac] + key < len("0123456789abcdef") and alphabets[carac] + key >= 0:
			cipheredWord += "0123456789abcdef"[alphabets[carac] + key]
		elif alphabets[carac] + key >= len("0123456789abcdef") or alphabets[carac] + key < 0 :
			cipheredWord += "0123456789abcdef"[(alphabets[carac] + key)%len("0123456789abcdef")]

	return cipheredWord


def InverseCesarCiffer(cipheredWord, key):
	return CesarCiffer(cipheredWord, -key)


def SHA256(filePath):

	with open(filePath,"rb") as file:
		binaryFile = file.read()# read entire file as byte
		readable_hash = hashlib.sha256(binaryFile).hexdigest();
	
	return readable_hash



def hashingProtectedFiles():
	
	pathProtectedFiles = ["./protectedFiles/{0}".format(protectedFile) for protectedFile in os.listdir("./protectedFiles")]
	mapOfHashedProtectedFiles = {pathProtectedFile:SHA256(pathProtectedFile) for pathProtectedFile in pathProtectedFiles}

	return mapOfHashedProtectedFiles

def cryptingOfCryptedFilesHash(mapOfHashedProtectedFiles):

	cryptedMapOfHashedProtectedFiles = {pathProtectedFile: CesarCiffer(hashDigest, key=5) for pathProtectedFile, hashDigest in mapOfHashedProtectedFiles.items()} 

	return cryptedMapOfHashedProtectedFiles


def saveStateOfProtectedFiles(pathStateOfProtectedFiles="./StateOfProtectedFiles"):
	
	mapOfHashedProtectedFiles = hashingProtectedFiles()
	cryptedMapOfHashedProtectedFiles = cryptingOfCryptedFilesHash(mapOfHashedProtectedFiles)
	
	with open(pathStateOfProtectedFiles, 'wb') as bFile:
		myPickler = pickle.Pickler(bFile)
		myPickler.dump(cryptedMapOfHashedProtectedFiles)
		 
	return None

def loadStateOfProtectedFiles(pathStateOfProtectedFiles="./StateOfProtectedFiles"):
	
	with open(pathStateOfProtectedFiles, 'rb') as bFile:
		myDepickler = pickle.Unpickler(bFile)
		cryptedMapOfHashedProtectedFiles = myDepickler.load()

	return cryptedMapOfHashedProtectedFiles

###############################################################################################
###############################################################################################

def StartServerTest():
	hote = ""
	port = 12800
	cryptedMapOfHashedProtectedFiles = loadStateOfProtectedFiles()

	print("Ci-joint les valeurs chiffrée de Hash des fichiers protégés :\n")

	for index, hashedValue in enumerate(cryptedMapOfHashedProtectedFiles.values()):
		print("{0} -> {1}".format(index, hashedValue))

	print("\nLancement du service.")

	principalConnexion = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
	principalConnexion.bind((hote, port))
	principalConnexion.listen(5)
	connexionWithClient, connexionInfos = principalConnexion.accept()

	print("Le serveur écoute à présent sur le port {}".format(port))

	stopWord = b"fin"

	connexionWithClient.send(stopWord)


	receivedMessage = b""
	while receivedMessage != stopWord:
	    receivedMessage = connexionWithClient.recv(1024)  # L'instruction ci-dessous peut lever une exception si le message réceptionné comporte des accents

	    print("la valeur de hash reçu : {0}".format(receivedMessage.decode()))
	    cryptedReceivedHash = CesarCiffer(receivedMessage.decode(), key=5)
	    print("la valeur chiffrée de hash reçu : {0}".format(cryptedReceivedHash))

	    if cryptedReceivedHash in cryptedMapOfHashedProtectedFiles.values():
	    	connexionWithClient.send(b"Le fichier est bon")
	    else:
	    	connexionWithClient.send(b"Le fichier est mauvais")


	print("Fermeture connexion.")
	connexionWithClient.close()
	principalConnexion.close()
	os.system("clear")
	return None


##########################################################################################################################
##########################################################################################################################

StartServerTest()