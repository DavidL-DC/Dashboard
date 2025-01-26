from Studienelement import StudyElement  # Importieren der Oberklasse, von der geerbt wird
from Modul import Module  # Importieren der Klasse Module
from typing import List  # Importieren von List aus dem Modul 'typing' für die Typisierung

# Definition der Klasse Semester, die von StudyElement erbt
class Semester(StudyElement):
    def __init__(self, name: str, elements: List[Module]):
        # Aufruf des Konstruktors der Oberklasse (StudyElement), um deren Attribute zu initialisieren
        super().__init__(name, elements)  # 'name' und 'elements' werden an die Oberklasse übergeben
        # Überprüfen, ob 'elements' eine Liste ist und ob sie nicht leer ist
        if isinstance(elements, list) or elements == []:
            # Durchgehen der Liste 'elements' und sicherstellen, dass jedes Element vom Typ 'Module' ist
            for element in elements:
               if not isinstance(element, Module):
                  # Fehler auslösen, wenn ein Element kein 'Module' ist
                  raise ValueError('Every element in elements must be a Module. Elements can not be empty.')
        else:
            # Fehler auslösen, wenn 'elements' keine Liste ist
            raise ValueError('Elements must be a list.')