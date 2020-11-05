#import .Entries
import json
import csv
import os

from util import choice

import inquirer
from kdata.entries import Student, Group, Exercice, ExerciceEntry

import errno

# Taken from https://stackoverflow.com/a/600612/119527
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def safe_open(path, s, **args):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    mkdir_p(os.path.dirname(path))
    return open(path, s, **args)

def load_students(group_path):
    group_name = choice("Choose group", os.listdir(group_path))
    group_path = os.path.join(group_path, group_name)

    group = Group(group_name, group_path)
    with open(group_path, encoding='utf-8') as file:
        reader = csv.reader(file, delimiter = ",")
        # skip first column
        next(reader)
        for row in reader:
            group.students.append(Student(*(row[:5])))

    return group

def find_student(group, student_code):
    for student in group.students:
        if student.code == student_code:
            return student
    return False
    

def save_exercice(exercice):
    for entry in exercice.entries:
        filepath = os.path.join(exercice.save_path, entry.students[0].get_code())
        if not os.path.exists(filepath):
            with safe_open(filepath, "w", encoding="utf-8") as file:
                writer = csv.writer(file, delimiter=",")
                writer.writerow([s.code for s in entry.students] + [entry.grade] + [entry.comments])


def load_exercice(exo_setting_path, group):
    exercice_name = choice("Choose exercice", os.listdir(exo_setting_path))
    exercice_path = os.path.join(exo_setting_path, exercice_name)

    exercice = Exercice(exercice_name, exercice_path)

    exercice.save_path = os.path.join(exercice_path, "save", group.name.split(".")[0])
    
    if os.path.exists(exercice.save_path):
        paths = os.listdir(exercice.save_path)
        for path in paths:
            with open(os.path.join(exercice.save_path, path), "r") as file:
                try:
                    reader = csv.reader(file, delimiter=",")
                    line = next(reader)
                    students_codes = line[:-2]
                    grade = float(line[-2])
                    comment = line[-1]
                    students = []
                    for student_code in students_codes:
                        if (student := find_student(group, student_code)):
                            students.append(student)
                        else:
                            print("ERROR cannot find code : ", student_code)
                            exit(1)

                    exercice.entries.append(ExerciceEntry(students, grade, comment))
                except Exception as e:
                    print("Reading file ", os.path.join(exercice.save_path, path), "got error", e)

    return exercice
    


        




