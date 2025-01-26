import tkinter as tk    # Importieren von Tkinter zur Erstellung einer Benutzeroberfläche
import customtkinter as ctk    # Importieren von CustomTkinter zur Gestaltung des geplanten Designs
import pyglet       # Importieren von Pyglet zur Nutzung externer Schriftarten
from matplotlib import colors  # Importieren von Matplotlib für Farbmanipulation
from datetime import date   # Importieren von Datetime zum abrufen aktueller Daten
from Beispieldaten import student, grade_goal, revenue_goal, active_courses_goal, study_duration_goal   # Importieren des Student-Objekts und der Hauptziele aus den Beispieldaten
from decimal import Decimal, ROUND_UP, ROUND_DOWN   # Importieren von Decimal zur Formatierung bestimmter Zahlen
import pywinstyles      # Importieren von Pywinstyles um Hintergründe von Widgets zu entfernen

# Quicksand als externe Schriftart hinzufügen
pyglet.font.add_file('quicksand-regular.ttf')
pyglet.font.add_file('quicksand-medium.ttf')

# Farbcode basierend auf dem Fortschritt berechnen, ähnlich wie in Ziel.py
def choose_color(percent):
    # Definiert die Farbpalette (rot, gelb, grün)
    base_colors = ['#FF817A', '#FFFE7A', '#7FFF7A']
    cmap = colors.LinearSegmentedColormap.from_list('cmap', base_colors)  # Erzeugt ein Farbschema basierend auf den Basisfarben
    norm = colors.Normalize(vmin=0, vmax=100)  # Normalisiert den Fortschritt, um ihn auf den Bereich von 0 bis 100 zu bringen
    color = cmap(norm(percent))  # Berechnet die Farbe basierend auf dem FProzentwert
    return colors.rgb2hex(color)  # Wandelt die RGB-Farbe in den Hex-Code um

# Zeichnen des Farbverlaufs
def draw_gradient(canvas, width, height):
    # Festlegen, wie viele Pixel am Rand eine feste Farbe haben sollen
    border = 10
    # Die ersten Pixel in Rot
    color = choose_color(0)
    for i in range(border):
        canvas.create_line(i, 0, i, height, fill=color)     # Zeichnet eine 1 Pixel dicke Linie senkrecht auf das Canvas
    # Alle Pixel, außer den ersten und letzten 10 bilden einen Farbverlauf
    for i in range(width-border*2):      # Für jedes Pixel in der Breite des Canvas wird eine Linie gezeichnet
        percent = (i + 1) / ((width-border*2) / 100)     # Berechnet die Prozent der gesamte Breite
        color = choose_color(percent)     # Bestimmt die Farbe der Linie anhand der Prozent
        canvas.create_line(i+border, 0, i+border, height, fill=color)     # Zeichnet eine 1 Pixel dicke Linie senkrecht auf das Canvas
    # Die letzten Pixel in Grün
    color = choose_color(100)
    for i in range(border):
        canvas.create_line(i+border+(width-border*2), 0, i+border+(width-border*2), height, fill=color)     # Zeichnet eine 1 Pixel dicke Linie senkrecht auf das Canvas

# Datum formatieren
def format_date(date):
    weekdays = {0:'Montag', 1:'Dienstag', 2:'Mittwoch', 3:'Donnerstag', 4:'Freitag', 5:'Samstag', 6:'Sonntag'}  # Dictionary für alle Wochentage in deutscher Sprache erstellen
    formated_current_date = date.strftime('%d.%m.%Y')    # Datum in gewünschte Schreibweise formatieren
    current_weekday = date.weekday()    # Heutigen Wochentag abfragen
    german_weekday = weekdays[current_weekday]  # Integer in deutschen Wochentag umwandeln
    date_text = f'{german_weekday}, {formated_current_date}'
    return date_text

