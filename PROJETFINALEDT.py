from datetime import timedelta
import mysql.connector

# Fonction pour se connecter à la base de données
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mdp",
            database="projetinfo"
        )
        print("Connexion à la base de données réussie.")
        return conn
    except mysql.connector.Error as err:
        print(f"Erreur de connexion à la base de données : {err}")
        return None

# Fonction pour créer un nouveau professeur
def create_professeur(conn):
    try:
        cursor = conn.cursor()
        nom = input("Entrez le nom du professeur : ")
        prenom = input("Entrez le prénom du professeur : ")
        cursor.execute("INSERT INTO Professeurs (Nom, Prenom) VALUES (%s, %s)", (nom, prenom))
        conn.commit()
        print("Professeur ajouté avec succès.")
        # Récupérer l'ID du nouveau professeur
        cursor.execute("SELECT ID_Professeur FROM Professeurs WHERE Nom = %s AND Prenom = %s", (nom, prenom))
        professeur_id = cursor.fetchone()[0]
        # Ajouter les disponibilités par défaut
        add_default_availability(conn, professeur_id)
        # Proposer la gestion des disponibilités
        manage_availability(conn, professeur_id)
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'ajout du professeur : {err}")

# Fonction pour ajouter les disponibilités par défaut d'un professeur
def add_default_availability(conn, professeur_id):
    try:
        cursor = conn.cursor()
        jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
        heures = sorted([timedelta(hours=i) for i in range(8, 21)])  # De 8h à 20h

        for jour in jours:
            for heure_debut in heures:
                cursor.execute("INSERT INTO Disponibilites (ID_Professeur, JourSemaine, HeureDebut, HeureFin) VALUES (%s, %s, %s, %s)", (professeur_id, jour, heure_debut, heure_debut + timedelta(hours=1)))
            conn.commit()

        print("Disponibilités par défaut ajoutées pour le professeur.")
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'ajout des disponibilités par défaut : {err}")

# Fonction pour gérer la suppression de disponibilités
def manage_availability(conn, professeur_id):
    try:
        cursor = conn.cursor()
        jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
        heures = sorted([timedelta(hours=i) for i in range(8, 21)])  # De 8h à 20h

        for jour in jours:
            print(jour + " :")
            for i, heure_debut in enumerate(heures):
                print(f"{i + 1}. {str(heure_debut).split(' ')[-1]}")
            print("Voulez-vous supprimer une disponibilité pour ce jour ? (O/N)")
            choix = input()
            while choix.upper() == "O":
                num_heure = int(input("Entrez le numéro de l'heure de disponibilité à supprimer (1-13) : "))
                if 1 <= num_heure <= 13:
                    heure_a_supprimer = heures[num_heure - 1]
                    cursor.execute("DELETE FROM Disponibilites WHERE ID_Professeur = %s AND JourSemaine = %s AND HeureDebut = %s", (professeur_id, jour, heure_a_supprimer))
                    conn.commit()
                    print(f"L'heure {heure_a_supprimer} pour le {jour} a été supprimée.")
                else:
                    print("Veuillez entrer un numéro valide (entre 1 et 13).")
                print("Voulez-vous supprimer une autre disponibilité ? (O/N)")
                choix = input()
    except mysql.connector.Error as err:
        print(f"Erreur lors de la gestion des disponibilités : {err}")

# Fonction pour récupérer la liste des professeurs depuis la base de données
def get_professeurs(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT ID_Professeur, CONCAT(Nom, ' ', Prenom) FROM Professeurs")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Erreur lors de la récupération des professeurs : {err}")
        return []

# Fonction pour afficher la liste des professeurs et demander à l'utilisateur de choisir
def choose_professeur(professeurs):
    print("Liste des professeurs :")
    for prof in professeurs:
        print(f"{prof[0]}. {prof[1]}")
    id_professeur = int(input("Entrez le numéro du professeur en charge de cette matière : "))
    return id_professeur

