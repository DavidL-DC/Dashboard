from typing import List, Literal
from datetime import date, timedelta

class StudyElement:
   # Definiert die möglichen Statuswerte für ein Studienelement
   possible_statuses = ['offen', 'aktiv', 'Bewertung ausstehend', 'abgeschlossen', 'pausiert']
   PossibleStatuses = Literal['offen', 'aktiv', 'Bewertung ausstehend', 'abgeschlossen', 'pausiert']
   
   def __init__(self, name: str, elements: List['StudyElement']):
         # Initialisiert ein Studienelement mit Name, Status, Unterelementen und Standardwerten
         if not isinstance(name, str):
            raise ValueError('Name must be a string.')
         if isinstance(elements, list) or elements == []:
            for element in elements:
               if not isinstance(element, StudyElement):
                  raise ValueError('Every element in elements must be a StudyElement. Elements can not be empty.')
         else:
            raise ValueError('Elements must be a list.')
         self._name = name
         self._status = 'offen'
         self._elements = elements
         self._try_number = 'KA'
         self._start_date = 'KA'
         self._end_date = 'KA'
         self._start_date_2 = 'KA'
         self._end_date_2 = 'KA'
         self._start_date_3 = 'KA'
         self._end_date_3 = 'KA'
         self._ect = 5

   @property
   def duration(self):
      # Berechnet die Gesamtdauer in Wochen, basierend auf den Unterelementen
      if self.status == 'abgeschlossen':
         total_duration = timedelta() # Platzhalte für die Gesamtdauer
         for element in self.elements:
            total_duration += element.duration
         return total_duration
      else:
         return 'KA'

   @property
   # Berechnet die gesamten ECTs, basierend auf den Unterelementen
   def ect(self):
      if self.elements != []:
         total_ects = 0
         for element in self.elements:
            total_ects = total_ects + element.ect
         return total_ects
      else:
          return self._ect
      
   @ect.setter
   def ect(self, new_ect):
      # Validiert und setzt neue ECT-Werte
      if not isinstance(new_ect, int):
            raise ValueError('ECT must be a integer.')
      self._ect = new_ect
               
   @property
   def name(self):
      return self._name
   
   @name.setter
   def name(self, new_name):
      # Validiert und setzt neuen Namen
      if not isinstance(new_name, str):
            raise ValueError('Name must be a string.')
      self._name = new_name

   @property
   def status(self):
      # Ermittelt den  Status basierend auf den Unterelementen
      if all(element.status == 'abgeschlossen' for element in self.elements):
         return 'abgeschlossen'
      elif all(element.status == 'offen' for element in self.elements):
         return 'offen'
      elif all(element.status in ['abgeschlossen', 'Bewertung ausstehend'] for element in self.elements):
         return 'Bewertung ausstehend'
      else:
         return 'aktiv'
   
   @status.setter
   def status(self, new_status):
      # Validiert und setzt neuen Status
      if new_status not in StudyElement.possible_statuses:
         raise ValueError('Status must be "offen", "aktiv", "Bewertung ausstehend" oder "abgeschlossen".')
      self._status = new_status

   @property
   def elements(self):
       return self._elements
   
   @elements.setter
   def elements(self, new_elements):
      # Validiert und setzt die Unterelemente
      if isinstance(new_elements, list):
            for element in new_elements:
               if not isinstance(element, StudyElement) or new_elements == []:
                  raise ValueError('Every element in elements must be a StudyElement. Elements can not be empty.')
      else:
         raise ValueError('Elements must be a list.')

   @property
   def try_number(self):
      return 'KA'
   
   @try_number.setter
   def try_number(self, new_try_number):
      # Gibt an, dass dieses Attribut für nicht-Kurse nicht verfügbar ist
      print('Study elements that are not a course have no attribute "try_number".')
      self._try_number = 'KA'
      
   @property
   def start_date(self):
      # Gibt das früheste Startdatum aus den Unterelementen zurück
      if self.status != 'offen':
         return self.find_earliest_date()
      else:
         return 'KA'

   @start_date.setter
   def start_date(self, new_start_date):
      # Validiert und setzt das Startdatum
      if not isinstance(new_start_date, date):
         raise ValueError('Start_date must be a date.')
      self._start_date = new_start_date
   
   @property
   def end_date(self):
      # Gibt das späteste Enddatum aus den Unterelementen zurück
      if self.status in ['Bewertung ausstehend', 'abgeschlossen']:
         return self.find_latest_date()
      else:
         return 'KA'
   
   @end_date.setter
   def end_date(self, new_end_date):
      # Validiert und setzt das Enddatum
      if not isinstance(new_end_date, date):
         raise ValueError('End_date must be a date.')
      self._end_date = new_end_date
      
   @property
   def start_date_2(self):
      return 'KA'

   @start_date_2.setter
   def start_date_2(self, new_start_date_2):
      # Gibt an, dass dieses Attribut für nicht-Kurse nicht verfügbar ist
      print('Study elements that are not a course have no attribute "start_date_2".')

   @property
   def end_date_2(self):
      return 'KA'

   @end_date_2.setter
   def end_date_2(self, new_end_date_2):
      # Gibt an, dass dieses Attribut für nicht-Kurse nicht verfügbar ist
      print('Study elements that are not a course have no attribute "end_date_2".')

   @property
   def start_date_3(self):
      return 'KA'

   @start_date_3.setter
   def start_date_3(sel, new_start_date_3):
      # Gibt an, dass dieses Attribut für nicht-Kurse nicht verfügbar ist
      print('Study elements that are not a course have no attribute "start_date_3".')

   @property
   def end_date_3(self):
      return 'KA'

   @end_date_3.setter
   def end_date_3(self, new_end_date_3):
      # Gibt an, dass dieses Attribut für nicht-Kurse nicht verfügbar ist
      print('Study elements that are not a course have no attribute "end_date_3".')

   def find_latest_date(self):
      # Findet das späteste Datum unter den Enddaten der Unterelemente
      valid_end_dates = []
      for element in self.elements:
         for date in [element.end_date, element._end_date_2, element._end_date_3]:
            if date != 'KA':
               valid_end_dates.append(date)
      return max(valid_end_dates)
   
   def find_earliest_date(self):
      # Findet das früheste Datum unter den Startdaten der Unterelemente
      valid_start_dates = []
      for element in self.elements:
         if element.start_date != 'KA':
            valid_start_dates.append(element.start_date)
      return min(valid_start_dates)