import mysql.connector
import random
import copy

def fetch_data(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in data]


def generate_initial_timetable(cours, professeurs, matieres, salles):
    initial_timetable = {}

    # Création d'une structure de données pour stocker les cours
    for course in cours:
        jour = course['JourSemaine']
        heure_debut = str(course['HeureDebut'])
        if jour not in initial_timetable:
            initial_timetable[jour] = {}
        if heure_debut not in initial_timetable[jour]:
            initial_timetable[jour][heure_debut] = []

        # Récupération des informations sur le professeur, la matière et la salle
        professeur = next(prof for prof in professeurs if prof['ID_Professeur'] == course['ID_Professeur'])
        matiere = next(mat for mat in matieres if mat['ID_Matiere'] == course['ID_Matiere'])
        salle = next(sal for sal in salles if sal['ID_Salle'] == course['ID_Salle'])

        # Ajout du cours à la structure de données
        initial_timetable[jour][heure_debut].append({
            'Professeur': professeur,
            'Matiere': matiere,
            'Salle': salle,
            'Heure fin': str(course['HeureFin'])
        })

    return initial_timetable

def evaluate_timetable(timetable, disponibilites, capacites_salles):
    conflicts_salle = 0
    conflicts_professeur = 0
    capacity_constraints = 0
    prof_availability_constraints = 0
    individual_preferences = 0

    for jour, heures in timetable.items():
        for heure, cours in heures.items():
            for course in cours:
                salle = course['Salle']
                professeur = course['Professeur']
                heure_debut = heure
                heure_fin = course['Heure fin']

                # Vérification des conflits de salle
                salle_dispo = [disp for disp in disponibilites if disp[1] == jour and disp[2] <= heure_debut and disp[3] >= heure_fin and disp[0] == salle]
                if not salle_dispo:
                    conflicts_salle += 1

                # Vérification des conflits de professeur
                prof_dispo = [disp for disp in disponibilites if disp[1] == jour and disp[2] <= heure_debut and disp[3] >= heure_fin and disp[0] == professeur]
                if not prof_dispo:
                    conflicts_professeur += 1

                # Vérification des contraintes de capacité des salles
                if capacites_salles[salle] < len(cours):
                    capacity_constraints += 1

                # Vérification des contraintes de disponibilité des professeurs
                if not prof_dispo:
                    prof_availability_constraints += 1

                # Vérification des préférences individuelles (non implémentées)

    evaluation = {
        'conflicts_salle': conflicts_salle,
        'conflicts_professeur': conflicts_professeur,
        'capacity_constraints': capacity_constraints,
        'prof_availability_constraints': prof_availability_constraints,
        'individual_preferences': individual_preferences
    }

    return evaluation

def generate_neighborhood(timetable):
    # Génère un voisinage en effectuant un échange aléatoire de deux cours
    # Nous allons simplement choisir deux cours aléatoires et échanger leurs horaires
    new_timetable = copy.deepcopy(timetable)

    # Choix aléatoire d'un jour et d'une heure
    jour1 = random.choice(list(new_timetable.keys()))
    heure1 = random.choice(list(new_timetable[jour1].keys()))

    # Choix aléatoire d'un autre jour et d'une autre heure
    jour2 = random.choice(list(new_timetable.keys()))
    heure2 = random.choice(list(new_timetable[jour2].keys()))

    # Échange des cours entre les deux horaires
    cours1 = new_timetable[jour1][heure1]
    cours2 = new_timetable[jour2][heure2]
    new_timetable[jour1][heure1] = cours2
    new_timetable[jour2][heure2] = cours1

    return new_timetable

def recherche_locale(initial_timetable, disponibilites, capacites_salles, max_iterations=1000):
    current_timetable = initial_timetable
    best_timetable = initial_timetable
    best_evaluation = evaluate_timetable(initial_timetable, disponibilites, capacites_salles)

    iterations = 0
    while iterations < max_iterations:
        new_timetable = generate_neighborhood(current_timetable)
        new_evaluation = evaluate_timetable(new_timetable, disponibilites, capacites_salles)

        if new_evaluation['conflicts_salle'] + new_evaluation['conflicts_professeur'] + new_evaluation['capacity_constraints'] + new_evaluation['prof_availability_constraints'] + new_evaluation['individual_preferences'] < best_evaluation['conflicts_salle'] + best_evaluation['conflicts_professeur'] + best_evaluation['capacity_constraints'] + best_evaluation['prof_availability_constraints'] + best_evaluation['individual_preferences']:
            best_timetable = new_timetable
            best_evaluation = new_evaluation

        current_timetable = new_timetable
        iterations += 1

    return best_timetable

def optimize_timetable(cursor, conn):
    # Fetching data
    cours = fetch_data(cursor, "Cours_Etudiants")
    professeurs = fetch_data(cursor, "Professeurs")
    matieres = fetch_data(cursor, "Matieres")  # Ajout pour récupérer les données des matières
    salles = fetch_data(cursor, "Salles")
    disponibilites = fetch_data(cursor, "Disponibilites")

    # Récupération des capacités des salles
    capacites_salles = {salle['ID_Salle']: salle['Capacite'] for salle in salles}

    # Création d'un emploi du temps initial
    initial_timetable = generate_initial_timetable(cours, professeurs, matieres, salles)

    # Optimisation de l'emploi du temps
    optimized_timetable = recherche_locale(initial_timetable, disponibilites, capacites_salles)

    return optimized_timetable

def main():
    # Connexion à la base de données
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Utopie39*",
        database="projetinfo"
    )
    if not conn:
        print("Erreur de connexion à la base de données.")
        return

    cursor = conn.cursor()

    # Optimisation de l'emploi du temps
    optimized_timetable = optimize_timetable(cursor, conn)

    # Fermeture de la connexion à la base de données
    conn.close()

if __name__ == "__main__":
    main()
