# Sécurité des bases de données - Chiffrement du contenu d'une base

## Implémentation d'un chiffrement par relation d'ordre et par chiffrement homomorphique

Ce projet s'inscrit dans le cadre de ma formation à l'ENSIBS de Vannes pour le diplôme d'ingénieur en cyberdéfense.
Il traite de l'implémentation de deux moyens de chiffrement permettant la confidentialité et l'intégrité des données
stockées en base de données.

L'intégralité du projet est détaillé dans le fichier *rapportProjet.pdf* fourni.

**Bonne lecture**






# Guide de déploiement de l'environnement

## Prérequis : Docker

Environnement de test (Machine virtuelle) :

`uname -a ` : Linux debian 4.19.0-17-amd64 #1 SMP Debian 4.19.194-2 (2021-06-21) x86_64 GNU/Linux

- Dans un terminal : `docker-compose up` (vérifier si les ports d'écoute positionnés par défaut vous conviennent)

L'environnement se monte en installant les containers et leurs dépendances.

____

- Lancement du middlewareServeur.py :
  - Dans un terminal : 

    - `docker exec -it {ID-Container-Python} bash`

    - root@{ID-Container-Python}> `python middlewareServeur.py`

      Le serveur d'écoute est maintenant configuré
      

- Configuration de la base de données :

  - Dans un terminal : 

    - `docker exec -it {ID-Container-mysql} bash`

    - root@{ID-Container-mysql}> `mysql -u root -p < /var/lib/mysql/deploydb.sql`

      (Pas de mot de passe sur le compte mysql root)
      La base de données est maintenant configurée

____

Enfin, une fois l'environnement monté est opérationnel :

user@{yours} > `python3 middlewareClient.py`

Enjoy !

PS : La base de données est fournie avec des utilisateurs pré-construits disposant d'un salaire chiffré (PHE + ORE), libre à vous de les modifier et de jouer avec grâce aux différentes options fournies par le programme.
