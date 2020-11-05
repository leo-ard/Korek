import argparse
import os
import sys

path = os.path

from util import choice, fuzz_search, yes_no

from exercice import open_exercice

from kdata.entries import ExerciceEntry

from kdata.data import load_students, load_exercice, save_exercice


# Argparse

parser = argparse.ArgumentParser(description='Program to Korek student code')
parser.add_argument('main_folder', help='Path to the directory containing the corection files')
parsed_args = parser.parse_args(sys.argv[1:])

KOREK_PATH = parsed_args.main_folder
SETTINGS_PATH = path.join(KOREK_PATH, ".korek")

if not path.exists(SETTINGS_PATH):
    print("Error, cannot find configuration folder at :"  + SETTINGS_PATH)
    exit(1)

# load students

group = load_students(path.join(SETTINGS_PATH, "groups"))

# Choose exercice

exercice = load_exercice(path.join(SETTINGS_PATH, "exercices"), group)
print("loaded", len(exercice.entries), "entries")

student_set = dict([(x.first_name + " "+ x.last_name, x) for x in group.students])

def start_correction():
    for folder_name in os.listdir(KOREK_PATH):
        
        if "_" not in folder_name:
            continue

        name = folder_name.split("_")[0]
        
        if name not in student_set:
            name = fuzz_search(student_set.keys(), search_for=name)
        print("Found", name)
        students = [student_set[name]]

        if students[0].code in [x.students[0].code for x in exercice.entries]:
            print("skipping " + students[0].first_name + "\n")
            continue

        open_exercice(exercice, os.path.join(KOREK_PATH, folder_name))
        
        if yes_no("Is there another student (y/n) ?", True, False):
            students.append(student_set[fuzz_search(student_set.keys())])
        
        print("Une serie de question va être posé. La réponse doit être du style [points enlevés] [commentaire]. n pour next")
        questions = ['Remise', 'Fonctionnement du code', 'Commentaires', 'Beauté du code \n  - nom de variable \n  - aération des expressions \n  - variables inutile/répétition de code \n  - modulaire', "Autre commentaire"]
        comment = [[] * len(questions)]

        affichage = [
            (0, "Remise"),
            (50, "Fonctionnement du code"),
            (10, "Commentaires"),
            (40, "Beauté du code"),
            (0, "Autre commentaires")
        ]

        grade = 100

        final_string = ""

        for i in range(len(questions)):
            x = input("?? " + questions[i] + "\n-> ")
            current_string = ""
            point_lost = 0

            max_point, text  = affichage[i]

            while x != "n":
                try:
                    p = float(x.split()[0])
                    assert p <= 0
                    point_lost += p
                    current_string += "  " + x + "\n"
                except Exception as e:
                    print("error got", e)
                x = input("-> ")

            if max_point != 0 or len(current_string) != 0:
                grade += point_lost
                next_to = ""
                if max_point == 0:
                    next_to = str(point_lost)
                else:
                    next_to = str(abs(point_lost +max_point)) + "/" + str(max_point) 
                final_string += text + " " + next_to + " \n"
                final_string += current_string

        final_string += "\nNOTE FINALE : " + str(grade)

        exercice.entries.append(ExerciceEntry(students, grade, final_string))
        save_exercice(exercice)

        print(final_string + "\n\n====================")
            
        #correct(exercice, path.join(KOREK_PATH, name))

start_correction()