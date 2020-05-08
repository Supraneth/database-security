#Securite des bases de données - MOREAU Kevin - VALLET Florian - CYBER2 - ENSIBS VANNES
#Mars 2020
#middlewareServer.py

#Imports libs
import math
from flask import Flask, json, request, jsonify, make_response
import mysql.connector, sys
from mysql.connector import errorcode
from pyope.ope import OPE
import phe.encoding
from phe import paillier
import json
import requests

#Fonctions globales

#Connexion à la bdd
def db_connexion(user,pas,host,db):
    cnx = mysql.connector.connect(user=user, password=pas, host=host,
                                database=db, autocommit=True)
    return cnx

#Fermeture de connexion à la bdd
def db_close(cnx):
    cnx.close()

#Fonction de mise à jour du salaire PHE (ajout des attributs de l'objet chiffré) d'une personne
def updatePHEsalary(nom, salairePHE):
    connec = db_connexion(db_user,db_password,db_host,db_db)
    cur = connec.cursor()
    query = "UPDATE salaire SET salairePHE=(%s) WHERE nom=(%s)"
    cur.execute(query, (salairePHE, nom))
    cur.close
    db_close(connec)

#Fonction de calcul de la somme des salairesPHE entre deux personnes
def calculsomme(nom1, nom2):
    connec = db_connexion(db_user,db_password,db_host,db_db)
    cur = connec.cursor()
    query = "SELECT salairePHE FROM salaire WHERE nom=(%s) OR nom=(%s)"
    cur.execute(query, (nom1, nom2))

    somme = 0
    for salairePHE in cur:
        #Chargement des attributs dans une variables
        recuperationPHE = json.loads(salairePHE[0])
        #Recuperation de la clé publique contenue
        n = recuperationPHE['public_key']
        public_key = paillier.PaillierPublicKey(n=int(n))
        #Regénération de l'objet chiffré
        valeurSalaire = paillier.EncryptedNumber(public_key, int(recuperationPHE['ciphertext']), int(recuperationPHE['exponent']))
        #Somme des salaires
        somme += valeurSalaire  
    cur.close
    db_close(connec)

    #Sérialisation de la somme
    serieSomme = {
        'public_key': public_key.n,
        'ciphertext': str(somme.ciphertext()),
        'exponent': somme.exponent
    }

    return serieSomme


#Définition des variables globales
db_user = 'neth'
db_password = 'neth'
db_host = 'db'
db_db = 'TP2020_MORVAL'
app = Flask(__name__)

#Page servant à la réponse du serveur au client pour la somme
@app.route("/sumGET", methods=['GET', 'POST'])
def hello():
    return "Hello World, you can GET me if you want...oops!"

#Page servant à l'ajout du salairePHE à la base de données
@app.route('/encrypted', methods=['POST'])
def transfertEncryptedNumber():
    print(request.is_json)
    data= request.get_json()
    print(data)
    receivedEncrypted = data.get('salairePHE')
    print(receivedEncrypted)
    updatePHEsalary(data.get('nom'), receivedEncrypted)
    return "JSON received & PHE updated"

#Page servant au calcul de la somme
@app.route('/sumPost', methods=['GET', 'POST'])
def traitementSomme():
    #Récupération du contenu posté par le client
    data= request.get_json()
    nom1 = data.get('nom1')
    nom2 = data.get('nom2')
    #Calcul de la somme
    seriesomme = calculsomme(nom1,nom2)
    return seriesomme

#Listener constant
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)

