class Student():
    def __init__(self, first_name, last_name, code, email, matricule):
        self.first_name = first_name
        self.last_name = last_name
        self.code = code
        self.email = email
        self.matricule = matricule

    def __repr__(self):
        return "Student(name=%s, code=%s)" % (self.first_name + " " + self.last_name, self.code)
    def get_code(self):
        return self.first_name.replace(" ", "_") + self.code

class Group():
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.students = []

class ExerciceEntry():
    def __init__(self, student, grade, comments):
        # By reference
        self.students = student
        # Style points, comment on points
        self.comments = comments
        self.grade = grade

    def __repr__(self):
        return "Entry( student=%s, grade=%d, comments=%s)" % (self.students, self.grade,self.comments[:min(len(self.comments), 25)].replace("\n",""))
    
class Exercice():
    def __init__(self, name, path):
        self.entries = []
        self.name = name
        self.path = path
        

        