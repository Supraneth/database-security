Guide de déploiement de l'environnement

Prérequis : Docker

____



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

    - root@{ID-Container-mysql}> `mysql -u root -p < /var/lib/mysql.deploydb.sql`

      La base de données est maintenant configurée

____

Enfin, une fois l'environnement monté est opérationnel :

user@{yours} > `python3 middlewareClient.py`

Enjoy !

PS : La base de données est fournie avec des utilisateurs pré-construits disposant d'un salaire chiffré (PHE + ORE), libre à vous de les modifier et de jouer avec grâce aux différentes options fournies par le programme.



Kévin MOREAU



