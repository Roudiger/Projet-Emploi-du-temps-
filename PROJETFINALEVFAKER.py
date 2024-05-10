import openpyxl
from openpyxl.styles import Font
from faker import Faker
import random
from datetime import timedelta

fake = Faker()

# Fonction pour créer des noms de professeurs aléatoires
def generate_professor_name():
    return fake.last_name(), fake.first_name()

# Fonction pour créer des noms de matières aléatoires
def generate_subject():
    return fake.word()

# Fonction pour créer des noms de salles aléatoires
def generate_room_name():
    return fake.company()

# Fonction pour générer des disponibilités aléatoires
def generate_availability():
    days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']
    hours = [(i, i+1) for i in range(8, 20)]  # De 8h à 20h
    availability = {}
    for day in days:
        availability[day] = random.sample(hours, random.randint(2, len(hours)))
    return availability

# Fonction pour générer des cours aléatoires pour les professeurs
def generate_courses():
    days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']
    courses = []
    for day in days:
        for _ in range(random.randint(1, 3)):
            start_hour = random.randint(8, 16)
            end_hour = start_hour + random.randint(1, 3)
            courses.append({
                'Matiere': generate_subject(),
                'Salle': generate_room_name(),
                'JourSemaine': day,
                'HeureDebut': start_hour,
                'HeureFin': end_hour
            })
    return courses

# Fonction pour organiser les cours des professeurs dans une structure de données
def organize_professor_courses(courses):
    timetable = {str(hour).zfill(2) + 'h': {} for hour in range(8, 21)}

    for course in courses:
        day = course['JourSemaine']
        start_time = str(course['HeureDebut']).zfill(2) + 'h'
        end_time = str(course['HeureFin']).zfill(2) + 'h'
        info = f"{course['Matiere']} - {course['Salle']}"

        if day not in timetable[start_time]:
            timetable[start_time][day] = [info]
        else:
            timetable[start_time][day].append(info)

    return timetable

# Fonction pour créer le fichier Excel pour les cours des professeurs
def create_professor_excel_file(timetable):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Emploi du temps Professeurs'

    # Ajouter les en-têtes de colonnes (jours de la semaine)
    days_of_week = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
    ws.append(['Heures'] + days_of_week)

    # Ajouter les heures (lignes) et les cours correspondants (cellules)
    for hour, schedule in timetable.items():
        row = [hour]
        for day in days_of_week:
            if day in schedule:
                row.append('\n'.join(schedule[day]))
            else:
                row.append('')
        ws.append(row)

    # Ajuster la largeur des colonnes
    ws.column_dimensions['A'].width = 10
    for col in range(2, len(days_of_week) + 2):
        ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 30

    # Enregistrer le fichier Excel
    filename = 'emploi_du_temps_professeurs.xlsx'
    wb.save(filename)
    print(f'Le fichier {filename} a été créé avec succès.')

def main():
    # Générer des données aléatoires
    professors = [generate_professor_name() for _ in range(5)]
    subjects = [generate_subject() for _ in range(5)]
    rooms = [generate_room_name() for _ in range(3)]
    professor_courses = []
    for professor in professors:
        for _ in range(random.randint(1, 3)):
            professor_courses.append({
                'Matiere': random.choice(subjects),
                'Salle': random.choice(rooms),
                'JourSemaine': random.choice(['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi','Samedi']),
                'HeureDebut': random.randint(8, 16),
                'HeureFin': random.randint(9, 17)
            })

    # Organiser les cours des professeurs dans une structure de données
    professor_timetable = organize_professor_courses(professor_courses)

    # Créer le fichier Excel
    create_professor_excel_file(professor_timetable)

if __name__ == "__main__":
    main()
