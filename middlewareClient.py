#Securite des bases de données - MOREAU Kevin - VALLET Florian - CYBER2 - ENSIBS VANNES
#Mars 2020
#middlewareClient.py

#Imports libs
import time
import mysql.connector,sys
from pyope.ope import OPE
from phe import paillier
import json
import requests
import pickle

# Définition de la fonction de connexion à la base de données
def db_connexion(user,pas,host,db):
    cnx = mysql.connector.connect(user=user, password=pas, host=host,
                                database=db)
    return cnx

# Définition de la fonction de fermeture de connexion à la base de données
def db_close(cnx):
    cnx.close()

# Définition de la fonction de génération de clé pour chiffrement OPE (relation d'ordre)
def generer_cle(key):
    return OPE(key)

# Insertion des valeurs chiffrés par OPE
def db_insert(cnx,nom,salaireORE):
    # Ecriture des requetes
    sqlSal1 = "INSERT INTO salaire(nom,salaireORE) VALUES (%s,%s)"
    valSal1 = (nom, salaireORE)

    # Creation du curseur pour etablir la connexion
    cur = cnx.cursor()
    # Execution des requetes
    cur.execute(sqlSal1,valSal1)
    cnx.commit()

def db_update(cnx,nom,salaire):
    # Ecriture des requetes
    sqlSal1 = "UPDATE salaire SET salaireORE = %s WHERE nom = %s"
    valSal1 = (salaire,nom)

    # Creation du curseur pour etablir la connexion
    cur = cnx.cursor()
    # Execution des requetes
    cur.execute(sqlSal1,valSal1)
    cnx.commit()

def db_afficher(cnx):
    cur = cnx.cursor()
    cur.execute("SELECT * FROM salaire")
    for x in cur.fetchall():
        print(x)

def db_afficher_clair(cnx,cipherORE):
    cur = cnx.cursor()
    cur.execute("SELECT * FROM salaire")
    for x in cur.fetchall():
        print ("Nom = ", x[0])
        salaireDechiffre = cipherORE.decrypt(x[1])
        print ("Salaire = ", salaireDechiffre)

def db_compare_salaire(cnx, nom1, nom2):
    #Selection des salaires chiffres en fonction des noms
    cur = cnx.cursor()
    #Salaire 1
    sql_select_query1 = """SELECT salaireORE FROM salaire WHERE nom=%s"""
    cur.execute(sql_select_query1, (nom1,))
    tupleSalairePersonne1 = cur.fetchall()[0]
    #Salaire2
    sql_select_query2 = """SELECT salaireORE FROM salaire WHERE nom=%s"""
    cur.execute(sql_select_query2, (Personne2,))
    tupleSalairePersonne2 = cur.fetchall()[0]

    #Recuperation des valeurs entieres sur le tuple
    salairePersonne1 =  tupleSalairePersonne1[0]
    salairePersonne2 =  tupleSalairePersonne2[0]
    #Comparaison :
    if salairePersonne1 > salairePersonne2:
        print("Le salaire de %s est plus eleve que celui de %s" % (Personne1, Personne2))
       
    else:
        print("Le salaire de %s est plus eleve que celui de %s" % (Personne2, Personne1))

