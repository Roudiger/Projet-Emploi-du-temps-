import mysql.connector
import re

# Fonction pour se connecter à la base de données
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Utopie39*",
            database="projetinfo"
        )
        print("Connexion à la base de données réussie.")
        return conn
    except mysql.connector.Error as err:
        print(f"Erreur de connexion à la base de données : {err}")
        return None

# Fonction pour récupérer les matières depuis la base de données
def get_matieres(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT ID_Matiere, Nom FROM Matieres")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Erreur lors de la récupération des matières : {err}")
        return []

# Fonction pour récupérer les disponibilités des professeurs pour une matière donnée
def get_professor_availability(conn, id_matiere):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.ID_Professeur, d.JourSemaine, d.HeureDebut, d.HeureFin
            FROM Professeurs p
            JOIN Disponibilites d ON p.ID_Professeur = d.ID_Professeur
            WHERE d.ID_Professeur IN (SELECT ID_Professeur FROM Matieres WHERE ID_Matiere = %s)
        """, (id_matiere,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Erreur lors de la récupération des disponibilités des professeurs : {err}")
        return []

# Fonction pour récupérer les disponibilités des salles
def get_room_availability(conn, capacite_requise):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ID_Salle, JourSemaine, HeureDebut, HeureFin
            FROM Disponibilites_salle
            WHERE Capacite >= %s
        """, (capacite_requise,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Erreur lors de la récupération des disponibilités des salles : {err}")
        return []

# Fonction pour valider le format de l'heure
def validate_time_format(time_str):
    if re.match(r'^\d{2}:\d{2}$', time_str):
        return True
    return False

# Fonction pour trouver un créneau disponible pour le cours
def find_available_slot(professor_availability, room_availability, duree_cours):
    for prof_availability in professor_availability:
        for room_availability in room_availability:
            if prof_availability[1] == room_availability[1]:  # Même jour
                start_time = max(prof_availability[2], room_availability[2])
                end_time = min(prof_availability[3], room_availability[3])
                if end_time - start_time >= duree_cours:
                    return prof_availability[1], start_time, start_time + duree_cours
    return None, None, None

# Fonction pour planifier un cours pour une matière donnée
def schedule_course(conn, id_matiere, id_salle, jour, heure_debut, heure_fin):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Cours_Etudiants (ID_Professeur, ID_Matiere, ID_Salle, JourSemaine, HeureDebut, HeureFin)
            VALUES (
                (SELECT ID_Professeur FROM Matieres WHERE ID_Matiere = %s),
                %s, %s, %s, %s, %s
            )
        """, (id_matiere, id_matiere, id_salle, jour, heure_debut, heure_fin))
        conn.commit()
        print("Cours planifié avec succès.")
    except mysql.connector.Error as err:
        print(f"Erreur lors de la planification du cours : {err}")

def main():
    # Connexion à la base de données
    conn = connect_to_database()
    if not conn:
        return

    # Récupérer les matières enseignées
    matieres = get_matieres(conn)

    # Afficher les matières et demander à l'utilisateur de choisir une matière
    print("Liste des matières :")
    for matiere in matieres:
        print(f"{matiere[0]}. {matiere[1]}")
    while True:
        try:
            id_matiere = int(input("Entrez le numéro de la matière pour laquelle vous voulez planifier un cours : "))
            if any(id_matiere == matiere[0] for matiere in matieres):
                break
            else:
                print("Veuillez entrer un numéro de matière valide.")
        except ValueError:
            print("Veuillez entrer un numéro de matière valide.")

    # Récupérer la durée du cours pour la matière sélectionnée
    while True:
        duree_cours = input("Entrez la durée du cours pour cette matière (HH:MM) : ")
        if validate_time_format(duree_cours):
            break
        else:
            print("Veuillez entrer une durée valide au format HH:MM.")

    # Récupérer les disponibilités des professeurs pour cette matière
    professor_availability = get_professor_availability(conn, id_matiere)

    # Récupérer la capacité requise pour la salle en fonction du nombre d'étudiants
    while True:
        try:
            nombre_etudiants = int(input("Entrez le nombre d'étudiants pour ce cours : "))
            capacite_requise = nombre_etudiants + 5  # Ajouter une marge de sécurité
            break
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    # Récupérer les disponibilités des salles en fonction de la capacité requise
    room_availability = get_room_availability(conn, capacite_requise)

    # Trouver un créneau disponible pour le cours
    jour, heure_debut, heure_fin = find_available_slot(professor_availability, room_availability, duree_cours)

    # Planifier le cours si un créneau est trouvé
    if jour and heure_debut and heure_fin:
        id_salle = room_availability[0]  # Sélectionner la première salle disponible
        schedule_course(conn, id_matiere, id_salle, jour, heure_debut, heure_fin)
    else:
        print("Impossible de trouver un créneau disponible pour ce cours.")

    # Fermeture de la connexion à la base de données
    conn.close()

if __name__ == "__main__":
    main()
