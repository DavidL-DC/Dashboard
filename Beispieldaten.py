from Kurs import Course  # Importiert die Klasse Course aus Kurs
from Modul import Module  # Importiert die Klasse Module aus Modul
from Semester import Semester  # Importiert die Klasse Semester aus Semester
from Studiengang import CourseOfStudies  # Importiert die Klasse CourseOfStudies aus Studiengang
from Student import Student  # Importiert die Klasse Student aus Student
from Ziel import Goal  # Importiert die Goal aus Ziel
from datetime import date, timedelta  # Die Datetime-Klasse wird zur Handhabung von Daten verwendet

# Kopierter Text aus dem Studiumsablaufplan zu meinem Studiengang ('Angewandte Künstliche Intelligenz')
text = """DLBDSEAIS01_D Artificial Intelligence 5 Klausur
DLBWIRITT01 Einführung in das wissenschaftliche Arbeiten für IT und Technik 5 Advanced Workbook
DLBDSIPWP01_D Einführung in die Programmierung mit Python 5 Klausur
DLBBIMD01 Mathematics: Analysis 5 Klausur
DLBKA01 Kollaboratives Arbeiten 5 Fachpräsentation
DLBDSSPDS01_D Statistics - Probability and Descriptive Statistics 5 Klausur
DLBDSOOFPP01_D Objektorientierte und funktionale Programmierung mit Python 5 Portfolio
DLBBIM01 Mathematik: Lineare Algebra 5 Klausur
DLBIHK01 Interkulturelle und ethische Handlungskompetenz 5 Fallstudie
DLBDSSIS01_D Statistik - Schließende Statistik 5 Klausur
DLBDSCC01_D Cloud Computing 5 Klausur
DLBSEPCP01_D Cloud Programming 5 Portfolio
DLBDSMLSL01_D Maschinelles Lernen - Supervised Learning 5 Klausur
DLBDSMLUSL01_D Maschinelles Lernen - Unsupervised Learning und Feature Engineering 5 Fallstudie
DLBDSNNDL01_D Neuronale Netze und Deep Learning 5 Fachpräsentation
DLBAIICV01_D Einführung in Computer Vision 5 Klausur
DLBAIPCV01_D Projekt: Computer Vision 5 Projektbericht
DLBAIIRL01_D Einführung in das Reinforcement Learning 5 Klausur
DLBAIINLP01_D Einführung in NLP 5 Klausur
DLBAIPNLP01_D Projekt: NLP 5 Projektbericht
DLBISIC01 Einführung in Datenschutz und IT-Sicherheit 5 Klausur
DLBDSDSSE01_D Data Science Software Engineering 5 Klausur
DLBDSMTP01_D Projekt: Vom Modell zum Produktvertrieb 5 Projektpräsentation
DLBDSSECDS01_D Seminar: Ethische Fragen der Data Science 5 Seminararbeit
DLBMIUEX01 User Experience 5 Klausur
DLBAIPEAI01_D Projekt: Edge AI 5 Projektbericht
DLBROIR01_D Einführung in die Robotik 5 Hausarbeit
DLBDBAPM01 Agiles Projektmanagement 5 Projektbericht"""

lines = text.splitlines()  # Zerlegt den Text in einzelne Zeilen, jede Zeile repräsentiert einen Kurs

course_list = []  # Liste zur Speicherung der erstellten Kurse

def create_courses():
    for line in lines:  # Iteration durch jede Kurszeile
        id = line.split()[0]  # Kurs-ID extrahieren
        name = ' '.join(line.split()[1:-2])  # Kursname extrahieren
        if line.split()[-2] == 'Advanced':  # Falls der Kurs ein Advanced Exam hat
            exam = ' '.join(line.split()[-2:])  # Extrahiert den Prüfungs-Typ
        else:
            exam = line.split()[-1]  # Andernfalls wird der letzte Wert als Prüfung verwendet
        course_list.append(Course(name, id, 'offen', 'KA', exam, 'KA', 1))  # Kursobjekt zur Liste hinzufügen
        

create_courses()  # Kurse aus den Zeilen erstellen

# Weitere Kurse werden manuell hinzugefügt (Komposition, mehrere Kurse gehören zum Studiengang)
course_list.append(Course('Wahlpflichtmodul A', 'KA', 'offen', 'KA', 'KA', 'KA', 1))
course_list.append(Course('Wahlpflichtmodul B', 'KA', 'offen', 'KA', 'KA', 'KA', 1))
course_list.append(Course('Wahlpflichtmodul C', 'KA', 'offen', 'KA', 'KA', 'KA', 1))
course_list.append(Course('Bachelorarbeit', 'BBAK01', 'offen', 'KA', 'Abschlussarbeit', 'KA', 1))