# Fonction principale
if __name__ == '__main__':
    # Definition des variables 

    # Variable de connexion a la base
    db_user = 'neth'
    db_password = 'neth'
    db_host = '0.0.0.0'
    db_db = 'TP2020_MORVAL'

    # Generation cle de chiffrement ORE et PHE
    #Chiffrement ORE
    cipherORE = generer_cle(b'long key' * 2)
    #Chiffrement PHE
    public_key= paillier.PaillierPublicKey(2161831391)
    private_key = paillier.PaillierPrivateKey(public_key, 47147,45853)
    #Verification de la paire de clés
    print(public_key)
    print(private_key)

    #GOO
    print("Middleware v1 : Chiffrement par relation d'ordre : \n")
    ans =''
    while ans !='0':
        print ("""
        1. Afficher le contenu de la table salaire
        2. Q31 : Inserer un employe (Chiffrement ORE + PHE))
        3. Q31 : Mettre a jour le salaire d'un employe (Chiffrement ORE + PHE)
        4  Q31 : Afficher les salaires des employes en clair
        5. Q31bis : Additionner 2 salaires (Chiffrement PHE)
        6. Q31bis : Comparer deux salaires (Chiffrement ORE)
        0. Quitter
        """
        )
        ans=input("Que voulez vous faire ? (saisir le chiffre) : ")

        #Afficher le contenu de la table salaire
        if ans == "1":
            print("\nAffichage du contenu de la base de donnees")   
            #Etablissement de la connexion BDD
            connec = db_connexion(db_user,db_password,db_host,db_db)
            db_afficher(connec)
            db_close(connec)

        #Q31 : Inserer un employe (Chiffrement ORE + PHE))
        elif ans == "2":
            #Etablissement de la connexion BDD
            connec = db_connexion(db_user,db_password,db_host,db_db)
            #INPUTS user
            nom = input('Saisir le nom de l\'employe : ')
            salaire = int(input('Saisir le salaire de l\'employe : '))
            #Chiffrement ORE
            #   Insertion du salaire chiffré par ORE
            db_insert(connec,nom,cipherORE.encrypt(int(salaire)))
            #Chiffrement PHE (le salaire en clair devient un objet PHE décomposé en 3 paramètres)
            salairePHE = public_key.encrypt(salaire)
            #Decomposition de la serie composant l'objet salairePHE
            seriePHE = {'public_key': public_key.n, 'ciphertext': str(salairePHE.ciphertext()), 'exponent': salairePHE.exponent}
            #Dump de la serie pour exploitation par le serveur distant
            serializedPHE = json.dumps(seriePHE)
            #Préparation du payload
            #  Envoi vers serveur.py (nom de la personne + l'objet salaire décomposé sérialisé)
            payload = {'nom':str(nom), 'salairePHE':serializedPHE}
            #   Envoi du payload vers le serveur d'écoute
            r = requests.post("http://0.0.0.0:5000/encrypted", json=payload)
            db_close(connec)

        #Q31 : Mettre a jour le salaire d'un employe (Chiffrement ORE + PHE)
        elif ans == "3":
            #Etablissement de la connexion BDD
            connec = db_connexion(db_user,db_password,db_host,db_db)
            #INPUTS user
            nom = input('Saisir le nom de l\'employe : ')
            salaire =  int(input('Saisir le nouveau salaire de l\'employe : '))
            db_update(connec,nom,cipherORE.encrypt(int(salaire)))
            #Chiffrement PHE
            salairePHE = public_key.encrypt(salaire)
            #Decomposition de la serie composant l'objet salairePHE
            seriePHE = {'public_key': public_key.n, 'ciphertext': str(salairePHE.ciphertext()), 'exponent': salairePHE.exponent}
            #Dump de la serie pour exploitation par le serveur distant
            serializedPHE = json.dumps(seriePHE)
            #Préparation du payload
            #  Envoi vers serveur.py (nom de la personne + l'objet salaire décomposé sérialisé)
            payload = {'nom':str(nom), 'salairePHE':serializedPHE}
            #   Envoi du payload vers le serveur d'écoute
            r = requests.post("http://0.0.0.0:5000/encrypted", json=payload)
            db_close(connec)

        #Q31 : Afficher les salaires des employes en clair
        elif ans == "4":
            connec = db_connexion(db_user,db_password,db_host,db_db)
            db_afficher_clair(connec,cipherORE)
            db_close(connec)
        #Q31bis : Additionner 2 salaires (Chiffrement PHE)
        elif ans == "5":
            #Ok hardpart, there we go
            #Etablissement de la connexion BDD
            connec = db_connexion(db_user,db_password,db_host,db_db)
            #INPUTS user
            nom1 = input('Saisir le nom de l\'employe 1 : ')
            nom2 = input('Saisir le nom de l\'employe 2 : ')
            #Generation du payload + envoi vers le serveur distant
            payload = {'nom1':str(nom1), 'nom2':str(nom2)}
            r = requests.post("http://0.0.0.0:5000/sumPost", json=payload)
            #Sleeping time
            time.sleep(2)
            #Récupération de la réponse donnée par le serveur
            r = requests.get("http://0.0.0.0:5000/sumPost", json=payload).json()
            #Reconstitution et Déchiffrement du message
            cipherSomme = int(r.get('ciphertext'))
            exponentSomme = int(r.get('exponent'))
            #Regeneration de l'objet
            encryptedSommeObject = paillier.EncryptedNumber(public_key,cipherSomme,exponentSomme)
            #Dechiffrement de la somme
            encryptedSommeCipher = private_key.decrypt(encryptedSommeObject)
            #Affichage de la somme
            print("La somme des deux salaires est : ",encryptedSommeCipher)

        #Q31bis : Comparer deux salaires (Chiffrement ORE)
        elif ans == "6":
            #Input utilisateur sur les noms des personnes a comparer
            Personne1 = input("Saisissez le nom de la premiere personne : ")
            Personne2 = input("Saisissez le nom de la deuxieme personne : ")
            connec = db_connexion(db_user,db_password,db_host,db_db)
            resultCompare = db_compare_salaire(connec, Personne1, Personne2)

        #Goodbye my friend
        else:
              print("\n Goodbye...")
              break

