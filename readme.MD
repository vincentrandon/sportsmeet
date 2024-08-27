# Gestionnaire de Matchs Sportifs

## Description
Bienvenue sur cette application de gestion de présences de joueurs à des rencontres sportives !

Ce projet est né d'un besoin concret : simplifier la tâche souvent fastidieuse de gestion des équipes sportives, des matchs et surtout des présences des joueurs. Face aux défis récurrents tels que l'envoi de multiples messages pour confirmer les présences ou la gestion de feuilles de calcul complexes, nous avons décidé de créer une solution centralisée et efficace.

Cette application web Django est conçue pour rationaliser l'organisation sportive. Elle permet de gérer facilement les équipes, de planifier les matchs et de suivre les présences des joueurs, le tout dans une interface intuitive et réactive. Notre objectif est de libérer les organisateurs des tâches administratives répétitives pour qu'ils puissent se concentrer sur ce qui compte vraiment : le sport et l'esprit d'équipe.

## Technologies Utilisées
- Django 5.0
- HTMX
- AlpineJS
- Tailwind CSS
- SQLite (base de données par défaut)

## Configuration

### Variables d'Environnement
Avant de lancer l'application, assurez-vous de configurer les variables d'environnement suivantes :

- `SECRET_KEY`: Clé secrète Django (générez-en une nouvelle pour la production)
- `DEBUG`: Réglez sur `False` en production
- `ALLOWED_HOSTS`: Liste des hôtes autorisés en production
- `DATABASE_URL`: URL de connexion à la base de données (si différente de SQLite)
- `EMAIL_HOST`: Serveur SMTP pour l'envoi d'emails
- `EMAIL_PORT`: Port du serveur SMTP
- `EMAIL_HOST_USER`: Nom d'utilisateur SMTP
- `EMAIL_HOST_PASSWORD`: Mot de passe SMTP
- `DEFAULT_FROM_EMAIL`: Adresse email par défaut pour l'envoi

### Installation
1. Clonez le dépôt :
   ```
   git clone [URL_DU_REPO]
   cd [NOM_DU_PROJET]
   ```

2. Créez un environnement virtuel et activez-le :
   ```
   python -m venv venv
   source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
   ```

3. Installez les dépendances :
   ```
   pip install -r requirements.txt
   ```

4. Appliquez les migrations :
   ```
   python manage.py migrate
   ```

5. Créez un superutilisateur :
   ```
   python manage.py createsuperuser
   ```

6. Lancez le serveur de développement :
   ```
   python manage.py runserver
   ```

### Importation des Joueurs

L'application offre une commande personnalisée pour importer facilement des joueurs à partir d'un fichier CSV.

#### Format du fichier CSV

Votre fichier CSV doit être structuré comme suit :

```
nom,numero_licence
John Doe,12345
Jane Smith,67890
```

Assurez-vous que le fichier est encodé en UTF-8 et que les colonnes sont séparées par des virgules.

#### Utilisation de la commande d'importation

Pour importer des joueurs à partir de votre fichier CSV, utilisez la commande suivante :

```
python manage.py import_players chemin/vers/votre/fichier.csv
```

Par exemple, si votre fichier CSV se nomme `joueurs.csv` et se trouve dans le même répertoire que `manage.py`, vous exécuterez :

```
python manage.py import_players joueurs.csv
```

Cette commande lira le fichier CSV et créera ou mettra à jour les joueurs dans la base de données. Elle affichera des messages indiquant le succès ou l'échec de l'importation pour chaque joueur.

Remarque : Si un joueur avec le même numéro de licence existe déjà, ses informations seront mises à jour avec les nouvelles données du CSV.

## Déploiement en Production

Pour déployer l'application en production :

1. Configurez les variables d'environnement mentionnées ci-dessus.
2. Utilisez un serveur WSGI comme Gunicorn.
3. Configurez un serveur web (Nginx ou Apache) comme proxy inverse.
4. Utilisez une base de données plus robuste comme PostgreSQL.
5. Configurez les fichiers statiques avec `python manage.py collectstatic`.
6. Assurez-vous que `DEBUG = False` dans les paramètres de production.

Exemple de commande pour lancer avec Gunicorn :
```
gunicorn config.wsgi:application
```

## Améliorations Futures

Cette première version pose les bases de l'application. Pour les versions futures, nous prévoyons :

1. Ajout de tests unitaires et d'intégration.
2. Amélioration du système d'authentification et de gestion des utilisateurs.
3. Mise en place d'un système de rappels automatiques par email pour les matchs à venir.
4. Optimisation des performances et de la scalabilité.
5. Ajout de fonctionnalités de reporting et d'analyse de données.

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Automatisation sur Mesure

Vous recherchez des solutions d'automatisation plus avancées pour votre organisation sportive ? Nous pouvons vous aider à personnaliser et à étendre les fonctionnalités de cette application selon vos besoins spécifiques.

Pour des solutions d'automatisation sur mesure, contactez-nous à hello@keerok.tech ou visitez notre site [keerok.tech](). Notre équipe est prête à transformer votre gestion d'équipe en un processus fluide et efficace.
