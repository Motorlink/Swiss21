# Webisco-Schnittstelle: Aufträge anlegen

**Quelle:** Webisco-Schnittstellenbeschreibung Protokoll-Version 55 (Abisco 8.8.23)  
**Stand:** 24.10.2025

---

## ✅ ANTWORT: JA, Aufträge können über Webisco angelegt werden!

### Ressource: `createauftrag`

**Beschreibung:** Erzeugt einen Auftrag in Abisco

---

## 📋 Übersicht aller Webisco-Ressourcen

Die Webisco-Schnittstelle ist ein **XML-basierter HTTP-POST-Service** auf Port 8228.

| Ressource | Beschreibung |
|-----------|--------------|
| `config` | Liefert kundenspezifische Grundkonfigurationen |
| `artikelanfrage` | Liefert Artikel nach bestimmten Suchkriterien |
| `beleganfrage` | Liefert existierende Kundenbelege |
| `belegbemerkung` | Fügt eine Bemerkung zu einem bestehenden Beleg hinzu |
| **`createauftrag`** | **Erzeugt einen Auftrag in Abisco** ✅ |
| `createkunde` | Erzeugt einen neuen Kunden in Abisco |
| `kundensuche` | Liefert Kundendaten anhand von Suchmustern |
| `positionsanfrage` | Liefert existierende Positionen für eventuelle Rückgaben |
| `removeauftrag` | Löscht einen bestehenden Auftrag |
| `tourfahrtanfrage` | Liefert die nächsten Tourfahrten für einen Kunden |
| `updatekunde` | Ändert die Daten eines existierenden Kunden |
| `zahlung` | Fügt eine Anzahlung zu einem Auftrag hinzu |
| `zugangsdaten` | Sendet dem Kunden seine Zugangsdaten |

---

## 🔧 Technische Details

### Kommunikation

- **Protokoll:** HTTP-POST
- **Port:** 8228
- **Format:** XML (UTF-8)
- **Server:** www.webisco.de:8228

### HTTP-Aufruf Beispiel

```
POST /createauftrag HTTP/1.1
Connection: Keep-Alive
Host: www.webisco.de:8228
content-length: 178

<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<webisco version="21" username="testuser" password="geheim" type="request">
<content>
[...Anfrage-Daten...]
</content>
</webisco>
```

### Envelope-Struktur

```xml
<webisco version="21" username="..." password="..." type="request">
  <content>
    <!-- Auftragsdaten hier -->
  </content>
</webisco>
```

**Attribute:**
- `version`: Versionsnummer des Protokolls (z.B. "21")
- `username`: Benutzername (oder Kundennummer)
- `password`: Passwort des Kunden
- `type`: "request" bei Anfragen, "response" bei Antworten

---

## 📝 Datentypen

| Datentyp | Beschreibung |
|----------|--------------|
| `#TEXT` | Zeichenfolge beliebiger Länge |
| `#ZAHL` | Ganzzahl (Integer) |
| `#GKZ` | Gleitkommazahl (Double), Komma als Dezimaltrennzeichen |
| `#PREIS` | Preis in Euro, Komma als Dezimaltrennzeichen |
| `#PROZENT` | Prozentzahl mit maximal zwei Nachkommastellen |
| `#MENGE` | Menge mit maximal zwei Nachkommastellen |
| `#BOOL` | Wahrheitswert ("T" = True, "F" = False) |
| `#DATUM` | Datum in der Form "YYYY-MM-DD" |
| `#ZEIT` | Zeitangabe in der Form "HH:MM:SS" |
| `#DATUMZEIT` | Zeitstempel in der Form "YYYY-MM-DD HH:MM:SS" |
| `#ENUM` | Ein Aufzählungstyp vom Typ #TEXT |

---

## 🎯 Nächste Schritte

Um die genaue Struktur für `createauftrag` zu sehen, müssen wir die entsprechende Seite in der PDF lesen (Seite 15 laut Inhaltsverzeichnis: "13. Aufträge anlegen (Bestellungen oder Anfragen)").

**Soll ich die Seite 15 der PDF öffnen und die genaue Struktur dokumentieren?**
