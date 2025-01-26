from datetime import date, timedelta
from Studienelement import StudyElement         # Importieren der Oberklasse, von der geerbt wird
from typing import Literal
from decimal import Decimal, ROUND_UP

class Course(StudyElement):
    # Statische Variablen der Klasse:
    # exam_types definiert die möglichen Prüfungsformen für Kurse. Diese werden auch als Literal (ExamTypes) definiert, um die Eingabe zu validieren.
    exam_types = ['Abschlussarbeit', 'Klausur', 'Hausarbeit', 'Seminararbeit', 'Fallstudie', 'Projektbericht', 'Advanced Workbook', 'Fachpräsentation', 'Konzeptpräsentation', 'Projektpräsentation', 'Portfolio', 'Creative Workbook', 'KA'] #Liste aller Prüfungsformen
    ExamTypes = Literal['Abschlussarbeit', 'Klausur', 'Hausarbeit', 'Seminararbeit', 'Fallstudie', 'Projektbericht', 'Advanced Workbook', 'Fachpräsentation', 'Konzeptpräsentation', 'Projektpräsentation', 'Portfolio', 'Creative Workbook', 'KA']
    course_list = [] # Liste aller Kurse
    def __init__(self, name: str, id: str, status: StudyElement.PossibleStatuses, mentor: str, exam: ExamTypes, grade: float, try_number=1):    # Übernimmt mögliche Status aus StudyElement
        # Initialisierung der Oberklasse StudyElement. `elements` wird hier als leere Liste übergeben, da ein Kurs keine weiteren Elemente enthält.
        super().__init__(name, elements=[])
        # Validierung der Eingabeparameter, um sicherzustellen, dass alle Attributwerte gültig sind.
        if not isinstance(id, str):
            raise ValueError('ID must be string.')
        if status not in StudyElement.possible_statuses:
            raise ValueError(f'Status must be one of this: {", ".join(StudyElement.possible_statuses)}.')
        if not isinstance(mentor, str):
            raise ValueError('Mentor must be string.')
        if exam not in Course.exam_types:
            raise ValueError(f'Exam must be one of this: {", ".join(Course.exam_types)}.')
        if not isinstance(grade, (float, int)) and grade != 'KA':
            raise ValueError('Grade must be a float or integer between 1 and 4, 5 or "KA".')
        elif grade != 'KA':
            # Zusätzliche Validierung, wenn die Note nicht "KA" (keine Angabe) ist.
            if not (1 <= grade <= 4) and grade != 5:
                raise ValueError('Grade must be a float or integer between 1 and 4, 5 or "KA".')
            elif status != 'abgeschlossen' and (1 <= grade <= 4):
                raise ValueError('A not finished Course has no grade except 5.')
            elif status != 'abgeschlossen' and try_number == 1:
                raise ValueError('The first try of a course has no grade if it is not finished.')
        elif status == 'abgeschlossen':
            raise ValueError('Finished courses require a grade.')
        if try_number not in [1, 2, 3]:
            raise ValueError('Try_number must be 1, 2 or 3.')
        # Zuweisung der Attribute zur Repräsentation eines Kursobjekts.
        self._id = id
        self._status = status
        self._mentor = mentor
        self._exam = exam
        self._try_number = try_number
        self._grade = f'{round(grade, 1):.1f}' if grade != 'KA' else 'KA'
        self._try_number = try_number
        self._pause_start = 'KA'    # Startzeitpunkt einer Pause (falls vorhanden).
        self._pause_total = timedelta() # Gesamte Pausezeit.
        # Initialisierung kursbezogener Daten (z. B. Start- und Enddaten).
        self.init_dates()
        # Falls der Status des Kurses "aktiv" ist, wird geprüft, ob es weitere aktive Kurse gibt.
        if self.status == 'aktiv':
            self.choose_active_course()
        # Hinzufügen des Kursobjekts zur Liste aller Kurse.
        Course.course_list.append(self)

    # Methode zur Erstellung eines Datums anhand einer Benutzereingabe.
    def create_date(self):
        day = int(input('Tag:'))
        month = int(input('Monat:'))
        year_value = input('Jahr:')
        if len(year_value) == 2:
            year = 2000 + int(year_value)
        else:
            year = year_value
        return date(year, month, day)

     # Initialisiert wichtige Datumsangaben für den Kurs.
    def init_dates(self):
        # Bedingungen für Kurse, die nicht im ersten Versuch offen sind.
        if not (self.status == 'offen' and self.try_number == 1):
            print(f'Wann wurde der erste Versuch vom Kurs "{self.name}" gestartet?')
            self.start_date = (self.create_date(), True)
            if self._try_number > 1:
                print(f'Wann wurde der erste Versuch vom Kurs "{self.name}" abgeschlossen?')
                self.end_date = (self.create_date(), True)
                if self.status != 'offen':
                    print(f'Wann wurde der zweite Versuch vom Kurs "{self.name}" gestartet?')
                    self.start_date_2 = (self.create_date(), True)
                if self._try_number == 3:
                    print(f'Wann wurde der zweite Versuch vom Kurs "{self.name}" abgeschlossen?')
                    self.end_date_2 = (self.create_date(), True)
                    if self.status != 'offen':
                        print(f'Wann wurde der dritte Versuch vom Kurs "{self.name}" gestartet?')
                        self.start_date_3 = (self.create_date(), True)
            # Bedingungen für abgeschlossene Kurse oder solche mit ausstehender Bewertung.
            if self.status in ['Bewertung ausstehend', 'abgeschlossen']:
                if self._try_number == 1:
                    print(f'Wann wurde der erste Versuch vom Kurs "{self.name}" abgeschlossen?')
                    self.end_date = (self.create_date(), True)
                elif self._try_number > 1:
                    print(f'Wann wurde der zweite Versuch vom Kurs "{self.name}" abgeschlossen?')
                    self.end_date_2 = (self.create_date(), True)
                    if self._try_number == 3:
                        print(f'Wann wurde der dritte Versuch vom Kurs "{self.name}" abgeschlossen?')
                        self.end_date_3 = self.create_date()
            # Zusätzliche Handhabung pausierter Kurse.
            if self.status == 'pausiert':
                print(f'Seit wann ist der Kurs "{self.name}" aktuell pausiert?')
                self.pause_start = self.create_date()
            # Fragt vergangen Pausierungen ab.
            pause_days = int(input(f'Wie viele Tage wurde der Kurs bereits pausiert? (Exklusive aktueller Pausierung)'))
            self._pause_total += timedelta(pause_days)
            # Falls der Kurs nicht abgeschlossen ist und es sich um einen erneuten Versuch handelt, wird die Note auf 5 gesetzt.
            if self.status != 'abgeschlossen' and self.try_number > 1:
                self._grade = 5

    # Wählt einen Kurs als "aktiv" aus, wenn der aktuelle Kursstatus "aktiv" ist.
    def choose_active_course(self):
        # Überprüfen, ob ein anderer Kurs bereits aktiv ist.
        if not all(course.status != 'aktiv' for course in Course.course_list):
            for index, course in enumerate(Course.course_list):
                if course.status == 'aktiv':
                    print(f'Es gibt bereits einen aktiven Kurs: "{course.name}".')
                    answer = input(f'Soll der aktive Kurs pausiert werden und stattdessen "{self.name}" aktiviert werden? (J/N)')
                    if answer not in ['J', 'N']:
                        raise ValueError('Answer must be J (Yes) or N (No).')
                    elif answer == 'J':
                        Course.course_list[index].pause_course(True)    # Setzt den Status des vorherigen aktiven Kurses auf "pausiert".
                        self._status = 'aktiv'  # Setzt den Status des aktuellen Kurses auf "aktiv".
                    elif answer == 'N':
                        self.pause_course(True)
                    break
        else:
            self._status = 'aktiv'

    # Startet einen neuen Kurses, wenn der aktive abgeschlossen wurde
    def start_next_course(self):
        index = 1
        open_courses = []
        # Fragt ab welcher der anderen, zu bearbeitenden, Kurse gestartet werden soll
        print('Welchen Kurs als nächstes?')
        for course in Course.course_list:
            if course.status == 'aktiv':
                course.pause_course(True)
            if course.status in ['offen', 'pausiert'] and course != self:
                open_courses.append(course)
        for course in open_courses:
            print(f'{index}. {course.name} ({course._try_number}.Versuch) ({course.status})')
            index += 1
        if index == 1:
            print('Es sind alle Kurse abgeschlossen.')  # Falls alle Kurse abgeschlossen sind
        else:
            number = int(input('Zahl eingeben:'))
            open_courses[number-1].status = 'aktiv'
    
    # Pausiert den aktiven Kurs und startet einen anderen
    def pause_course(self, init = False):   # init gibt an, ob es sich um einen neu initialisierten Kurs handelt
        if self.status != 'pausiert':
            if not init:
                if self.status not in ['aktiv']:    # Nur aktive Kurse können pausiert werden
                    raise ValueError('Course can only be paused if it is active.')
                self._status = 'pausiert'
                self.start_next_course()    # Starten eines neuen Kurses
            else:
                self._status = 'pausiert'
            self._pause_start = date.today()
        else:
            print('Der Kurs ist bereits pausiert.')
        

    # Setzt das Startdatum oder aktualisiert Pausendauer basierend auf Status und Versuchszahl
    def set_start_date(self):
        if self.status == 'offen':
            if self._try_number == 1:
                self.start_date = date.today()
            elif self._try_number == 2:
                self._start_date_2 = date.today()
            elif self._try_number == 3:
                self._start_date_3 = date.today()
        elif self.status == 'pausiert':
            pause = date.today() - self._pause_start  # Berechnung der Pausendauer
            self._pause_total += pause
        else:
            raise ValueError('Status can not be changed to "aktiv" if it is not "offen".')

    # Setzt das Enddatum, wenn die Bedingungen zwischen Statusänderungen erfüllt sind
    def set_end_date(self, new_status):
        current_status = self.status
        if not (current_status == 'Bewertung ausstehend' and new_status == 'abgeschlossen'):
            if self.end_date == 'KA':
                self.end_date = date.today()
            elif self._end_date_2 == 'KA':
                self._end_date_2 = date.today()
            elif self._end_date_3 == 'KA':
                self._end_date_3 = date.today()

    # Berechnet die Gesamtdauer basierend auf Start-, Enddatum und Pausen
    @property
    def duration(self):
        if self.status == 'abgeschlossen':
            total_duration = self.end_date - self.start_date
            if self._start_date_2 != 'KA':
                total_duration += (self._end_date_2 - self._start_date_2)
            if self._start_date_3 != 'KA':
                total_duration += (self._end_date_3 - self._start_date_3)
            return total_duration - self._pause_total
        else:
            return 'KA'

    # Getter für Elemente, gibt immer eine leere Liste zurück
    @property
    def elements(self):
        return []
    
    # Setter für Elemente, gibt Hinweis aus, dass Elemente nicht unterstützt werden
    @elements.setter
    def elements(self, new_elements):
        print('Courses do not contain any elements.')
    
    # Getter für das Startdatum, kapselt den direkten Zugriff auf das Attribut
    @property
    def start_date(self):
        return self._start_date

    # Setter für das Startdatum, prüft Eingabe und sichert Datenintegrität
    @start_date.setter
    def start_date(self, new_start_date):
        if isinstance(new_start_date, tuple):
            new_start_date, init = new_start_date
        else:
            init = False
        if new_start_date == self.start_date:
            print(f'Start_date is already set to {new_start_date}.')
        elif new_start_date == 'KA':     # Reset aller relevanten Attribute
            self._start_date = 'KA'
            self._end_date = 'KA'
            self._start_date_2 = 'KA'
            self._end_date_2 = 'KA'
            self._start_date_3 = 'KA'
            self._end_date_3 = 'KA'
            self._status = 'offen'
            self._grade = 'KA'
            self._try_number = 1
            self._pause_start = 'KA'
            self._pause_total = timedelta()
        else:
            if not isinstance(new_start_date, date):
                raise ValueError('Start_date must be a date.')
            elif new_start_date > date.today():
                raise ValueError('Dates can not be a future date.')
            elif self.end_date != 'KA' and new_start_date > self.end_date:
                raise ValueError('Start_date must be bevore end_date.')
            if not init:
                if self.status not in ['aktiv', 'pausiert'] and self.end_date == 'KA':
                    if self.mentor == 'KA':
                        self.mentor = input(f'Welche*r Tutor*in ist für den Kurs "{self.name}" verantwortlich?')
                    self.choose_active_course()
            self._start_date = new_start_date

    # end_date getter und setter
    @property
    def end_date(self):
        return self._end_date  # Zugriff auf das private Attribut _end_date

    @end_date.setter
    def end_date(self, new_end_date):
        if isinstance(new_end_date, tuple):  # Überprüfung, ob new_end_date ein Tupel ist
            new_end_date, init = new_end_date
        else:
            init = False  # Flag, ob der Wert initialisiert wurde
        if new_end_date == self.end_date:
            print(f'End_date is already set to {new_end_date}.')  # Vermeidung doppelter Zuweisungen
        elif new_end_date == 'KA':  # Spezialwert 'KA' wird behandelt
            self._end_date = 'KA'
            self._start_date_2 = 'KA'
            self._end_date_2 = 'KA'
            self._start_date_3 = 'KA'
            self._end_date_3 = 'KA'
            self._grade = 'KA'
            self._try_number = 1
            self.choose_active_course()  # Methode zur Kursauswahl aufrufen
        else:
            if not isinstance(new_end_date, date):  # Typprüfung für das Datum
                raise ValueError('End_date must be a date.')
            elif new_end_date > date.today():  # Verhindert zukünftige Daten
                raise ValueError('Dates can not be a future date.')
            if self.start_date_2 != 'KA':
                if  new_end_date > self.start_date_2:  # Validierung der Reihenfolge der Daten
                    raise ValueError('End_date must be before start_date_2.')
            if self.start_date == 'KA':  # Initialisierung des Startdatums bei Bedarf
                print(f'Wann wurde der erste Versuch vom Kurs "{self.name}" gestartet?')
                self.start_date = (self.create_date(), True)
            if self.start_date > new_end_date:  # Validierung der zeitlichen Reihenfolge
                    raise ValueError('End_date must be after start_date.')
            if not init and self.status not in ['Bewertung ausstehend', 'abgeschlossen']:  # Statusprüfung
                if self.try_number == 1:
                    answer = input(f'Wurde der Kurs bereits benotet? (J/N)')
                if answer not in ['J', 'N']:  # Validierung der Benotungsantwort
                    raise ValueError('Answer must be J (Yes) or N (No).')
                elif answer == 'J':
                    self.status = 'abgeschlossen'  # Statusänderung bei Benotung
                elif answer == 'N':
                    self.status = 'Bewertung ausstehend'
            self._end_date = new_end_date  # Zuweisung des Enddatums

    # start_date_2 getter und setter       
    @property
    def start_date_2(self):
        return self._start_date_2  # Zugriff auf das private Attribut _start_date_2

    @start_date_2.setter
    def start_date_2(self, new_start_date_2):
        if isinstance(new_start_date_2, tuple):  # Überprüfung, ob new_start_date_2 ein Tupel ist
            new_start_date_2, init = new_start_date_2
        else:
            init = False
        if new_start_date_2 == self.start_date_2:
            print(f'Start_date_2 is already set to {new_start_date_2}.')  # Vermeidung doppelter Zuweisungen
        elif new_start_date_2 == 'KA':  # Spezialwert 'KA' wird behandelt
            self._start_date_2 = 'KA'
            self._end_date_2 = 'KA'
            self._start_date_3 = 'KA'
            self._end_date_3 = 'KA'
            self._status = 'offen'
            self._grade = 5
            self._try_number = 2
        else:
            if not isinstance(new_start_date_2, date):  # Typprüfung für das Datum
                raise ValueError('Start_date_2 must be a date.')
            elif new_start_date_2 > date.today():  # Verhindert zukünftige Daten
                raise ValueError('Dates can not be a future date.')
            if self.end_date_2 != 'KA':
                if new_start_date_2 > self.end_date_2:  # Validierung der Reihenfolge der Daten
                    raise ValueError('Start_date_2 must be bevore end_date_2.')
            if self.start_date == 'KA':  # Initialisierung des Startdatums bei Bedarf
                print(f'Wann wurde der erste Versuch vom Kurs "{self.name}" gestartet?')
                self.start_date = (self.create_date(), True)
            if self.end_date == 'KA':
                print(f'Wann wurde der erste Versuch vom Kurs "{self.name}" abgeschlossen?')
                self.end_date = (self.create_date(), True)
            if new_start_date_2 < self.end_date:
                raise ValueError('Start_date_2 must be after end_date.')  # Validierung der Reihenfolge
            if not init:
                if self.status not in ['aktiv', 'pausiert'] and self.end_date_2 == 'KA':  # Statusprüfung
                    if self.mentor == 'KA':  # Mentor wird bei Bedarf abgefragt
                        self.mentor = input(f'Welche*r Tutor*in ist für den Kurs "{self.name}" verantwortlich?')
                    self.choose_active_course()  # Kursauswahl aufrufen
            if self.try_number == 1:
                self._try_number = 2
            if self.status != 'abgeschlossen':
                self._grade = 5  # Standardnote festlegen
            self._start_date_2 = new_start_date_2  # Zuweisung des Startdatums

    # end_date_2 getter und setter
    @property
    def end_date_2(self):
        return self._end_date_2  # Zugriff auf das private Attribut _end_date_2

    @end_date_2.setter
    def end_date_2(self, new_end_date_2):
        if isinstance(new_end_date_2, tuple):  # Überprüfung, ob new_end_date_2 ein Tupel ist
            new_end_date_2, init = new_end_date_2
        else:
            init = False
        if new_end_date_2 == self.end_date_2:
            print(f'End_date_2 is already set to {new_end_date_2}.')  # Vermeidung doppelter Zuweisungen
        elif new_end_date_2 == 'KA':  # Spezialwert 'KA' wird behandelt
            self._end_date_2 = 'KA'
            self._start_date_3 = 'KA'
            self._end_date_3 = 'KA'
            self._grade = 5
            self._try_number = 2
            self.choose_active_course()  # Methode zur Kursauswahl aufrufen
        else:
            if not isinstance(new_end_date_2, date):  # Typprüfung für das Datum
                raise ValueError('End_date_2 must be a date.')
            elif new_end_date_2 > date.today():  # Verhindert zukünftige Daten
                raise ValueError('Dates can not be a future date.')
            if self.start_date_3 != 'KA':
                if  new_end_date_2 > self.start_date_3:  # Validierung der Reihenfolge der Daten
                    raise ValueError('End_date_2 must be before start_date_3.')
            if self.start_date == 'KA':  # Initialisierung des Startdatums bei Bedarf
                print(f'Wann wurde der erste Versuch vom Kurs "{self.name}" gestartet?')
                self.start_date = (self.create_date(), True)
            if self.end_date == 'KA':
                print(f'Wann wurde der erste Versuch vom Kurs "{self.name}" abgeschlossen?')
                self.end_date = (self.create_date(), True)
            if self.start_date_2 == 'KA':  # Initialisierung des zweiten Startdatums
                print(f'Wann wurde der zweite Versuch vom Kurs "{self.name}" gestartet?')
                self.start_date_2 = (self.create_date(), True)
            if self.start_date_2 > new_end_date_2:
                    raise ValueError('End_date_2 must be after start_date_2.')  # Reihenfolge prüfen
            if not init:
                if self.status not in ['aktiv', 'pausiert'] and self.end_date_2 == 'KA':  # Statusprüfung
                    if self.mentor == 'KA':  # Mentor wird bei Bedarf abgefragt
                        self.mentor = input(f'Welche*r Tutor*in ist für den Kurs "{self.name}" verantwortlich?')
                    self.choose_active_course()  # Kursauswahl aufrufen
            if self.try_number == 1:
                self._try_number = 2
            if self.status != 'abgeschlossen':
                self._grade = 5  # Standardnote festlegen
            self._end_date_2 = new_end_date_2  # Zuweisung des Enddatums

    # start_date_3 getter und setter
    @property
    def start_date_3(self):
        return self._start_date_3  # Zugriff auf das private Attribut _start_date_3

    @start_date_3.setter
    def start_date_3(self, new_start_date_3):
        if isinstance(new_start_date_3, tuple):  # Überprüfung, ob new_start_date_3 ein Tupel ist
            new_start_date_3, init = new_start_date_3
        else:
            init = False
        if new_start_date_3 == self.start_date_3:
            print(f'Start_date_3 is already set to {new_start_date_3}.')  # Vermeidung doppelter Zuweisungen
        elif new_start_date_3 == 'KA':  # Spezialwert 'KA' wird behandelt
            self._start_date_3 = 'KA'
            self._end_date_3 = 'KA'
            self._status = 'offen'
            self._grade = 5
            self._try_number = 3
        else:
            if not isinstance(new_start_date_3, date):  # Typprüfung für das Datum
                raise ValueError('Start_date_3 must be a date.')
            elif new_start_date_3 > date.today():  # Verhindert zukünftige Daten
                raise ValueError('Dates can not be a future date.')
            if self.end_date_3 != 'KA':
                if new_start_date_3 > self.end_date_3:  # Validierung der Reihenfolge der Daten
                    raise ValueError('Start_date_3 must be bevore end_date_3.')
            if self.start_date == 'KA':  # Initialisierung des Startdatums bei Bedarf
                print(f'Wann wurde der erste Versuch vom Kurs "{self.name}" gestartet?')
                self.start_date = (self.create_date(), True)
            if self.end_date == 'KA':
                print(f'Wann wurde der erste Versuch vom Kurs "{self.name}" abgeschlossen?')
                self.end_date = (self.create_date(), True)
            if self.start_date_2 == 'KA':  # Initialisierung des zweiten Startdatums
                print(f'Wann wurde der zweite Versuch vom Kurs "{self.name}" gestartet?')
                self.start_date_2 = (self.create_date(), True)
            if self.end_date_2 == 'KA':  # Initialisierung des zweiten Enddatums
                print(f'Wann wurde der zweite Versuch vom Kurs "{self.name}" abgeschlossen?')
                self.end_date_2 = (self.create_date(), True)
            if new_start_date_3 < self.end_date_2:
                raise ValueError('Start_date_3 must be after end_date_2.')  # Validierung der Reihenfolge
            if not init:
                if self.status not in ['aktiv', 'pausiert'] and self.end_date_3 == 'KA':  # Statusprüfung
                    if self.mentor == 'KA':  # Mentor wird bei Bedarf abgefragt
                        self.mentor = input(f'Welche*r Tutor*in ist für den Kurs "{self.name}" verantwortlich?')
                    self.choose_active_course()  # Kursauswahl aufrufen
            if self.try_number != 3:
                self._try_number = 3  # Versuchszähler anpassen
            if self.status != 'abgeschlossen':
                self._grade = 5  # Standardnote festlegen
            self._start_date_3 = new_start_date_3  # Zuweisung des Startdatums

    # end_date_3 getter und setter 
    @property
    def end_date_3(self):
        return self._end_date_3  # Zugriff auf das private Attribut _end_date_3

    @end_date_3.setter
    def end_date_3(self, new_end_date_3):
        if new_end_date_3 == self.end_date_3:
            print(f'End_date_3 is already set to {new_end_date_3}.')  # Vermeidung doppelter Zuweisungen
        elif new_end_date_3 == 'KA':  # Spezialwert 'KA' wird behandelt
            self._end_date_3 = 'KA'
            self._grade = 5
            self._try_number = 3
            self.choose_active_course()  # Methode zur Kursauswahl aufrufen
        else:
            if not isinstance(new_end_date_3, date):  # Typprüfung für das Datum
                raise ValueError('End_date_3 must be a date.')
            elif new_end_date_3 > date.today():  # Verhindert zukünftige Daten
                raise ValueError('Dates can not be a future date.')
            if self.start_date == 'KA':  # Initialisierung des Startdatums bei Bedarf
                print(f'Wann wurde der erste Versuch vom Kurs "{self.name}" gestartet?')
                self.start_date = (self.create_date(), True)
            if self.end_date == 'KA':
                print(f'Wann wurde der erste Versuch vom Kurs "{self.name}" abgeschlossen?')
                self.end_date = (self.create_date(), True)
            if self.start_date_2 == 'KA':  # Initialisierung des zweiten Startdatums
                print(f'Wann wurde der zweite Versuch vom Kurs "{self.name}" gestartet?')
                self.start_date_2 = (self.create_date(), True)
            if self.end_date_2 == 'KA':  # Initialisierung des zweiten Enddatums
                print(f'Wann wurde der zweite Versuch vom Kurs "{self.name}" abgeschlossen?')
                self.end_date_2 = (self.create_date(), True)
            if self.start_date_3 == 'KA':  # Initialisierung des dritten Startdatums
                print(f'Wann wurde der dritte Versuch vom Kurs "{self.name}" gestartet?')
                self.start_date_3 = (self.create_date(), True)
            if self.start_date_3 > new_end_date_3:
                    raise ValueError('End_date_3 must be after start_date_3.')  # Validierung der Reihenfolge
            if self.status not in ['Bewertung ausstehend', 'abgeschlossen']:  # Statusprüfung
                answer = input(f'Wurde der Kurs bereits benotet? (J/N)')
                if answer not in ['J', 'N']:  # Antwortvalidierung
                    raise ValueError('Answer must be J (Yes) or N (No).')
                elif answer == 'J':
                    self.status = 'abgeschlossen'  # Statusänderung bei Benotung
                elif answer == 'N':
                    self.status = 'Bewertung ausstehend'
            if self.status != 'abgeschlossen':
                self._grade = 5  # Standardnote festlegen
                if self.status != 'Bewertung ausstehend':
                    self.exmatriculate()  # Exmatrikulation bei Bedarf
            self._end_date_3 = new_end_date_3  # Zuweisung des Enddatums


    # pause_start getter und setter
    @property
    def pause_start(self):
        return self._pause_start  # Zugriff auf das private Attribut _pause_start
    
    @pause_start.setter
    def pause_start(self, new_pause_start):
        # Überprüfen, ob der Wert vom Typ 'date' ist
        if not isinstance(new_pause_start, date):
            raise ValueError('Pause_start must be a date.')
        # Sicherstellen, dass der Wert nicht in der Zukunft liegt
        elif new_pause_start > date.today():
            raise ValueError('Dates can not be a future date.')
        # Nur für aktive oder pausierte Kurse zulässig
        elif self.status not in ['aktiv', 'pausiert']:
                raise ValueError('Pause_start can only be set for active or paused courses.')
        # Überprüfen der Bedingungen für den Pausebeginn je nach Versuchsnummer
        elif self._try_number == 3:
            if new_pause_start < self._start_date_3:
                raise ValueError('Pause_start can not be before recent start date (start_date_3).')
        elif self._try_number == 2:
            if new_pause_start < self._start_date_2:
                raise ValueError('Pause_start can not be before recent start date (start_date_2).')
        elif new_pause_start < self.start_date:
            raise ValueError('Pause_start can not be before recent start date (start_date).')
        # Pausieren des Kurses, wenn der Status aktiv ist
        if self.status == 'aktiv':
            self.pause_course()
        self._pause_start = new_pause_start

    # pause_total getter und setter
    @property
    def pause_total(self):
        return self._pause_total  # Zugriff auf das private Attribut _pause_total
    
    @pause_total.setter
    def pause_total(self, new_pause_total):
        # Überprüfen, ob der Wert vom Typ 'timedelta' ist
        if not isinstance(new_pause_total, timedelta):
            raise ValueError('Pause_total must be a timedate.')
        # Sicherstellen, dass die Pausendauer positiv ist
        elif new_pause_total < timedelta():
            raise ValueError('Pause_total must be greater than 0.')
        else:
            self._pause_total = new_pause_total  # Setzen der Pausendauer

    # Getter für status
    @property
    def status(self):
        return self._status  # Zugriff auf das private Attribut _status

    # Setter für Status
    @status.setter
    def status(self, new_status):
        # Überprüfen, ob der Status gültig ist
        if new_status not in StudyElement.possible_statuses:
            raise ValueError('Status must be "offen", "aktiv", "Bewertung ausstehend" oder "abgeschlossen".')
        # Verhindern, dass der Status unverändert bleibt
        if new_status == self.status:
            raise ValueError(f'Status already is {new_status}.')
        # Aktionen je nach Statuswechsel (beenden, starten, pausieren)
        if new_status in ['Bewertung ausstehend', 'abgeschlossen']:
            if new_status == 'abgeschlossen':
                self.grade = float(input(f'Mit welcher Note wurde der Kurs "{self.name}" abgeschlossen?'))
            self.set_end_date(new_status)
            self._status = new_status
            self.start_next_course()
        elif new_status == 'aktiv':
            self.set_start_date()
            if self.mentor == 'KA':
                self.mentor = input(f'Welche*r Tutor*in ist für den Kurs "{self.name}" verantwortlich?')
            self.choose_active_course()
        elif new_status == 'pausiert':
            self.pause_course(False)
        else:
            raise ValueError('Status can not be returned to "offen".')

    # id getter und setter
    @property
    def id(self):
        return self._id  # Zugriff auf das private Attribut _id
    
    @id.setter
    def id(self, new_id):
        # Überprüfen, ob die ID eine Zeichenkette ist
        if not isinstance(new_id, str):
            raise ValueError('ID must be a string.')
        self._id = new_id  # Setzen der ID

    # mentor getter und setter
    @property
    def mentor(self):
        return self._mentor  # Zugriff auf das private Attribut _mentor
    
    @mentor.setter
    def mentor(self, new_mentor):
        # Überprüfen, ob der Mentor eine Zeichenkette ist
        if not isinstance(new_mentor, str):
            raise ValueError('Mentor must be a string.')
        self._mentor = new_mentor  # Setzen des Mentors

    # exam getter und setter
    @property
    def exam(self):
        return self._exam  # Zugriff auf das private Attribut _exam
    
    @exam.setter
    def exam(self, new_exam):
        # Überprüfen, ob die Prüfung vom richtigen Typ ist
        if new_exam not in Course.exam_types:
            raise ValueError(f'Exam must be one of: {", ".join(Course.exam_types)}.')

    #grade getter und setter
    @property
    def grade(self):
        if self._grade != 'KA':
            return Decimal(str(self._grade)).quantize(Decimal('0.1'), rounding=ROUND_UP)  # Notenwert auf eine Dezimalstelle runden
        else:
            return 'KA'
    
    @grade.setter
    def grade(self, new_grade):
        # Überprüfen, ob die Note gültig ist
        if not isinstance(new_grade, (float, int)) and new_grade != 'KA':
            raise ValueError('Grade must be a float or integer between 1 and 4, 5 or "KA".')
        elif new_grade != 'KA':
            # Gültigkeitsprüfung der Notenwerte
            if not (1 <= new_grade <= 4) and new_grade != 5:
                raise ValueError('Grade must be a float or integer between 1 and 4, 5 or "KA".')
            elif new_grade == 5:
                # Anpassen des Versuchszählers bei der Note 5
                if self._try_number < 3:
                    self._try_number += 1
                else:
                    self.exmatriculate()  # Exmatrikulation bei Überschreiten der Versuche
                self._status = 'offen'
            else:
                self._status = 'abgeschlossen'
            self._grade = f'{round(new_grade, 1):.1f}'  # Runden und Setzen der Note
        else:
            self._grade = 'KA'  # Setzen von "KA" (Keine Angabe)

    # try_number getter und setter
    @property
    def try_number(self):
        return self._try_number  # Zugriff auf das private Attribut _try_number
    
    @try_number.setter
    def try_number(self, new_try_number):
        # Überprüfen, ob die Versuchsnummer gültig ist
        if new_try_number not in [1, 2, 3]:
            raise ValueError('Try_number must be 1, 2, or 3.')
        elif new_try_number == self.try_number:
            print(f'Try_number is already set to "{new_try_number}".')
        elif new_try_number < self.try_number:
            # Zurücksetzen von Daten bei der Rücksetzung der Versuchsnummer
            self._start_date_3 = 'KA'
            self._end_date_3 = 'KA'
            if self.status not in ['Bewertung ausstehend', 'abgeschlossen'] or new_try_number == 1:
                self._end_date_2 = 'KA'
            if self.status == 'offen' or new_try_number == 1:
                self._start_date_2 = 'KA'
            if new_try_number == 1:
                if self.status not in ['Bewertung ausstehend', 'abgeschlossen']:
                    self._end_date = 'KA'
                if self.status != 'abgeschlossen':
                    self._grade = 'KA'
                if self.status == 'offen':
                    self._start_date = 'KA'
            self._try_number = new_try_number
        elif new_try_number > self.try_number:
            # Datum und Status anpassen, wenn Versuche erhöht werden
            if self.start_date == 'KA':
                print(f'Wann wurde der erste Versuch vom Kurs "{self.name}" gestartet?')
                self.start_date = (self.create_date(), True)
            if self.end_date == 'KA':
                print(f'Wann wurde der erste Versuch vom Kurs "{self.name}" abgeschlossen?')
                self.end_date = (self.create_date(), True)
            if (self.status != 'offen' or new_try_number == 3) and self.start_date_2 == 'KA':
                print(f'Wann wurde der zweite Versuch vom Kurs "{self.name}" gestartet?')
                self.start_date_2 = (self.create_date(), True)            
            if (self.status in ['Bewertung ausstehend', 'abgeschlossen'] or new_try_number == 3) and self.end_date_2 == 'KA':
                print(f'Wann wurde der zweite Versuch vom Kurs "{self.name}" abgeschlossen?')
                self.end_date_2 = (self.create_date(), True)
            if self.status != 'offen' and new_try_number == 3:
                print(f'Wann wurde der dritte Versuch vom Kurs "{self.name}" gestartet?')
                self.start_date_3 = (self.create_date(), True)
            if self.status in ['Bewertung ausstehend', 'abgeschlossen'] and new_try_number == 3:
                print(f'Wann wurde der dritte Versuch vom Kurs "{self.name}" abgeschlossen?')
                self.end_date_3 = self.create_date() 
            # Note anpassen und Status setzen
            if self.status != 'abgeschlossen' and new_try_number > 1:
                self._grade = 5
            self._try_number = new_try_number

    #Exmatrikulation bei Scheitern des dritten Versuches
    def exmatriculate(self):
        # Nutzer wird informiert und der Prozess wird gestoppt
        print(f'Der Kurs {self.name} wurde beim dritten Versuch nicht bestanden. Du wirst somit exmatrikuliert. Bei Rückfragen wende dich bitte an die IU - Internationale Hochschule.')
        quit()  # Beendet das Programm