# Fonction pour créer une nouvelle matière
def create_matiere(conn):
    try:
        cursor = conn.cursor()
        nom_matiere = input("Entrez le nom de la matière : ")
        professeurs = get_professeurs(conn)
        id_professeur = choose_professeur(professeurs)
        nb_cours = int(input("Entrez le nombre de cours pour cette matière : "))
        duree = input("Entrez la durée des cours pour cette matière (HH:MM) : ")
        cursor.execute("INSERT INTO Matieres (Nom, ID_Professeur, Nb_Cours, Duree) VALUES (%s, %s, %s, %s)", (nom_matiere, id_professeur, nb_cours, duree))
        conn.commit()
        print("Matière ajoutée avec succès.")
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'ajout de la matière : {err}")

# Fonction pour créer une nouvelle salle
def create_salle(conn):
    try:
        cursor = conn.cursor()
        nombre_salles = int(input("Entrez le nombre de salles à créer : "))
        capacite_commune = int(input("Entrez la capacité commune pour toutes les salles : "))
        for i in range(nombre_salles):
            nom_salle = input(f"Entrez le nom de la salle {i+1} : ")
            cursor.execute("INSERT INTO Salles (Nom, Capacite) VALUES (%s, %s)", (nom_salle, capacite_commune))
        conn.commit()
        print("Salles ajoutées avec succès.")

        # Saisie des disponibilités pour chaque salle
        for i in range(nombre_salles):
            print(f"--- Salle {i+1} ---")
            add_availability(conn, f"Salle {i+1}")

    except mysql.connector.Error as err:
        print(f"Erreur lors de l'ajout des salles : {err}")

# Fonction pour ajouter les disponibilités pour une salle donnée
def add_availability(conn, salle):
    jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']
    heures = [(i, i+1) for i in range(8, 20)]  # De 8h à 20h
    try:
        cursor = conn.cursor()
        for jour in jours:
            print(f"Disponibilités pour {jour} :")
            print("1. Prendre toutes les disponibilités")
            for i, heure_debut in enumerate(heures):
                print(f"{i + 2}. {heure_debut[0]}h-{heure_debut[1]}h")
            choix = input("Entrez le numéro de l'heure de disponibilité (ou 'stop' pour arrêter) : ")
            if choix.lower() == 'stop':
                break
            if choix.isdigit():
                indice = int(choix) - 2
                if indice == -1:
                    for heure_disponible in heures:
                        cursor.execute("INSERT INTO Disponibilites_salle (ID_Salle, JourSemaine, HeureDebut, HeureFin) VALUES ((SELECT ID_Salle FROM Salles WHERE Nom = %s), %s, TIME_FORMAT(%s, '%H:%i:%s'), TIME_FORMAT(%s, '%H:%i:%s'))", (salle, jour, heure_disponible[0], heure_disponible[1], heure_disponible[0], heure_disponible[1]))
                else:
                    heure_disponible = heures[indice]
                    cursor.execute("INSERT INTO Disponibilites_salle (ID_Salle, JourSemaine, HeureDebut, HeureFin) VALUES ((SELECT ID_Salle FROM Salles WHERE Nom = %s), %s, TIME_FORMAT(%s, '%H:%i:%s'), TIME_FORMAT(%s, '%H:%i:%s'))", (salle, jour, heure_debut[0], heure_debut[1], heure_debut[0], heure_debut[1]))
        conn.commit()
        print(f"Disponibilités pour la salle {salle} ajoutées avec succès.")
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'ajout des disponibilités pour la salle {salle} : {err}")

def main():
    # Connexion à la base de données
    conn = connect_to_database()
    if not conn:
        return

    # Menu principal
    while True:
        print("\nMenu Principal :")
        print("1. Ajouter un professeur")
        print("2. Ajouter une matière")
        print("3. Ajouter une salle")
        print("4. Quitter")
        choix = input("Entrez votre choix : ")
        if choix == "1":
            create_professeur(conn)
        elif choix == "2":
            create_matiere(conn)
        elif choix == "3":
            create_salle(conn)
        elif choix == "4":
            break
        else:
            print("Choix invalide. Veuillez entrer un numéro valide.")

    # Fermeture de la connexion à la base de données
    conn.close()

if __name__ == "__main__":
    main()
