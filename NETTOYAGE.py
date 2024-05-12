import mysql.connector

# Se connecter à la base de données
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mdp",
    database="projetinfo"
)
cursor = conn.cursor()

try:
    # Désactiver les contraintes de clé étrangère
    cursor.execute("SET FOREIGN_KEY_CHECKS=0")

    # Liste des tables
    tables = ["Cours_Etudiants", "Cours_Classe", "Matieres", "Classes", "Salles", "Disponibilites",
              "Disponibilites_salle", "Professeurs", ]

    # Supprimer tous les enregistrements dans chaque table
    for table in tables:
        try:
            cursor.execute(f"DELETE FROM {table}")
            conn.commit()
            print(f"Tous les enregistrements ont été supprimés de la table {table}.")
        except mysql.connector.Error as err:
            print(f"Erreur MySQL : {err}")
            conn.rollback()

    # Réactiver les contraintes de clé étrangère
    cursor.execute("SET FOREIGN_KEY_CHECKS=1")

    # Réinitialiser les compteurs d'auto-incrémentation pour chaque table
    for table in tables:
        try:
            cursor.execute(f"ALTER TABLE {table} AUTO_INCREMENT = 1")
            conn.commit()
            print(f"Le compteur d'auto-incrémentation a été réinitialisé pour la table {table}.")
        except mysql.connector.Error as err:
            print(f"Erreur MySQL : {err}")
            conn.rollback()

    print("Tables réinitialisées avec succès.")

except mysql.connector.Error as err:
    print(f"Erreur MySQL : {err}")
    conn.rollback()

finally:
    # Fermer la connexion à la base de données
    try:
        cursor.close()
        conn.close()
        print("Connexion à la base de données fermée.")
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