# Anpassen der Größe des runden Elements in der Mitte
def update_circle():
    frame_width = middle_frame.winfo_width()    # Ermitteln der Breite des mittleren Frames
    gavg_colored_frame.configure(width=frame_width, height=frame_width, corner_radius=frame_width / 2)  # Maße werden so berechnet, dass das Element als Kreis immer den gesamten Platz des mittleren Frames ausnutzt
    inner_width = frame_width-25
    gavg_inner_frame.configure(width=inner_width, height=inner_width, corner_radius=inner_width / 2)

# Position des Datum- und des Indikator-Widgets anhand der Größe des Fensters berechnen
def widget_positions(event):
    width = root.winfo_width()    # Reagieren auf Veränderungen der Breite des Fensters
    height = root.winfo_height()    # Reagieren auf Veränderungen der Höhe des Fensters
    date_label.place(x=width - 210, y=5)    # Das Date wird immer in der oberen rechten Ecke angezeigt
    indicator_frame.place(x=20, y=height - 43)    # Der Indikator wird immer in der unteren linken Ecke angezeigt
    update_circle()     # Die Maße des Kreiselements anpassen

# Funktion zur Erstellung einzelner Label für vergangene Kurse und ihre Dauer
def show_finished_courses():
    # Wenn es abgeschlossene Kurse gibt
    if student.finished_courses_duration != 'KA':
        # Für jeden Kurs in den abgeschlossenen Kursen
        for course, duration in student.finished_courses_duration:
            course_frame = tk.Frame(cd_text_frame, bg='white')      # Einen Frame für den Kurs und die Dauer erstellen
            course_label = tk.Label(course_frame, text=course, font=('quicksand', 10), bg='white', justify='left', wraplength=150)      # Den Titel des Kurses als ein Label definieren, linksbündig mit Umbrüchen falls nötig
            course_label.pack(side='left', padx=2)      # Das Label links im Frame platzieren
            weeks = Decimal(str(duration.days / 7)).quantize(Decimal('0.1'), rounding=ROUND_DOWN) if int(((duration.days / 7) * 10) % 10) == 5 else Decimal(str(duration.days / 7)).quantize(Decimal('1'), rounding=ROUND_UP)       # Die Anzahl an Wochen der Kursdauer berechnen -> Es werden nur ganze oder halbe Wochen angegeben 
            duration_label = tk.Label(course_frame, text=f' {weeks} {'Woche' if weeks == 1 else 'Wochen'}', font=('quicksand', 10), bg='white', fg='#93a0d8')  # Ein Label für die Dauer des Kurses in Wochen definieren, rechtsbündig
            duration_label.pack(side='right', padx=2, anchor='n')   # Das Label rechts im Frame platzieren
            course_frame.pack(fill='x')     # Den gesamten Frame im cd_text_frame platzieren
    # Wenn es keine abgeschlossenen Kurse gibt
    else:
        label = tk.Label(cd_text_frame, text='Es wurden noch keine Kurse abgeschlossen.', font=('quicksand', 10), bg='white', wraplength=200)
        label.pack(pady=30)

# Funktion zur Erstellung einzelner Label für ausstehende Bewertungen und ihre Fälligkeit
def show_pending_grades():
    # Wenn es ausstehende Bewertungen gibt
    if student.outstanding_grades != 'KA':
        # Für jeden Kurs in den ausstehenden Bewertungen
        for course, date in student.outstanding_grades:
            course_frame = tk.Frame(pg_text_frame, bg='white')      # Einen Frame für den Kurs und das Fälligkeitsdatum erstellen
            course_label = tk.Label(course_frame, text=course, font=('quicksand', 10), bg='white', justify='left', wraplength=150)      # Den Titel des Kurses als ein Label definieren, linksbündig mit Umbrüchen falls nötig
            course_label.pack(side='left', padx=2)      # Das Label links im Frame platzieren
            date_label = tk.Label(course_frame, text=format_date(date), font=('quicksand', 10), bg='white', fg='#93a0d8', wraplength=100)  # Ein Label für das Fälligkeitsdatum der Bewertung, rechtsbündig mit Umbrüchen falls nötig
            date_label.pack(side='right', padx=2, anchor='n')   # Das Label rechts im Frame platzieren
            course_frame.pack(fill='x')     # Den gesamten Frame im pg_text_frame platzieren
    # Wenn es keine ausstehenden Bewertungen gibt
    else:
        label = tk.Label(pg_text_frame, text='Es stehen aktuell keine Bewertungen aus.', font=('quicksand', 10), bg='white', wraplength=200)
        label.pack(pady=30)

