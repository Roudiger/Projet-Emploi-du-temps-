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

def main():
    # Connexion à la base de données
    conn = connect_to_database()
    if not conn:
        return

    # Ajouter une nouvelle matière
    create_matiere(conn)

    # Fermeture de la connexion à la base de données
    conn.close()

if __name__ == "__main__":
    main()
