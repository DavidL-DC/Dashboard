from typing import Union  # Union ermöglicht es, mehrere Datentypen für eine Variable zuzulassen
from matplotlib import colors  # Importieren von Matplotlib für Farbmanipulation
from decimal import Decimal, ROUND_UP  # Importieren von Decimal für präzise Berechnungen

# Definition der Klasse Goal
class Goal:
    # Initialisierung von Goal
    def __init__(self, title: str, goal_value: Union[float, int], current_value: Union[float, int], worst_value: Union[float, int], low_goal: bool):
        # Überprüfen der Eingabewerte, ob sie den richtigen Datentyp haben
        if not isinstance(title, str):
            raise ValueError('Title must be a string.')
        if not isinstance(goal_value, (float, int)):
            raise ValueError('Goal_value must be a float or an integer.')
        if not isinstance(current_value, (float, int)):
            raise ValueError('Current_value must be a float or an integer.')
        if not isinstance(worst_value, (float, int)):
            raise ValueError('Worst_value must be a float or an integer.')
        if not isinstance(low_goal, bool):
            raise ValueError('Low_goal must be a boolean.')
        
        # Zuweisung der Eingabewerte an die privaten Attribute, dabei werden die Werte gerundet
        self._title = title
        self._goal_value = Decimal(str(goal_value)).quantize(Decimal('0.1'), rounding=ROUND_UP)
        self._current_value = Decimal(str(current_value)).quantize(Decimal('0.01'), rounding=ROUND_UP)
        self._worst_value = Decimal(str(worst_value)).quantize(Decimal('0.01'), rounding=ROUND_UP)
        self._low_goal = low_goal

    # Getter und Setter für alle Attribute
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, new_title):
        if not isinstance(new_title, str):
            raise ValueError('Title must be a string.')
        self._title = new_title

    @property
    def goal_value(self):
        return self._goal_value
    
    @goal_value.setter
    def goal_value(self, new_goal_value):
        if not isinstance(new_goal_value, (float, int)):
            raise ValueError('Goal_value must be a float or an integer.')
        self._goal_value = Decimal(str(new_goal_value)).quantize(Decimal('0.1'), rounding=ROUND_UP)

    @property
    def current_value(self):
        return self._current_value
    
    @current_value.setter
    def current_value(self, new_current_value):
        if not isinstance(new_current_value, (float, int)):
            raise ValueError('Current_value must be a float or an integer.')
        self._current_value = Decimal(str(new_current_value)).quantize(Decimal('0.01'), rounding=ROUND_UP)
        
    @property
    def worst_value(self):
        return self._worst_value
    
    @worst_value.setter
    def worst_value(self, new_worst_value):
        if not isinstance(new_worst_value, (float, int)):
            raise ValueError('Worst_value must be a float or an integer.')
        self._worst_value = Decimal(str(new_worst_value)).quantize(Decimal('0.01'), rounding=ROUND_UP)

    @property
    def low_goal(self):
        return self._low_goal
    
    @low_goal.setter
    def low_goal(self, new_low_goal):
        if not isinstance(new_low_goal, bool):
            raise ValueError('Low_goal must be a boolean.')
        self._low_goal = new_low_goal

    # Fortschritt des Ziels berechnen
    @property
    def progress(self):
        # Berechnung für Ziele, die einen niedrigen Wert anstreben
        if self.low_goal:
            return max(0, min(round(((self.worst_value - self.current_value) / (self.worst_value - self.goal_value)) * 100), 100))  # Fortschritt wird auf ganze Zahlen gerundet und auf einen Maximalwert von 100 und einen Minimalwert von 0 limitiert.
        # Berechnung für Ziele, die einen hohen Wert anstreben
        else: 
            return max(0, min(round(((self.current_value - self.worst_value) / (self.goal_value - self.worst_value)) * 100), 100))
        
    # Farbcode basierend auf dem Fortschritt berechnen
    @property
    def color(self):
        # Definiert die Farbpalette (rot, gelb, grün)
        base_colors = ['#FF817A', '#FFFE7A', '#7FFF7A']
        cmap = colors.LinearSegmentedColormap.from_list('cmap', base_colors)  # Erzeugt ein Farbschema basierend auf den Basisfarben
        norm = colors.Normalize(vmin=0, vmax=100)  # Normalisiert den Fortschritt, um ihn auf den Bereich von 0 bis 100 zu bringen
        color = cmap(norm(self.progress))  # Berechnet die Farbe basierend auf dem Fortschritt
        return colors.rgb2hex(color)  # Wandelt die RGB-Farbe in den Hex-Code um