# Funktion zur Erstellung einzelner Label für erreichte Bewertungen abgeschlossener Kurse
def show_grades():
    # Wenn es abgeschlossene Kurse gibt
    if student.grade_overview != 'KA':
        # Für jeden Kurs in den abgeschlossenen Kursen
        for course, grade in student.grade_overview:
            course_frame = tk.Frame(go_text_frame, bg='white')      # Einen Frame für den Kurs und die Note erstellen
            course_label = tk.Label(course_frame, text=course, font=('quicksand', 10), bg='white', justify='left', wraplength=150)      # Den Titel des Kurses als ein Label definieren, linksbündig mit Umbrüchen falls nötig
            course_label.pack(side='left', padx=2)      # Das Label links im Frame platzieren
            date_label = tk.Label(course_frame, text=grade, font=('quicksand', 10), bg='white', fg='#93a0d8', wraplength=100)  # Ein Label für die Bewertung, rechtsbündig
            date_label.pack(side='right', padx=2, anchor='n')   # Das Label rechts im Frame platzieren
            course_frame.pack(fill='x')     # Den gesamten Frame im go_frame platzieren
    # Wenn es keine abgeschlossenen Kurse gibt
    else:
        label = tk.Label(go_text_frame, text='Es gibt noch keine Bewertungen.', font=('quicksand', 10), bg='white', wraplength=200)
        label.pack(pady=30)

# Einkerbung an mittleren, oberen Widget zeichnen
def draw_upper_canvas():
    width = middle_frame.winfo_width()  # Breite des mittleren Frames auslesen
    upper_canvas.configure(width=width)       # Breite auf Breite des mittleren Frames setzen
    for i in range(2):                  # 2 Pixel breiten Rand an Anfang des Canvas zeichnen
        upper_canvas.create_line(i, 0, i, 65, fill='#93a0d8')
    for i in range(2):                  # 2 Pixel breiten Rand an Ende des Canvas zeichnen
        upper_canvas.create_line(width-i-1, 0, width-i-1, 65, fill='#93a0d8')
    upper_canvas.create_arc(0, 10, width, width-70, fill='white', start=180, extent=-180, width=2, outline='#93a0d8', style='arc')    # Große Einkerbung zeichnen
    upper_canvas.create_arc(0, 50, 22, 70, fill='white', start=180, extent=160, width=2, outline='#93a0d8', style='arc')              # Abgerundetes Eck links zeichnen
    upper_canvas.create_arc(width, 50, width-22, 70, fill='white', start=-160, extent=180, width=2, outline='#93a0d8', style='arc')   # Abgerundetes Eck rechts zeichnen

# draw_upper_canvas in gespiegelter Variante für unteres Widget
def draw_lower_canvas():
    width = middle_frame.winfo_width()  
    lower_canvas.configure(width=width)       
    for i in range(2):                  
        lower_canvas.create_line(i, 6, i, 71, fill='#93a0d8')
    for i in range(2):                  
        lower_canvas.create_line(width-i-1, 6, width-i-1, 71, fill='#93a0d8')
    lower_canvas.create_arc(0, 61, width, -width+141, fill='white', start=180, extent=180, width=2, outline='#93a0d8')   
    lower_canvas.create_arc(0, 0, 22, 20, fill='white', start=-180, extent=-160, width=2, outline='#93a0d8', style='arc')             
    lower_canvas.create_arc(width, 0, width-22, 20, fill='white', start=160, extent=-180, width=2, outline='#93a0d8', style='arc') 



