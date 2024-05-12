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

# Fonction pour créer une nouvelle classe
def create_classe(conn):
    try:
        cursor = conn.cursor()
        nom_classe = input("Entrez le nom de la classe : ")
        cursor.execute("INSERT INTO Classes (Nom) VALUES (%s)", (nom_classe,))
        conn.commit()
        print("Classe ajoutée avec succès.")
        return cursor.lastrowid  # Récupère l'ID de la dernière classe ajoutée
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'ajout de la classe : {err}")
        return None

# Fonction pour ajouter un nouvel élève à une classe donnée
def add_eleve(conn, id_classe):
    try:
        cursor = conn.cursor()
        nom_eleve = input("Entrez le nom de l'élève : ")
        prenom_eleve = input("Entrez le prénom de l'élève : ")
        cursor.execute("INSERT INTO Eleves (Nom, Prenom, ID_Classe) VALUES (%s, %s, %s)", (nom_eleve, prenom_eleve, id_classe))
        conn.commit()
        print("Élève ajouté avec succès.")
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'ajout de l'élève : {err}")

def main():
    # Connexion à la base de données
    conn = connect_to_database()
    if not conn:
        return

    # Demander combien de classes créer
    nombre_classes = int(input("Combien de classes voulez-vous créer ? "))

    # Créer les classes
    for _ in range(nombre_classes):
        id_classe = create_classe(conn)
        if id_classe is not None:
            # Ajouter des élèves à la classe
            nombre_eleves = int(input("Entrez le nombre d'élèves à ajouter à cette classe : "))
            for _ in range(nombre_eleves):
                add_eleve(conn, id_classe)

    # Fermeture de la connexion à la base de données
    conn.close()

if __name__ == "__main__":
    main()
