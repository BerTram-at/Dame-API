# Dame-API
Deutsche Dame-API für Python

## 📋 Inhaltsverzeichnis
- [Verfügbare Funktionen](#verfügbare-funktionen)
- [Anleitung](#anleitung)
- [Wichtige Hinweise](#wichtige-hinweise)
- [Variableninfo](#variableninfo)
- [Technische Details](#technische-details)

## Verfügbare Funktionen
- **visual_feldname**  
  Visualisiert die Feldnummer als Feldname (z. B. 11 → A1)
- **visual_farbe**  
  Visualisiert die Farbnummer als Farbnamen (10 / -10)
- **visual_farbenkürzel**  
  Visualisiert die Farbnummer als Farbkürzel (w / s / c)
- **visual_figur**  
  Visualisiert die Figurnummer als Figurennamen
- **visual_figurkürzel**  
  Visualisiert die Figurnummer als Figurenkürzel
- **neues_spiel**  
  Erstellt die Variablen für ein neues Spiel (Startaufstellung)
- **fstatus_func**  
  Erstellt die Statusvariable - Sortierung: Feld > Farbe >> Figur
- **farbe_figur_auf_feld**  
  Gibt die Armeefarbe und Figur auf dem übermittelten Feld aus
- **figurfelder_final**  
  Kompiliert die allgemein möglichen Zielfelder der Figur auf dem entsprechenden Startfeld unter Berücksichtigung von Brettbegrenzung und Figurenblockaden und gibt diese Liste aus. Gibt außerdem zurück, ob ein Schlag möglich ist.
- **armeefiguren_final**  
  Gibt final für die übergebene Farbe die Liste der bewegungsfähigen Figuren anhand deren Felder aus. Berücksichtigt mögliche Schlagzüge.
- **zug_final**  
  Führt den angegebenen Zug aus, aktualisiert `kstatus` und gibt zusätzlich `weiterschlagen` und `matt` als boolesche Werte zurück.

## Anleitung

1. **Spielstart:**  
   Zum Spielstart muss 1 Variable lokal angelegt werden mit der Funktion `neues_spiel()`:
   ```python
   kstatus = dame_api.neues_spiel()
   ```

2. **Spielfeldvisualisierung:**  
   `kstatus` ist ein Dictionary, das von den Figuren ausgehend ihre besetzten Felder anzeigt. Mit der Funktion `fstatus_func()` kann daraus ein Dictionary hergeleitet werden, das den Status pro Feld liefert.

3. **Bei jedem Zug:**  
   - Mit `armeefiguren_final(kstatus, farbe)` erhältst du eine Liste der Figuren (identifiziert durch ihr Startfeld), die ziehen können und/oder schlagen müssen.  
   - Mit `figurfelder_final(kstatus, startfeld)` erhältst du die Liste der möglichen Zielfelder der ausgewählten Figur sowie einen Bool (`kannschlagen`), ob ein Schlag möglich ist.  
   - Mit `zug_final(kstatus, startfeld, zielfeld)` führst du den Zug aus und erhältst den aktualisierten `kstatus` sowie Flags für `weiterschlagen` und `matt`.

4. **Sonderfälle (Rückgabewerte von `zug_final`):**  
   - **Weiterschlagen:** Wahr, wenn ein Schlag ausgeführt wurde und die gezogene Figur unmittelbar weiter schlagen kann (und keine Umwandlung stattfand).  
   - **Matt:** Wahr, wenn die gegnerische Farbe danach keine legalen Züge mehr besitzt.

## ⚠️ Wichtige Hinweise
- Die Funktion `zug_final()` prüft nicht alle Validitätsregeln für Züge. Ein korrektes Spiel ist nur gewährleistet, wenn die richtigen Werte (gültige Start- und Zielfelder) ordentlich weitergereicht werden. 💎

## Variableninfo

- **kstatus**  
  Allgemeine Statusvariable — beinhaltet die Startsituation bzw. aktuelle Spielsituation. Sortierung: Farbe > Figur >> Liste der Felder. Beispielhafte Struktur: `{farbe: {figur: [liste_felder]}}`

## Technische Details

### Spielfeld
```
🔽 schwarz
18  28  38  48  58  68  78  88
17  27  37  47  57  67  77  87
16  26  36  46  56  66  76  86
15  25  35  45  55  65  75  85
14  24  34  44  54  64  74  84
13  23  33  43  53  63  73  83
12  22  32  42  52  62  72  82
11  21  31  41  51  61  71  81
🔼 weiß
```

### Farbe
- `10` = **w** / Weiß ⚪  
- `-10` = **s** / Schwarz ⚫  
- `0` = leer

### Figuren
- `1` = **Bauer**  
- `2` = **Dame**

### Hinweise zur Bewegung (intern)
- `_bauernweg` definiert die Richtungen für normale Züge und Schlagzüge je Farbe. Die Indices sind intern folgendermaßen genutzt:
  - Index 0: ein diagonales Vorwärtsfeld (rechts)
  - Index 1: ein diagonales Vorwärtsfeld (links)
  - Index 2: Prüfflag für die jeweils gegenüberliegende Grundreihe (für Umwandlungen)