# Hauptfenster mit Customtkinter erstellen
root = ctk.CTk(fg_color='white')    # Hintergrundfarbe auf weiß setzen
root.title('Studium-Dashboard')     # Titel festlegen
root.geometry('1300x800')       # Fenstermaße festlegen
root.resizable(False, False)    # Veränderungen in Breite und Höhe verbieten



# Frame für Name und Matrikelnummer hinzufügen, um den Hintergrund zu färben
title_frame = ctk.CTkFrame(root, width=180, height=50, fg_color='#1a1a1a', bg_color='white', corner_radius=10)
title_frame.pack()
# Erzwingen der Größe des Frames
title_frame.pack_propagate(False)

# Erstellen eines Backgroundlabel um die oberen Ecken des Widgets scharf zu gestalten
backgorund_label = tk.Label(title_frame, height=1, width=180, bg='#1a1a1a')
backgorund_label.place(x=0, y=0)

# Name als Label hinzufügen
name_label = tk.Label(title_frame, text=student.name, font=('quicksand', 14, 'bold'), fg='white', bg='#1a1a1a')
name_label.pack()

# Frame für die Matrikelnummer, um die Höhe zu verändern
number_frame = tk.Frame(title_frame, width=172, height=16, bg='#1a1a1a')
number_frame.place(x=1, y=28)
# Erzwingen der Größe des Frames
number_frame.pack_propagate(False)

# Matrikelnummer als Label hinzufügen
number_label = tk.Label(number_frame, text=student.student_number, font=('quicksand', 12), fg='#93a0d8', bg='#1a1a1a')
number_label.pack()



# Datum hinzufügen
date_label = tk.Label(root, text=format_date(date.today()), font=('quicksand', 16), fg='#93a0d8', bg='white')



# Äußerster Frame für alle Ziel-Elemente
outer_frame = tk.Frame(root, bg='white')
outer_frame.pack(fill='both', expand=True, pady=20, padx=100)

# Frame für linke spalte der Ziele
left_frame = tk.Frame(outer_frame, bg='white')
left_frame.pack(side='left', fill='both', expand=True)
left_frame.pack_propagate(False)  # Erzwingen der Größe des Frames

# Frame für mittlere spalte der Ziele
middle_frame = tk.Frame(outer_frame, bg='white')
middle_frame.pack(side='left', padx=100, fill='both', expand=True)
middle_frame.pack_propagate(False)  # Erzwingen der Größe des Frames

# Frame für rechte spalte der Ziele
right_frame = tk.Frame(outer_frame, bg='white')
right_frame.pack(side='left', fill='both', expand=True)
right_frame.pack_propagate(False)  # Erzwingen der Größe des Frames



# Studiendauer im linken Frame hinzufügen
# Frame für Studiendauer
study_duration_frame = ctk.CTkFrame(left_frame, border_width=2, border_color='#93a0d8', bg_color='white', fg_color='white', corner_radius=22)
study_duration_frame.pack(pady=(0, 20), fill='x')

# Abgerundeter Teil des farbigen Indikators
sd_indicator = ctk.CTkFrame(study_duration_frame, height=40, fg_color=study_duration_goal.color, bg_color='#93a0d8', corner_radius=20)    
sd_indicator.pack(fill='x', pady=(2, 0), padx=2)
pywinstyles.set_opacity(sd_indicator, color='#93a0d8')  # Entfernen des Hintergrunds
sd_indicator.pack_propagate(False)  # Erzwingen der Größe des Frames

# Unterer, eckiger Teil des Farbigen Indikators
sd_indicator_corner = ctk.CTkFrame(sd_indicator, height=15, fg_color=study_duration_goal.color)    
sd_indicator_corner.pack(fill='x', side='bottom')

# Trennlinie zwischen Indikator und Inhalt
border = tk.Frame(study_duration_frame, height=2, bg='#93a0d8')
border.pack(fill='x')

