"""
# Schach-API

| : Verfügbare Funktionen
| : Anleitung
| : Wichtige Hinweise
| : Variableninfo
| : Technische Details


Verfügbare Funktionen
-------------------
- visual_feldname
    Visualisiert die Feldnummer als Schachfeldname
- visual_farbe
    Visualisiert die Farbnummer als Farbnamen
- visual_farbenkürzel
    Visualisiert die Farbnummer als Farbkürzel
- visual_figur
    Visualisiert die Figurnummer als Figurennamen
- visual_figurkürzel
    Visualisiert die Figurnummer als Figurenkürzel
- neues_spiel
    Herstellen der Variablen für ein neues Spiel
- fstatus_func
    Herstellen der Statusvariable - Sortierung: Feld > Farbe >> Figur
- farbe_figur_auf_feld
    Ausgabe der Armeefarbe und Figur auf dem übermittelten Feld
- figurfelder_final
    Berechnet alle möglichen Zielfelder der Figur auf dem entsprechenden Startfeld unter Berücksichtigung von Brettbegrenzung und Figurenblockaden
- armeefiguren_final:
    Gibt final für die übergebene Farbe die Liste der bewegungsfähigen Figuren anhand deren Felder aus. Alle Funktionen wurden darin berücksichtigt.
- zug_final
    Führt den angegebenen Zug aus und aktualisiert kstatus und gibt zusätzlich die Weiterschlagen und Matt als bool aus.

Anleitung
---------
1. **Spielstart:**
    Zum Spielstart muss 1 Variable lokal angelegt mit der Funktion :class:`neues_spiel` (:class:`kstatus = schach_api.neues_spiel()`).
2. **Spielfeldvisualisierung:**
    :class:`kstatus` ist ein Dictionary das von den Figuren ausgehend, deren besetzte Felder anzeigt, aufgebaut ist, man kann davon immer mit der Funktion :class:`fstatus_func` ein Dictionary herleiten, bei dem das Spielfeld die Referenz ist.
3. **Bei jedem Zug:**
    Mit der Funktion :class:`armeefiguren_final` erhältst du eine Liste der Figuren anhand ihrer Felder, die ziehen können und dürfen.
    Mit der Funktion :class:`figurfelder_final` erhältst du eine Liste, welche Felder die ausgewählte Figur besetzen kann und darf.
    Mit der Funktion :class:`zug_final` setzt du den :class:`kstatus` neu anhand der angegebenen Figurbewegung
4. **Sonderfälle:**
    :class:`zug_final` gibt zusätzlich Informationen aus:
    4.1. **Weiterschlagen:**
        Wenn die gezogene Farbe einen weiteren Schlag ausführen kann.
    4.2. **Matt:**
        Wenn die gegnerische Farbe Matt ist.

WICHTIG
---------
- Die Funktion :class:`zug_final` prüft keine validen Züge, deswegen ist ein korrektes Spiel nur gewährleistet, wenn die richtigen Werte ordentlich weitergereicht werden. 💎

Variableninfo
-----------------
- kstatus
    Allgemeine Statusvariable - beinhaltet so die Startsituation - Sortierung: Farbe > Figur >> Liste der Felder

Technische Details
---------
- **Spielfeld:**
    🔽 schwarz
    18  28	38	48	58	68	78	88
    17	27	37	47	57	67	77	87
    16	26	36	46	56	66	76	86
    15	25	35	45	55	65	75	85
    14	24	34	44	54	64	74	84
    13	23	33	43	53	63	73	83
    12	22	32	42	52	62	72	82
    11	21	31	41	51	61	71	81
    🔼 weiß
- **Farbe:**
    < *10* = w / Weiß ⚪
    < *-10* = s / Schwarz ⚫
    sollte *0* sein ist es als leer zu werten
- **Figuren:**
    < *1* = b / Bauer
    < *2* = d / Dame
"""
from copy import deepcopy

__version__ = "16-Feb-2026 10:00"

def _strer(x: str | int) -> str:
    return str(x)

_allefelder = [11, 13, 15, 17, 22, 24, 26, 28, 31, 33, 35, 37, 42, 44, 46, 48, 51, 53, 55, 57, 62, 64, 66, 68, 71, 73, 75, 77, 82, 84, 86, 88]
_farben = {10: "weiß", -10: "schwarz"}
_farbenkürzel = {10: "w", -10: "s", 0: "c"}
_figuren = {1: "Bauer", 2: "Dame"}
_figurenkürzel = {1: "b", 2: "d", 0: "c"}