# Beispielhafte Kursdaten zu jedem Kurs hinzufügen
course_list[0]._status = 'abgeschlossen'
course_list[0]._start_date = date(2024, 1, 26)
course_list[0]._end_date = date(2024, 2, 11)
course_list[0]._grade = 2.7
course_list[0]._mentor = 'Petra Fuhs'
course_list[1]._status = 'abgeschlossen'
course_list[1]._start_date = date(2024, 2, 11)
course_list[1]._end_date = date(2024, 3, 9)
course_list[1]._grade = 2.3
course_list[1]._mentor = 'Markus Kleffmann'
course_list[2]._status = 'abgeschlossen'
course_list[2]._start_date = date(2024, 3, 9)
course_list[2]._end_date = date(2024, 4, 21)
course_list[2]._grade = 2
course_list[2]._mentor = 'Gabriele Bleser-Taetz'
course_list[3]._status = 'abgeschlossen'
course_list[3]._start_date = date(2024, 4, 21)
course_list[3]._end_date = date(2024, 5, 28)
course_list[3]._grade = 3
course_list[3]._mentor = 'Nazli Andjic'
course_list[4]._status = 'abgeschlossen'
course_list[4]._start_date = date(2024, 5, 28)
course_list[4]._end_date = date(2024, 6, 16)
course_list[4]._grade = 1.3
course_list[4]._mentor = 'Katja Tombrock-Söll'
course_list[5]._status = 'abgeschlossen'
course_list[5]._start_date = date(2024, 6, 16)
course_list[5]._end_date = date(2024, 7, 30)
course_list[5]._grade = 2
course_list[5]._mentor = 'Robert Graf'
course_list[6]._status = 'offen'
course_list[6]._mentor = 'Jacko Nudzor'
course_list[7]._status = 'abgeschlossen'
course_list[7]._start_date = date(2024, 7, 30)
course_list[7]._end_date = date(2024, 8, 29)
course_list[7]._grade = 4
course_list[7]._mentor = 'Volker Isernhagen'
course_list[8]._status = 'Bewertung ausstehend'
course_list[8]._start_date = date(2024, 8, 29)
course_list[8]._end_date = date(2024, 9, 27)
course_list[8]._start_date_2 = date(2024, 11, 10)
course_list[8]._end_date_2 = date(2024, 12, 7)
course_list[8]._try_number = 2
course_list[8]._mentor = 'Alexandra Araiza'
course_list[9]._status = 'abgeschlossen'
course_list[9]._start_date = date(2024, 9, 27)
course_list[9]._end_date = date(2024, 10, 25)
course_list[9]._start_date_2 = date(2024, 10, 25)
course_list[9]._end_date_2 = date(2024, 11, 10)
course_list[9]._try_number = 2
course_list[9]._grade = 2.7
course_list[9]._mentor = 'Michael Klein'
for course in course_list[-4:]:
    course.ect = 10

module_list = [Module(course.name, [course]) for course in course_list]  # Erstellen von Modulen mit Kursen als Komponenten (Aggregation)

semester_list = [Semester(f'{semester + 1}. Semester', []) for semester in range(6)]  # Erstellen von Semestern (Komposition, Semester besitzen Module)
for module in module_list:
    for semester in semester_list:
        if semester.ect + module.ect <= 30:  # Ein Modul wird nur dann einem Semester zugewiesen, wenn es Platz hat
            semester.elements.append(module)  # Assoziation zwischen Semester und Modul
            break

course_of_studies = CourseOfStudies('B.Sc. Angewandte Künstliche Intelligenz', semester_list, 'Bachelor')  # Kurs des Studiengangs enthält Semester (Komposition)

student = Student('Max Mustermann', 56488293, course_of_studies, date(2024, 1, 26), 309.48)  # Der Student ist Teil des Studiengangs (Assoziation zwischen Student und CourseOfStudies)

# Beispielhafte Ziele des Studenten definieren basierend auf meinen genannten Zielen (Ziele sind Objekte, die den Fortschritt des Studenten überwachen)
grade_goal = Goal('Notendurchschnitt', 2.0, float(student.grade_average), 4.0, True)
active_courses_goal = Goal('Aktive Kurse', 1, int(student.active_courses), 0, False)
revenue_goal = Goal('Gezahlter beitrag', 13000, float(student.contribution_paid), 18500, True)
study_duration_goal = Goal('Voraussichtliche Studiendauer', 3.5, float(student.estimated_study_duration), 5, True)