from Studienelement import StudyElement  # Importieren der Oberklasse, von der geerbt wird
from Kurs import Course  # Importieren der Klasse Course
from typing import List  # Importieren von List aus dem Modul 'typing' für die Typisierung

# Definition der Klasse Module, die von StudyElement erbt
class Module(StudyElement):
    def __init__(self, name: str, elements: List[Course]):
        # Aufruf des Konstruktors der Oberklasse (StudyElement), um deren Attribute zu initialisieren
        super().__init__(name, elements)  # 'name' und 'elements' werden von der Oberklasse geerbt
        # Überprüfen, ob 'elements' eine Liste ist und ob sie nicht leer ist
        if isinstance(elements, list) or elements == []:
            # Durchgehen der Liste 'elements' und sicherstellen, dass jedes Element vom Typ 'Course' ist
            for element in elements:
               if not isinstance(element, Course):
                  # Fehler auslösen, wenn ein Element kein 'Course' ist
                  raise ValueError('Every element in elements must be a Course. Elements can not be empty.')
        else:
            # Fehler auslösen, wenn 'elements' keine Liste ist
            raise ValueError('Elements must be a list.')