# Titel Label
study_duration_title = tk.Label(study_duration_frame, text='Voraussichtliche\nStudiendauer', font=('quicksand medium', 23, 'bold'), bg='white')
study_duration_title.pack(padx=10,pady=10)

# Vorraussichtliche Studiendauer als Canvas dem Frame hinzufügen
# Canvas für berechnete Zahl zum Festlegen der Höhe
study_duration_canvas = tk.Canvas(study_duration_frame, width=150, height=80, bg='white', highlightthickness=0)    
study_duration_canvas.pack(pady=(15, 0), anchor='center')
# Vorraussichtliche Studiendauer als Text dem Canvas hinzufügen
study_duration_canvas.create_text(75, 30, text=Decimal(str(study_duration_goal.current_value)).quantize(Decimal('0.1'), rounding=ROUND_UP), font=('quicksand medium', 80, 'bold'), fill='black')    # Postion in der Mitte des Canvas, Wert wird auf eine Nachkommastelle gerundet

# Schriftzug 'Jahre' als Label erstellen
years_label = tk.Label(study_duration_frame, text='Jahre', font=('quicksand medium', 20, 'bold'), bg='white')
years_label.pack(pady=2)

# Gesetztes Ziel für Studiendauer als Label erstellen
study_duration_goal_label = tk.Label(study_duration_frame, text=f'(Ziel: {study_duration_goal.goal_value} Jahre)', font=('quicksand', 20), fg='#93a0d8', bg='white')
study_duration_goal_label.pack(padx=10,pady=(5, 20))



# Kursdauer im linken Frame hinzufügen
# Frame für Kursdauer
course_duration_frame = ctk.CTkFrame(left_frame, border_width=2, border_color='#93a0d8', bg_color='white', fg_color='white', corner_radius=22)
course_duration_frame.pack(fill='both', expand=True)

# Titel Label
course_duration_title = tk.Label(course_duration_frame, text='Dauer\nvergangener Kurse', font=('quicksand medium', 20, 'bold'), bg='white')
course_duration_title.pack(padx=10,pady=(10, 0))

# Scrollbarer Frame für Textinhalt
cd_text_frame = ctk.CTkScrollableFrame(course_duration_frame, height=10, fg_color='white', scrollbar_button_color='#93a0d8', scrollbar_button_hover_color='#acb3d3')
cd_text_frame._scrollbar.configure(height=0)    # Veränderung am Frame durch die Höhe der Scrollbar verhindern
cd_text_frame.pack(fill='both', pady=(0, 10), padx=10, expand=True)

# Abgeschlossene Kurse mit Dauer anzeigen
show_finished_courses()



# Ausstehende Bewertungen im mittleren Frame hinzufügen
pending_grades_frame = ctk.CTkFrame(middle_frame, corner_radius=22, border_color='#93a0d8', border_width=2, fg_color='white')
pending_grades_frame.pack(fill='both', expand=True)
# Ausstehende Bewertungen Label
pg_label = ctk.CTkLabel(pending_grades_frame, text='Ausstehende Bewertungen', font=('quicksand medium', 20, 'bold'), bg_color='white', wraplength=300, corner_radius=10, text_color='black')
pg_label.pack(pady=5, padx=2)
pywinstyles.set_opacity(pg_label, color='white')    # Entfernen des Hintergrunds, damit er nicht die Border überdeckt
# Scrollbarer Frame für Textinhalt
pg_text_frame = ctk.CTkScrollableFrame(pending_grades_frame, height=10, fg_color='white', scrollbar_button_color='#93a0d8', scrollbar_button_hover_color='#acb3d3')
pg_text_frame._scrollbar.configure(height=0)    # Veränderung am Frame durch die Höhe der Scrollbar verhindern
pg_text_frame.pack(fill='both', pady=(0, 10), padx=10, expand=True)
# Ausstehende Bewertungen mit Fälligkeitsdatum anzeigen
show_pending_grades()
# Canvas zu Designzwecken erstellen, um Einkerbung in Widget darzustellen
upper_canvas = tk.Canvas(middle_frame, height=71, bg='white', highlightthickness=0)
upper_canvas.place(x=0, y=129)
draw_upper_canvas()



