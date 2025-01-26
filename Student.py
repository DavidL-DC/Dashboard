from Studiengang import CourseOfStudies  # Importieren der Klasse CourseOfStudies, die für den Studiengang zuständig ist
from datetime import date, timedelta  # Importieren von Modulen für Datum und Zeit
from dateutil.relativedelta import relativedelta  # Importieren für die Berechnung relativer Zeiträume
from typing import Union  # Union wird für die Angabe mehrerer zulässiger Typen verwendet
from decimal import Decimal, ROUND_UP  # Importieren von Decimal für präzise Berechnungen

# Definition der Klasse Student
class Student:
    def __init__(self, name: str, student_number: int, course_of_studies: CourseOfStudies, enrollment_date: date, monthly_tuition_fee: Union[float, int]):
        # Überprüfen, ob die Eingabewerte gültig sind
        if not isinstance(name, str):
            raise ValueError('Name must be a string.')
        if not isinstance(student_number, int):
            raise ValueError('Student_number must be an integer.')
        if not isinstance(course_of_studies, CourseOfStudies):
            raise ValueError('Course_of_studies must be a CourseOfStudies element.')
        if not isinstance(enrollment_date, date):
            raise ValueError('Enrollment_date must be a date.')
        if not isinstance(monthly_tuition_fee, (float, int)):
            raise ValueError('Monthly_tuition_fee must be a float or an integer.')

        # Initialisierung der Instanzvariablen
        self._name = name
        self._student_number = student_number
        self._course_of_studies = course_of_studies
        self._enrollment_date = enrollment_date
        self._monthly_tuition_fee = Decimal(str(monthly_tuition_fee)).quantize(Decimal('0.01'), rounding=ROUND_UP)

    # Getter und Setter für die Attribute: name, student_number, course_of_studies, enrollment_date, monthly_tuition_fee
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        if not isinstance(new_name, str):
            raise ValueError('Name must be a string.')
        else:
            self._name = new_name

    @property
    def student_number(self):
        return self._student_number
    
    @student_number.setter
    def student_number(self, new_student_number):
        if not isinstance(new_student_number, int):
            raise ValueError('Student_number must be an integer.')
        else:
            self._student_number = new_student_number

    @property
    def course_of_studies(self):
        return self._course_of_studies
    
    @course_of_studies.setter
    def course_of_studies(self, new_course_of_studies):
        if not isinstance(new_course_of_studies, CourseOfStudies):
            raise ValueError('Course_of_studies must be a CourseOfStudies element.')
        else:
            self._course_of_studies = new_course_of_studies

    @property
    def enrollment_date(self):
        return self._enrollment_date
    
    @enrollment_date.setter
    def enrollment_date(self, new_enrollment_date):
        if not isinstance(new_enrollment_date, date):
            raise ValueError('Enrollment_date must be a date.')
        else:
            self._enrollment_date = new_enrollment_date

    @property
    def monthly_tuition_fee(self):
        return self._monthly_tuition_fee
    
    @monthly_tuition_fee.setter
    def monthly_tuition_fee(self, new_monthly_tuition_fee):
        if not isinstance(new_monthly_tuition_fee, (float, int)):
            raise ValueError('Monthly_tuition_fee must be a float or an integer.')
        else:
            self._monthly_tuition_fee = Decimal(str(new_monthly_tuition_fee)).quantize(Decimal('0.01'), rounding=ROUND_UP)

    # Berechnung der Anzahl aktiver Kurse
    @property
    def active_courses(self):
        return len([course for semester in self.course_of_studies.elements
                    for module in semester.elements
                    for course in module.elements
                    if course.status == 'aktiv'])

    # Berechnung des bezahlten Studienbeitrags
    @property
    def contribution_paid(self):
        studied_time = relativedelta(date.today(), self.enrollment_date)
        studied_months = studied_time.years * 12 + studied_time.months
        return Decimal(str(studied_months * float(self.monthly_tuition_fee))).quantize(Decimal('0.01'), rounding=ROUND_UP)

    # Berechnung der geschätzten Studiendauer
    @property
    def estimated_study_duration(self):
        finished_courses_ect = sum(course.ect for semester in self.course_of_studies.elements
                                    for module in semester.elements
                                    for course in module.elements
                                    if course.status == 'abgeschlossen')
        studied_time = date.today() - self.enrollment_date
        studied_years = studied_time.days / 365.25
        if finished_courses_ect:
            estimated_duration = (self.course_of_studies.ect / finished_courses_ect) * studied_years
            return Decimal(str(estimated_duration)).quantize(Decimal('0.1'), rounding=ROUND_UP).normalize()
        else:
            return Decimal(str((self.course_of_studies.ect / 60))).quantize(Decimal('0.1'), rounding=ROUND_UP).normalize()

    # Berechnung des Notendurchschnitts
    @property
    def grade_average(self):
        all_grades = [course.grade for semester in self.course_of_studies.elements
                        for module in semester.elements
                        for course in module.elements
                        if course.status == 'abgeschlossen']
        if all_grades:
            average = sum(all_grades) / len(all_grades)
            return Decimal(str(average)).quantize(Decimal('0.01'), rounding=ROUND_UP)
        else:
            return 'KA'  # Kein Durchschnitt, falls keine Kurse abgeschlossen sind

    # Auflistung der ausstehenden Bewertungen mit Fälligkeitsdatum
    @property
    def outstanding_grades(self):
        outstanding_grade_courses = [course for semester in self.course_of_studies.elements
                                        for module in semester.elements
                                        for course in module.elements
                                        if course.status == 'Bewertung ausstehend']
        if outstanding_grade_courses:
            course_date_couples = [(course.name, self.grading_period(course)) for course in outstanding_grade_courses]
            return course_date_couples
        else:
            return 'KA'

    # Berechnung der Korrekturfrist für ausstehende Bewertungen
    def grading_period(self, course):
        if course.try_number == 1:
            end_date = course.end_date
        elif course.try_number == 2:
            end_date = course.end_date_2
        else:
            end_date = course.end_date_3
        year = end_date.year
        month = end_date.month + 1
        if month == 13:
            month = 1
            year += 1
        return date(year, month, 1) + timedelta(42)

    # Notenübersicht
    @property
    def grade_overview(self):
        finished_courses = [course for semester in self.course_of_studies.elements
                                        for module in semester.elements
                                        for course in module.elements
                                        if course.status == 'abgeschlossen']
        if finished_courses:
            course_grade_couples = [(course.name, course.grade) for course in finished_courses]
            course_grade_couples.reverse()
            return course_grade_couples
        else:
            return 'KA'

    # Dauer der abgeschlossenen Kurse
    @property
    def finished_courses_duration(self):
        finished_courses = [course for semester in self.course_of_studies.elements
                        for module in semester.elements
                        for course in module.elements
                        if course.status == 'abgeschlossen']
        if finished_courses:
            course_duration_couples = [(course.name, course.duration) for course in finished_courses]
            course_duration_couples.reverse()
            return course_duration_couples
        else:
            return 'KA'