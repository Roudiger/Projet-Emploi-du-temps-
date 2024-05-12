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

def main():
    # Connexion à la base de données
    conn = connect_to_database()
    if not conn:
        return

    # Menu principal
    while True:
        print("\n1. Ajouter un professeur")
        print("2. Quitter")
        choix = input("Entrez votre choix : ")
        if choix == "1":
            create_professeur(conn)
        elif choix == "2":
            break
        else:
            print("Choix invalide. Veuillez entrer 1 ou 2.")

    # Fermeture de la connexion à la base de données
    conn.close()

if __name__ == "__main__":
    main()