# Notenübersicht im mittleren Frame hinzufügen
go_frame = ctk.CTkFrame(middle_frame, corner_radius=22, border_color='#93a0d8', border_width=2, fg_color='white')
go_frame.pack(fill='both', expand=True, side='bottom')
# Ausstehende Bewertungen Label
go_label = tk.Label(go_frame, text='Notenübersicht', font=('quicksand medium', 17, 'bold'), bg='white')
go_label.pack(pady=(15, 0), padx=2)
# Scrollbarer Frame für Textinhalt
go_text_frame = ctk.CTkScrollableFrame(go_frame, height=10, fg_color='white', scrollbar_button_color='#93a0d8', scrollbar_button_hover_color='#acb3d3')
go_text_frame._scrollbar.configure(height=0)    # Veränderung am Frame durch die Höhe der Scrollbar verhindern
go_text_frame.pack(fill='both', pady=(0, 10), padx=10, expand=True)
# Ausstehende Bewertungen mit Fälligkeitsdatum anzeigen
show_grades()
# Canvas zu Designzwecken erstellen, um Einkerbung in Widget darzustellen
lower_canvas = tk.Canvas(middle_frame, height=71, bg='white', highlightthickness=0)
lower_canvas.place(x=0, y=440)
draw_lower_canvas()



# Notendurchschnitt im mittleren Frame hinzufügen
# Äußerer Frame, der die farbliche Indikation anzeigt
gavg_colored_frame = ctk.CTkFrame(middle_frame, fg_color=grade_goal.color, bg_color='white', border_color='#93a0d8', border_width=2)    
gavg_colored_frame.pack(pady=20, fill='x')
gavg_colored_frame.pack_propagate(False)  # Erzwingen der Größe des Frames
pywinstyles.set_opacity(gavg_colored_frame, color='white')   # Entfernen des Hintergrunds, da er ansonsten Elemente darunter verdecken würde
# Frame für berechnete Zahl
gavg_inner_frame = ctk.CTkFrame(gavg_colored_frame, fg_color='white', bg_color=grade_goal.color, border_color='#93a0d8', border_width=2)    # Innerer Frame, der einen weißen Hintergrund hinter dem aktuellem Wert ermöglicht
gavg_inner_frame.pack(pady=25, padx=25)
gavg_inner_frame.pack_propagate(False)    # Erzwingen der Größe des Frames
pywinstyles.set_opacity(gavg_inner_frame, color=grade_goal.color)   # Entfernen des Hintergrunds, da er ansonsten Elemente darunter verdecken würde
# Label 'Notendurchschnitt' für den inneren Frame
gavg_title = ctk.CTkLabel(gavg_inner_frame, text='Notendurchschnitt', font=('quicksand medium', 18, 'bold'), bg_color='white', corner_radius=10, text_color='black')
gavg_title.pack(pady=(40, 0))
pywinstyles.set_opacity(gavg_title, color='white')    # Entfernen des Hintergrunds, damit er nicht die Border überdeckt
# Notendurchschnitt als Canvas dem Frame hinzufügen
# Canvas für Notendurchschnitt zum Festlegen der Höhe
gavg_canvas = tk.Canvas(gavg_inner_frame, width=150, height=80, bg='white', highlightthickness=0)    
gavg_canvas.pack(pady=10)
# Vorraussichtliche Studiendauer als Text dem Canvas hinzufügen
gavg_canvas.create_text(75, 35, text=Decimal(str(grade_goal.current_value)).quantize(Decimal('0.1'), rounding=ROUND_UP), font=('quicksand medium', 70, 'bold'), fill='black')    # Postion in der Mitte des Canvas, Wert wird auf eine Nachkommastelle gerundet
# Gesetztes Ziel für Notendurchschnitt als Label erstellen
gavg_goal_label = tk.Label(gavg_inner_frame, text=f'(Ziel: {grade_goal.goal_value})', font=('quicksand', 20), fg='#93a0d8', bg='white')
gavg_goal_label.pack()



