# Studiums-Dashboard mit Zielsetzung
Ein Prototyp, um einen Überblick über persönliche Ziele und des Fortschritte, im Rahmen eines Studiums, zu gewinnen.

## Beschreibung
Dieses Projekt ist ein einfaches Dashboard, welches einen Überblick über vier Hauptziele (Dauer, Kosten, Noten und Kurse) eines Studiums ermöglicht.
Es wurde im Rahmen eines Kurses an einer Hochschule erstellt und legt den Schwerpunkt auf objektorientierte Programmierung und dessen Hauptkonzepte, wie Vererbung und Komposition.
Aktuell dient dieses Projekt ausschließlich einem Leistungsnachweis und wird zur Bewertung veröffentlicht.

## Installation

### Voraussetzungen
1. **Python installieren:**  
   Stelle sicher, dass Python (mindestens Version 3.13) auf deinem Computer installiert ist.  
   - [Python herunterladen](https://www.python.org/downloads/)  
   - Überprüfen, ob Python korrekt installiert ist:  
     ```bash
     python --version
     ```

2. **Pip installieren:**
   Pip sollte bereits mit Python installiert sein. Überprüfe es mit:
   ```bash
   pip --version
   ```

---

### Installationsschritte

1. **Projekt herunterladen:**  
   Lade das Projekt von GitHub herunter:  
   [GitHub-Link einfügen]

   Alternativ kannst du das Projekt direkt mit Git klonen:  
   ```bash
   git clone [GitHub-Link einfügen]
   cd projektordner
   ```

2. **Virtuelle Umgebung erstellen (empfohlen):**  
   Erstelle eine virtuelle Umgebung, um Abhängigkeiten zu isolieren:  
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate         # Windows
   ```

3. **Abhängigkeiten installieren:**  
   Installiere die benötigten Bibliotheken mit `requirements.txt`:  
   ```bash
   pip install -r requirements.txt
   ```

4. **Schriftarten sicherstellen:**  
   Achte darauf, dass die Schriftarten `Quicksand-Medium.ttf` und `Quicksand-Regular.ttf` im gleichen Ordner wie die Python-Dateien liegen. Diese werden automatisch geladen.

5. **Programm starten:**  
   Starte das Dashboard:  
   ```bash
   python Dashboard.py
   ```

---

## Projektstruktur

```
projektordner/
├── Quicksand-Medium.ttf
├── Quicksand-Regular.ttf
├── Beispieldaten.py
├── Dashboard.py
├── Kurs.py
├── Modul.py
├── Semester.py
├── Student.py
├── Studienelement.py
├── Studiengang.py
├── Ziel.py
├── requirements.txt
```

---

## Nutzung

---

## Lizenz
Dieses Projekt ist nur für Bildungszwecke gedacht und darf nicht für kommerzielle oder produktive Zwecke verwendet werden.

---

## Kontakt
Falls es Fragen gibt, kontaktieren Sie mich unter der an der Hochschule hinterlegten E-Mail.

---

## Beitragende
- David Lohmann (https://github.com/DavidL-DC)
