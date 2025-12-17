# Dokumentations-Index für Swiss21

**Vollständige Übersicht aller Dokumentationen für die KI-Übergabe**

---

## Hauptdokumentationen

### 1. [HANDOVER_FOR_AI.md](./HANDOVER_FOR_AI.md)
**Vollständige Übergabedokumentation für KI-Agenten**

Diese Datei ist die zentrale Anlaufstelle für jeden KI-Agenten, der das Projekt übernimmt. Sie enthält:
- Projektübersicht und Architektur
- Repository-Struktur
- Nächste Schritte für die Übernahme
- Detaillierte Beschreibung aller Scripts und Code
- Server-Setup und Credentials-Management
- API-Mappings und Datenstrukturen
- Datenbank und extrahierte Daten
- Systematischer Import-Prozess
- Wichtige Dateien und Ressourcen

**Zielgruppe:** KI-Agenten, die das Projekt übernehmen  
**Umfang:** Vollständig  
**Status:** ✅ Aktuell

---

### 2. [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md)
**Projekt-Übersicht und aktueller Stand**

Diese Datei bietet einen kompakten Überblick über das gesamte Projekt:
- Projektziel und Datenfluss
- Aktueller Projektstand (was wurde bereits erreicht)
- Wichtige Erkenntnisse
- Nächste Schritte
- Wichtige Dateien
- Benutzeranforderungen
- Server-Details
- Technologie-Stack

**Zielgruppe:** Alle, die einen schnellen Überblick benötigen  
**Umfang:** Zusammenfassung  
**Status:** ✅ Aktuell

---

### 3. [STEP_BY_STEP_GUIDE.md](./STEP_BY_STEP_GUIDE.md)
**Schritt-für-Schritt-Anleitung für KI-Agenten**

Diese Datei ist eine detaillierte Anleitung für die Durchführung des systematischen Imports:
- Phase 1: Kunden in ABA Ninja importieren
- Phase 2: Rechnungen in ABA Ninja importieren
- Phase 3: QR-Code-Generierung
- Phase 4: E-Mail-Versand
- Phase 5: Zahlungsabgleich

Jede Phase enthält konkrete SQL-Abfragen, API-Endpunkte und Code-Beispiele.

**Zielgruppe:** KI-Agenten, die den Import durchführen  
**Umfang:** Detaillierte Anleitung  
**Status:** ✅ Aktuell

---

## Technische Dokumentationen

### 4. [test_data/ABISCO_TO_ABANINJA_MAPPING.md](./test_data/ABISCO_TO_ABANINJA_MAPPING.md)
**Vollständiges Daten-Mapping zwischen Abisco und ABA Ninja**

Diese Datei dokumentiert die exakte Übersetzung der Datenmodelle:
- Analyse der existierenden ABA Ninja Rechnung
- Mapping-Tabellen für Rechnungskopf, Kunde, Zahlungsinformationen und Positionen
- Wichtige Erkenntnisse (z.B. benötigte UUIDs)
- Fehlende Informationen und nächste Schritte

**Zielgruppe:** Entwickler und KI-Agenten  
**Umfang:** Technische Details  
**Status:** ✅ Aktuell

---

### 5. [docs/PAYMENT_RECONCILIATION.md](./docs/PAYMENT_RECONCILIATION.md)
**Dokumentation des Zahlungsabgleichs**

Diese Datei beschreibt den bidirektionalen Zahlungsabgleich zwischen Bank, ABA Ninja und Abisco.

**Zielgruppe:** Entwickler und KI-Agenten  
**Umfang:** Technische Details  
**Status:** ✅ Aktuell (falls vorhanden)

---

## Scripts und Code

### 6. [scripts/create_invoice_from_abisco.py](./scripts/create_invoice_from_abisco.py)
**Proof-of-Concept-Skript für Rechnungserstellung**

Dieses Python-Skript demonstriert die erfolgreiche Erstellung einer Rechnung in ABA Ninja aus Abisco-Daten. Es dient als Vorlage für den produktiven Import.

**Funktionen:**
- Lädt Testdaten aus einem Python-Dictionary
- Konvertiert Abisco-Daten in das ABA Ninja-Format
- Sendet die Rechnung über die API
- Gibt detaillierte Logs aus

**Status:** ✅ Funktioniert (Rechnung R0002 erfolgreich erstellt)

---

### 7. [scripts/extract_abisco_invoices.py](./scripts/extract_abisco_invoices.py)
**Skript zur Extraktion von Rechnungsdaten aus der Abisco-Datenbank**

Dieses Skript extrahiert alle Rechnungen und Gutschriften aus der PostgreSQL-Datenbank und speichert sie in einer JSON-Datei.

**Status:** ✅ Funktioniert

---

## Daten und Exports

### 8. [data/Kunden_Rechnungen.xlsx](./data/Kunden_Rechnungen.xlsx)
**Excel-Export mit Kundendaten und Rechnungen**

Diese Excel-Datei enthält:
- Ein Arbeitsblatt pro Kunde
- Alle Rechnungen des Kunden mit Details (Nummer, Datum, Betrag, Status, etc.)
- Kundenstammdaten

**Status:** ✅ Erstellt und committed

---

## Verwendung

### Für KI-Agenten, die das Projekt übernehmen:

1.  **Start:** Lies zuerst [HANDOVER_FOR_AI.md](./HANDOVER_FOR_AI.md) für einen vollständigen Überblick.
2.  **Überblick:** Konsultiere [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md) für den aktuellen Stand.
3.  **Durchführung:** Folge der [STEP_BY_STEP_GUIDE.md](./STEP_BY_STEP_GUIDE.md) für die Implementierung.
4.  **Technische Details:** Nutze [test_data/ABISCO_TO_ABANINJA_MAPPING.md](./test_data/ABISCO_TO_ABANINJA_MAPPING.md) für das Daten-Mapping.

### Für Entwickler:

1.  **Überblick:** Lies [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md).
2.  **Code:** Analysiere die Scripts in `scripts/`.
3.  **API-Mapping:** Konsultiere [test_data/ABISCO_TO_ABANINJA_MAPPING.md](./test_data/ABISCO_TO_ABANINJA_MAPPING.md).

---

## Repository-Information

**Repository-Name:** `Motorlink/Swiss21`  
**GitHub-URL:** https://github.com/Motorlink/Swiss21

**Letzter Commit:** Vollständige Dokumentation für KI-Übergabe hinzugefügt  
**Datum:** 2025-12-17

---

**Erstellt von:** Manus AI  
**Datum:** 2025-12-17
