import copy

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

    # Création d'un emploi du temps initial
    initial_timetable = generate_initial_timetable(cours, professeurs, matieres, salles)

    # Optimisation de l'emploi du temps
    optimized_timetable = recherche_locale(initial_timetable, disponibilites, capacites_salles)

    return optimized_timetable
