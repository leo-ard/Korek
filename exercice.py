from util import choice
import os

def open_exercice(exercice, path):
    possible_path = os.path.join(path, exercice.name + ".py")
    if not os.path.exists(possible_path):
        possible_path = os.path.join(path, choice("File not found, choose plz", os.listdir(path)))

    print(possible_path)
    os.system("code \"" + possible_path + "\"")