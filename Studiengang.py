from Studienelement import StudyElement  # Importieren der Oberklasse, von der geerbt wird
from Semester import Semester  # Importieren der Klasse Semester
from typing import List, Literal  # Importieren von List und Literal für Typisierung

# Definition der Klasse CourseOfStudies, die von StudyElement erbt
class CourseOfStudies(StudyElement):
    possible_degrees = ['Bachelor', 'Master', 'MBA']  # Mögliche Abschlüsse
    PossibleDegrees = Literal['Bachelor', 'Master', 'MBA']  # Literals für mögliche Abschlüsse

    def __init__(self, name: str, elements: List[Semester], degree: PossibleDegrees):
        # Aufruf des Konstruktors der Oberklasse (StudyElement), um deren Attribute zu initialisieren
        super().__init__(name, elements)  # 'name' und 'elements' werden an die Oberklasse übergeben
        # Überprüfen, ob 'elements' eine Liste ist und ob sie nicht leer ist
        if isinstance(elements, list) or elements == []:
            # Durchgehen der Liste 'elements' und sicherstellen, dass jedes Element vom Typ 'Semester' ist
            for element in elements:
                if not isinstance(element, Semester):
                    # Fehler auslösen, wenn ein Element kein 'Semester' ist
                    raise ValueError('Every element in elements must be a Semester. Elements can not be empty.')
        else:
            # Fehler auslösen, wenn 'elements' keine Liste ist
            raise ValueError('Elements must be a list.')
        
        # Überprüfen, ob der Abschluss (degree) zu den möglichen Abschlüssen gehört
        if degree not in CourseOfStudies.possible_degrees:
            raise ValueError('Degree must be "Bachelor", "Master" or "MBA".')
        
        # Speichern des Abschlusses als private Instanzvariable
        self._degree = degree

    # Getter für degree
    @property
    def degree(self):
        return self._degree
    
    # Setter für degree
    @degree.setter
    def degree(self, new_degree):
        # Überprüfen, ob der neue Abschluss gültig ist
        if new_degree not in CourseOfStudies.possible_degrees:
            raise ValueError('Degree must be "Bachelor", "Master" or "MBA".')
        # Setzen des neuen Abschlusses
        self._degree = new_degree

    # Berechnen der Studiendauer als durchschnittliche Anzahl von Semestern
    @property
    def study_duration(self):
        # Die Studiendauer basiert auf der Anzahl der Semester (elements) geteilt durch 2
        duration = len(self.elements) / 2
        # Rückgabe der Studiendauer als formatierter String
        return f'{duration:.1f}'.rstrip('0').rstrip('.')