# Gezahlten Beitrag im rechten Frame hinzufügen
# Frame für gezahlten Beitrag
payed_revenue_frame = ctk.CTkFrame(right_frame, border_width=2, border_color='#93a0d8', bg_color='white', fg_color='white', corner_radius=22)
payed_revenue_frame.pack(pady=(0, 20), fill='both', expand=True)

# Abgerundeter Teil des farbigen Indikators
pr_indicator = ctk.CTkFrame(payed_revenue_frame, height=40, fg_color=revenue_goal.color, bg_color='#93a0d8', corner_radius=20)    
pr_indicator.pack(fill='x', pady=(2, 0), padx=2)
pywinstyles.set_opacity(pr_indicator, color='#93a0d8')  # Entfernen des Hintergrunds
pr_indicator.pack_propagate(False)  # Erzwingen der Größe des Frames

# Unterer, eckiger Teil des Farbigen Indikators
pr_indicator_corner = ctk.CTkFrame(pr_indicator, height=15, fg_color=revenue_goal.color)    
pr_indicator_corner.pack(fill='x', side='bottom')

# Trennlinie zwischen Indikator und Inhalt
pr_border = tk.Frame(payed_revenue_frame, height=2, bg='#93a0d8')
pr_border.pack(fill='x')

# Titel Label
pr_title = tk.Label(payed_revenue_frame, text='Gezahlter Beitrag', font=('quicksand medium', 23, 'bold'), bg='white')
pr_title.pack(padx=10,pady=10, fill='y', expand=True)

# Gezahlter Beitrag als Canvas dem Frame hinzufügen
# Canvas für berechnete Zahl zum Festlegen der Höhe
pr_canvas = tk.Canvas(payed_revenue_frame, width=280, height=60, bg='white', highlightthickness=0)    
pr_canvas.pack(fill='y', expand=True)
# Aktuellen Wert in deutsche Schreibweise umformatieren
formatted_current_value = format(revenue_goal.current_value, ',.2f').replace(',', 'X').replace('.', ',').replace('X', '.')
# Gezahlter Beitrag als Text dem Canvas hinzufügen
pr_canvas.create_text(140, 30, text=f'{formatted_current_value}€', font=('quicksand medium', 39, 'bold'), fill='black')
# Zielwert in deutsche Schreibweise umformatieren
formatted_goal_value = format(revenue_goal.goal_value, ',.2f').replace(',', 'X').replace('.', ',').replace('X', '.')
# Gesetztes Ziel für gezahlten Beitrag als Label erstellen
pr_goal_label = tk.Label(payed_revenue_frame, text=f'(Ziel: max {formatted_goal_value}€)', font=('quicksand', 20), fg='#93a0d8', bg='white')
pr_goal_label.pack(padx=10,pady=10, fill='y', expand=True)



# Aktive Kurse im rechten Frame hinzufügen
# Frame für aktive Kurse
active_courses_frame = ctk.CTkFrame(right_frame, border_width=2, border_color='#93a0d8', bg_color='white', fg_color='white', corner_radius=22)
active_courses_frame.pack(pady=(0, 20), fill='both', expand=True)

# Titel Label
ac_title = tk.Label(active_courses_frame, text='Aktive Kurse', font=('quicksand medium', 25, 'bold'), bg='white')
ac_title.pack(padx=10,pady=(20, 10), fill='y', expand=True)

# Aktive Kurse als Canvas dem Frame hinzufügen
# Canvas für aktive Kurse zum Festlegen der Höhe
ac_canvas = tk.Canvas(active_courses_frame, width=280, height=120, bg='white', highlightthickness=0)    
ac_canvas.pack(fill='y', expand=True)
# Anzahl aktiver Kurse als Text dem Canvas hinzufügen
ac_canvas.create_text(140, 60, text=int(active_courses_goal.current_value), font=('quicksand medium', 90, 'bold'), fill='black')    # Aktuellen Wert als Integer übergeben

