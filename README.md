# 🩺 KidneyCare ML - Plateforme d'Aide au Diagnostic des Maladies Rénales 🌟  

*KidneyCare ML* est une solution basée sur le Machine Learning et Django, conçue pour assister les professionnels de santé dans la détection précoce des maladies rénales. En s'appuyant sur des données patients, cette plateforme offre des prédictions précises et une interface ergonomique, adaptée aux besoins des médecins et des patients.  

---

## 🔎 Contexte  

Les maladies rénales représentent une menace mondiale pour la santé publique, souvent diagnostiquées tardivement. L’objectif de *KidneyCare ML* est de fournir un outil qui analyse les données médicales, alerte sur les risques potentiels et permet aux praticiens de prendre des décisions rapides et éclairées.  

---

## 🚀 Fonctionnalités principales  

- *Prédiction des risques rénaux* : Évaluation automatique de la probabilité de maladies rénales en fonction des données cliniques.  
- *Gestion des utilisateurs* :  
  - Médecins : Visualisation des prédictions pour leurs patients.  
  - Patients : Accès à leur historique médical et recommandations.  
- *Tableau de bord dynamique* : Graphiques et analyses statistiques pour interpréter les résultats.  
- *Rapports détaillés* : Génération de documents téléchargeables pour les consultations.  

---

## 🛠️ Technologies et outils utilisés  

- *Backend* : Django - Gestion des utilisateurs et API.  
- *Frontend* : HTML, CSS, Bootstrap - Interface responsive et moderne.  
- *Machine Learning* : Algorithmes supervisés (Random Forest, SVM, ou autres).  
- *Base de données* : SQLite pour la gestion des données utilisateurs et des prédictions.  
- *Visualisation des données* : Matplotlib et Seaborn pour les graphiques.  

---

## 📋 Structure du projet  

kidneycare/  
├── db.sqlite3                 # Base de données contenant les utilisateurs et prédictions  
├── manage.py                  # Script principal pour gérer Django  
├── kidneycare/                # Répertoire principal du projet Django  
│   ├── settings.py            # Paramètres du projet  
│   ├── urls.py                # Définition des URL  
│   └── wsgi.py                # Point d'entrée pour le déploiement  
├── ml_models/                 # Modèles de Machine Learning entraînés  
├── static/                    # Fichiers CSS, JS et images  
├── templates/                 # Pages HTML pour les interfaces utilisateur  
├── reports/                   # Fichiers générés pour les médecins/patients  
└── README.md                  # Documentation du projet  

---

## ⚙️ Installation et configuration  

### Pré-requis  

- Python 3.x  
- pip (gestionnaire de paquets)  
- virtualenv  

### Étapes  

1. *Clonez le dépôt :*  
   ```bash
   git clone https://github.com/amira-1manai/KidneyCare-Machine-Learning-for-Renal-Health.git  
   cd kidneycare-ml  
   ```

2. *Créez un environnement virtuel et installez les dépendances :*  
   ```bash
   virtualenv venv  
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate  
   pip install -r requirements.txt  
   ```

3. *Appliquez les migrations pour configurer la base de données :*  
   ```bash
   python manage.py migrate  
   ```

4. *Créez un compte administrateur :*  
   ```bash
   python manage.py createsuperuser  
   ```

5. *Lancez le serveur local :*  
   ```bash
   python manage.py runserver  
   ```

6. *Accédez à l'application dans le navigateur :*  
   [http://127.0.0.1:8000](http://127.0.0.1:8000)  