_bauernweg = {10: [+11, -9, 8], -10: [-11, +9, 1]}
"""
I 0 : Ein Feld diagonal vorwärts rechts
I 1 : Ein Feld diagonal vorwärts links
I 2 : Zielfeld%10 muss gleich sein - indexiert die gegn. Grundreihe
"""

def visual_feldname(feld: int | str) -> str:
    """
    Zulässig: von 11 bis 88, Zahlen mit 9 oder 0 ausgenommen
    """
    o = _strer(feld)
    match o[0]:
        case "1":
            return "A" + o[1]
        case "2":
            return "B" + o[1]
        case "3":   
            return "C" + o[1]
        case "4":
            return "D" + o[1]   
        case "5":
            return "E" + o[1]
        case "6":
            return "F" + o[1]
        case "7":
            return "G" + o[1]
        case "8":
            return "H" + o[1]
def visual_farbe(x: int) -> str:
    """
    Zulässig: 10, -10
    """
    return _farben[x]
def visual_farbenkürzel(x: int) -> str:
    """
    Zulässig: 10, -10, 0
    """
    return _farbenkürzel[x]
def visual_figur(figur: int) -> str:
    """
    Zulässig: 1-2
    """
    return _figuren[figur]
def visual_figurkürzel(figur: int) -> str:
    """
    Zulässig: 1-2
    """
    return _figurenkürzel[figur]


kstatus: dict[int, dict[int, list[int]]] = {10: {1: [11, 13, 22, 31, 33, 42, 51, 53, 62, 71, 73, 82], 2: []}, -10: {1: [17, 26, 28, 37, 46, 48, 57, 66, 68, 77, 86, 88], 2: []}}
"""Allgemeine Statusvariable - beinhaltet so die Startsituation - Sortierung: Farbe > Figur > Liste der Felder"""

def neues_spiel() -> dict[int, dict[int, list[int]]]:
    """
    Herstellen der Variablen für ein neues Spiel
    
    Return
    -------
    - kstatus:
        :class:`dict[int, dict[int, list[int]]]`
        Status der Figuren auf dem Schachbrett
    """
    return deepcopy(kstatus)

def fstatus_func(kstatus: dict[int, dict[int, list[int]]]) -> dict[int, dict[int, int]]:
    """
    Herstellen der Statusvariable - Sortierung: Feld > Farbe >> Figur

    Input
    -------
    - kstatus:
        :class:`dict[int, dict[int, list[int]]]`
        Status der Figuren auf dem Schachbrett
    
    Return
    -------
    - fstatus:
        :class:`dict[int, dict[int, int]]`
    """
    fstatus: dict[int, dict[int, int]] = {x: {0: 0} for x in range(11, 89)}
    for fa, farbe in kstatus.items():
        for fi, felder in farbe.items():
            for feld in felder:
                fstatus[feld] = {fa: fi}
    return fstatus

def farbe_figur_auf_feld(kstatus: dict[int, dict[int, list[int]]], feld: int) -> tuple[int, int]:
    """
    Ausgabe der Armeefarbe und Figur auf dem übermittelten Feld

    Input
    -------
    - kstatus:
        :class:`dict[int, dict[int, list[int]]]`
        Status der Figuren auf dem Schachbrett
    - feld:
        :class:`int`
        Feldnummer
    
    Return
    -------
    - farbe:
        :class:`int`
    - figur:
        :class:`int`
    """
    fstatus = fstatus_func(kstatus)
    farbe, figur = next(iter(fstatus[feld].items()))
    return farbe, figur

def figurfelder_final(kstatus: dict[int, dict[int, list[int]]], startfeld: int) -> tuple[list[int], bool]:
    """
    Berechnet alle möglichen Zielfelder der Figur auf dem entsprechenden Startfeld unter Berücksichtigung von Brettbegrenzung und Figurenblockaden

    Input
    -------
    - kstatus:
        :class:`dict[int, dict[int, list[int]]]`
        Status der Figuren auf dem Schachbrett
    - startfeld:
        :class:`int`
        Startfeldnummer
    
    Return
    -------
    - figurfelderliste:
        :class:`list[int]`
    - kannschlagen
        :class:`bool`
    """
    normalliste: list[int] = []
    schlagliste: list[int] = []
    farbe, figur = farbe_figur_auf_feld(kstatus, startfeld)
    kannschlagen = False
    match figur:
        case 1:
            sr = _bauernweg[farbe][0]
            sl = _bauernweg[farbe][1]
            for richtung in [sr, sl]:
                ziel1feld = int(richtung+startfeld)
                ziel2feld = int(richtung*2+startfeld)
                if ziel1feld in _allefelder:
                    zfa, zfi = farbe_figur_auf_feld(kstatus, ziel1feld)
                    if zfa == farbe:
                        continue
                    elif zfa == 0:
                        normalliste.append(ziel1feld)
                        continue
                    elif zfa == -farbe:
                        if ziel2feld in _allefelder:
                            z2fa, z2fi = farbe_figur_auf_feld(kstatus, ziel2feld)
                            if z2fa == 0:
                                kannschlagen = True
                                schlagliste.append(ziel2feld)
        case 2:
            sr = _bauernweg[farbe][0]
            sl = _bauernweg[farbe][1]
            for richtung in [sr, sl, -sr, -sl]:
                ziel1feld = int(richtung+startfeld)
                ziel2feld = int(richtung*2+startfeld)
                if ziel1feld in _allefelder:
                    zfa, zfi = farbe_figur_auf_feld(kstatus, ziel1feld)
                    if zfa == farbe:
                        continue
                    elif zfa == 0:
                        normalliste.append(ziel1feld)
                        continue
                    elif zfa == -farbe:
                        if ziel2feld in _allefelder:
                            z2fa, z2fi = farbe_figur_auf_feld(kstatus, ziel2feld)
                            if z2fa == 0:
                                kannschlagen = True
                                schlagliste.append(ziel2feld)
    if kannschlagen:
        return sorted(schlagliste), kannschlagen
    return sorted(normalliste), kannschlagen

