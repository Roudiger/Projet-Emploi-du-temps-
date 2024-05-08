import mysql.connector

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
                        cursor.execute("INSERT INTO Disponibilites_salle (ID_Salle, JourSemaine, HeureDebut, HeureFin) VALUES ((SELECT ID_Salle FROM Salles WHERE Nom = %s), %s, %s, %s)", (salle, jour, heure_disponible[0], heure_disponible[1]))
                else:
                    heure_disponible = heures[indice]
                    cursor.execute("INSERT INTO Disponibilites_salle (ID_Salle, JourSemaine, HeureDebut, HeureFin) VALUES ((SELECT ID_Salle FROM Salles WHERE Nom = %s), %s, %s, %s)", (salle, jour, heure_disponible[0], heure_disponible[1]))
        conn.commit()
        print(f"Disponibilités pour la salle {salle} ajoutées avec succès.")
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'ajout des disponibilités pour la salle {salle} : {err}")

def main():
    # Connexion à la base de données
    conn = connect_to_database()
    if not conn:
        return

    # Ajouter de nouvelles salles
    create_salle(conn)

    # Fermeture de la connexion à la base de données
    conn.close()

if __name__ == "__main__":
    main()