# Gesetztes Ziel für aktive Kurse als Label erstellen
ac_goal_label = tk.Label(active_courses_frame, text=f'(Ziel: min {int(active_courses_goal.goal_value)})', font=('quicksand', 20), fg='#93a0d8', bg='white')     # Zielwert ebenfalls als Integer übergeben
ac_goal_label.pack(padx=10,pady=10, fill='y', expand=True)

# Abgerundeter Teil des farbigen Indikators
ac_indicator = ctk.CTkFrame(active_courses_frame, height=40, fg_color=active_courses_goal.color, bg_color='#93a0d8', corner_radius=20)    
ac_indicator.pack(fill='x', pady=(0, 2), padx=2, side='bottom')
pywinstyles.set_opacity(ac_indicator, color='#93a0d8')  # Entfernen des Hintergrunds
ac_indicator.pack_propagate(False)  # Erzwingen der Größe des Frames

# Unterer, eckiger Teil des Farbigen Indikators
ac_indicator_corner = ctk.CTkFrame(ac_indicator, height=15, fg_color=active_courses_goal.color)    
ac_indicator_corner.pack(fill='x')

# Trennlinie zwischen Indikator und Inhalt
ac_border = tk.Frame(active_courses_frame, height=2, bg='#93a0d8')
ac_border.pack(fill='x', side='bottom')



# Indikator hinzufügen
# Frame für alle Widgets des Indikators
indicator_frame = tk.Frame(root, bg='white')

# "Nicht gut"-Label als schriftlicher Indikator
bad_label = tk.Label(indicator_frame, text='Nicht gut', font=('quicksand', 13), fg='#93a0d8', bg='white')
bad_label.pack(side='left')

# Frame, der abgerundete Ecken für den Indikator ermöglicht
indicator_gradient_frame = ctk.CTkFrame(indicator_frame, width=150, height=15, border_color='#93a0d8', border_width=2, fg_color='white', bg_color='white', corner_radius=15)
indicator_gradient_frame.pack(side='left', padx=5, pady=(5, 0))
indicator_gradient_frame.pack_propagate(False)  # Erzwingen der Größe des Frames

# Erstellen eines roten Kreise, um eine runde optik des Indikators zu ermöglichen
red_circle = ctk.CTkFrame(indicator_gradient_frame, width=11, height=11, fg_color=choose_color(0), bg_color='#93a0d8', corner_radius=15)
red_circle.place(x=2, y=2)
pywinstyles.set_opacity(red_circle, color='#93a0d8')    # Entfernen des Hintergrunds

# Erstellen eines grünen Kreise, um eine runde optik des Indikators zu ermöglichen
green_circle = ctk.CTkFrame(indicator_gradient_frame, width=11, height=11, fg_color=choose_color(100), bg_color='#93a0d8', corner_radius=15)
green_circle.place(x=138, y=2)
pywinstyles.set_opacity(green_circle, color='#93a0d8')    # Entfernen des Hintergrunds

# Erstellung eines Canvas zur Dartsellung des Farbverlaufs
indicator_canvas = tk.Canvas(indicator_gradient_frame, width=135, height=10, bg='white', highlightthickness=0)
indicator_canvas.place(x=9, y=2)
# Zeichnen des Farbverlaufs
draw_gradient(indicator_canvas, 135, 10)

# "Gut"-Label als schriftlicher Indikator
good_label = tk.Label(indicator_frame, text='Gut', font=('quicksand', 13), fg='#93a0d8', bg='white')
good_label.pack(side='left')



# Studiengang hinzufügen
course_of_studies_label = tk.Label(root, text=student.course_of_studies.name, font=('quicksand', 16), fg='#93a0d8', bg='white')
course_of_studies_label.pack(side='bottom', pady=10)

root.bind('<Configure>', widget_positions)     # Berechnung der Position des Indikators und des Datums bei Veränderungen am Fenster

# Hauptloop starten
root.mainloop()