def armeefiguren_final(kstatus: dict[int, dict[int, list[int]]], farbe: int) -> tuple[list[int], bool]:
    """
    Gibt final für die übergebene Farbe die Liste der bewegungsfähigen Figuren anhand deren Felder aus. Alle Funktionen wurden darin berücksichtigt.

    Input
    -------
    - kstatus:
        :class:`dict[int, dict[int, list[int]]]`
        Status der Figuren auf dem Schachbrett  
    - farbe:
        :class:`int`
        Armeefarbe
    
    Return
    -------
    - armeeliste:
        :class:`list[int]`
    - schlag:
        :class:`bool`
        Gibt aus, ob die Farbe gerade schlagen kann
    """
    normalliste: list[int] = []
    schlagliste: list[int] = []
    schlagen = False
    armeeliste = kstatus[farbe]
    for fig in armeeliste.values():
        for feld in fig:
            felder, kannschlagen = figurfelder_final(kstatus, feld)
            if kannschlagen:
                schlagliste.append(feld)
                schlagen = True
            elif len(felder) > 0:
                normalliste.append(feld)
    if len(schlagliste) == 0:
        return sorted(normalliste), schlagen
    return sorted(schlagliste), schlagen

def zug_final(kstatus: dict[int, dict[int, list[int]]], startfeld: int, zielfeld: int) -> tuple[dict[int, dict[int, list[int]]], bool, bool]:
    """
    Führt den angegebenen Zug aus und aktualisiert kstatus und gibt zusätzlich die Weiterschlagen und Matt als bool aus.

    Input
    -------
    - kstatus:
        :class:`dict[int, dict[int, list[int]]]`
        Status der Figuren auf dem Schachbrett  
    - startfeld:
        :class:`int`
        Startfeldnummer
    - zielfeld:
        :class:`int`
        Zielfeldnummer

    Return
    -------
    - kstatus:
        :class:`dict[int, dict[int, list[int]]]`
    - weiterschlagen:
        :class:`bool`  
    - matt:
        :class:`bool`
    """
    matt = False
    weiterschlagen = False
    geschlagen = False
    umgewandelt = False
    farbe, figur = farbe_figur_auf_feld(kstatus, startfeld)
    diff = zielfeld-startfeld
    sr = _bauernweg[farbe][0]
    sl = _bauernweg[farbe][1]
    if diff in [sr, sl, -sr, -sl]:
        kstatus[farbe][figur].remove(startfeld)
        kstatus[farbe][figur].append(zielfeld)
    elif diff//2 in [sr, sl, -sr, -sl]:
        kstatus[farbe][figur].remove(startfeld)
        kstatus[farbe][figur].append(zielfeld)
        ggfa, ggfi = farbe_figur_auf_feld(kstatus, zielfeld-diff//2)
        kstatus[ggfa][ggfi].remove(zielfeld-diff//2)
        geschlagen = True
    if zielfeld%10 == _bauernweg[farbe][2]:
        if figur == 1:
            kstatus[farbe][1].remove(zielfeld)
            kstatus[farbe][2].append(zielfeld)
            umgewandelt = True
    neueliste, schlagen = figurfelder_final(kstatus, zielfeld)
    weiterschlagen = schlagen and geschlagen and not umgewandelt
    ggliste, ggsschl = armeefiguren_final(kstatus, -farbe)
    if len(ggliste) == 0:
        matt = True
    return kstatus, weiterschlagen, matt



