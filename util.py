import inquirer
from difflib import get_close_matches

def choice(question, choices):
    question = inquirer.List("q", message=question, choices=choices)
    return inquirer.prompt([question])['q']

def yes_no(question, yes, no):
    x = None
    while x != "y" and x != "n": 
        x = input(question)
    return yes if x == 'y' else no

def fuzz_search(full_list, search_for = False):
    print(full_list)
    if not search_for:
        search_for = input("Seach name for : ")
    while True:
        possible_match = get_close_matches(search_for, full_list)
        if len(possible_match) == 0:
            possible_match = [x for x in full_list if x.lower().startswith(search_for)]
        x = choice("Is it one of those : ", possible_match + ["Aucun"])
        if x != "Aucun":
            return x
        search_for = input("Seach name for : ")